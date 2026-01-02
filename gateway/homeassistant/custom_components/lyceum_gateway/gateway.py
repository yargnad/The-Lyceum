"""Gateway device wrapper for Home Assistant."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Callable, Optional

from homeassistant.core import HomeAssistant, callback
import aiohttp

from .const import (
    DOMAIN,
    EVENT_MESSAGE_RECEIVED,
    EVENT_MESSAGE_SENT,
    ATTR_RSSI,
    ATTR_SNR,
    ATTR_SENDER,
    ATTR_CHANNEL,
    ATTR_TIMESTAMP,
)

_LOGGER = logging.getLogger(__name__)


class LyceumGatewayDevice:
    """
    Wrapper for the E22 LoRa gateway device.
    
    Runs in a background thread/task and pushes events to HA
    when messages are received.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        port: str,
        channel: int = 4,
        aes_key: Optional[bytes] = None,
        node_id: str = "!ha_gateway",
    ):
        self.hass = hass
        self.port = port
        self.channel = channel
        self.aes_key = aes_key
        self.node_id = node_id
        
        self._gateway = None
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        # State
        self.last_message: Optional[str] = None
        self.last_rssi: int = 0
        self.last_snr: float = 0.0
        self.message_count: int = 0
        self._callbacks: list[Callable] = []

    async def async_start(self) -> None:
        """Start the gateway listener."""
        # Import here to avoid circular imports
        import sys
        import os
        
        # Add gateway package to path
        gateway_path = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )))
        if gateway_path not in sys.path:
            sys.path.insert(0, gateway_path)
        
        try:
            from e22_driver import LyceumGateway
            self._gateway = LyceumGateway(
                self.port,
                baud=115200,
                aes_key=self.aes_key,
            )
            _LOGGER.info("Lyceum Gateway connected on %s", self.port)
        except Exception as e:
            _LOGGER.error("Failed to connect to gateway: %s", e)
            raise
        
        self._running = True
        self._task = asyncio.create_task(self._listen_loop())

    async def async_stop(self) -> None:
        """Stop the gateway listener."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        if self._gateway:
            self._gateway.close()
            self._gateway = None
        
        _LOGGER.info("Lyceum Gateway stopped")

    async def _listen_loop(self) -> None:
        """Background loop to listen for incoming messages."""
        while self._running:
            try:
                # Poll for data (non-blocking check would be better)
                data = await self.hass.async_add_executor_job(
                    self._gateway.e22.read, 256
                )
                
                if data:
                    await self._handle_received_data(data)
                    
            except Exception as e:
                _LOGGER.error("Error in gateway listen loop: %s", e)
            
            await asyncio.sleep(0.1)

    async def _handle_received_data(self, data: bytes) -> None:
        """Process received LoRa data."""
        # Decrypt if we have a key
        if self.aes_key:
            plaintext = self._gateway.decrypt_payload(data)
            if plaintext is None:
                _LOGGER.warning("Failed to decrypt incoming packet")
                return
            data = plaintext
        
        try:
            message = data.decode("utf-8")
        except UnicodeDecodeError:
            _LOGGER.warning("Received non-UTF8 data")
            return
        
        # Update state
        self.last_message = message
        self.message_count += 1
        
        # Fire HA event for automations
        self.hass.bus.async_fire(EVENT_MESSAGE_RECEIVED, {
            "message": message,
            ATTR_RSSI: self.last_rssi,
            ATTR_SNR: self.last_snr,
            ATTR_CHANNEL: self.channel,
            ATTR_TIMESTAMP: datetime.now().isoformat(),
        })
        
        # Notify sensor updates
        for callback_fn in self._callbacks:
            callback_fn()
        
        _LOGGER.info("Received Lyceum message: %s", message[:50])

    async def async_send_message(
        self,
        destination: int,
        channel: int,
        message: str,
    ) -> None:
        """Send a message over LoRa."""
        if not self._gateway:
            raise RuntimeError("Gateway not connected")
        
        await self.hass.async_add_executor_job(
            self._gateway.send_text,
            destination,
            channel,
            message,
            int(self.node_id.replace("!", ""), 16) if self.node_id.startswith("!") else 0x0001,
        )
        
        # Fire event
        self.hass.bus.async_fire(EVENT_MESSAGE_SENT, {
            "message": message,
            "destination": hex(destination),
            ATTR_CHANNEL: channel,
            ATTR_TIMESTAMP: datetime.now().isoformat(),
        })

    async def async_relay_to_internet(self, message: str, relay_url: str) -> None:
        """
        Relay a message to the internet backbone.
        
        This is used during bootstrapping when mesh coverage is limited.
        The message is sent to a central relay server that can forward
        it to distant Lyceum nodes over the internet.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{relay_url}/relay",
                    json={
                        "message": message,
                        "node_id": self.node_id,
                        "channel": self.channel,
                        "timestamp": datetime.now().isoformat(),
                    },
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status == 200:
                        _LOGGER.info("Message relayed to internet backbone")
                    else:
                        _LOGGER.warning("Relay failed: %s", resp.status)
            except Exception as e:
                _LOGGER.error("Relay error: %s", e)

    def register_callback(self, callback_fn: Callable) -> None:
        """Register callback for state updates."""
        self._callbacks.append(callback_fn)

    def unregister_callback(self, callback_fn: Callable) -> None:
        """Unregister callback."""
        if callback_fn in self._callbacks:
            self._callbacks.remove(callback_fn)
