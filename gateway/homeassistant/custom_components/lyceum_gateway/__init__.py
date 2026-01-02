"""
Lyceum LoRa Gateway Integration for Home Assistant

This integration allows using an E22-900T22U USB LoRa module as a
Lyceum network gateway. It provides:

- Sensor: Last received message, RSSI, link quality
- Service: Send message to the Lyceum mesh
- Events: Incoming messages for automations

Use Case: Backbone relay during The Lyceum bootstrapping phase,
using your home's internet to relay messages between distant nodes.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .gateway import LyceumGatewayDevice

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lyceum Gateway from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Create gateway device
    gateway = LyceumGatewayDevice(
        hass,
        port=entry.data["port"],
        channel=entry.data.get("channel", 4),
        aes_key=bytes.fromhex(entry.data["aes_key"]) if entry.data.get("aes_key") else None,
        node_id=entry.data.get("node_id", "!ha_gateway"),
    )
    
    # Start the gateway
    await gateway.async_start()
    
    hass.data[DOMAIN][entry.entry_id] = gateway
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    await async_setup_services(hass, gateway)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        gateway = hass.data[DOMAIN].pop(entry.entry_id)
        await gateway.async_stop()
    
    return unload_ok


async def async_setup_services(hass: HomeAssistant, gateway: LyceumGatewayDevice) -> None:
    """Set up Lyceum Gateway services."""
    
    async def handle_send_message(call) -> None:
        """Handle the send_message service call."""
        destination = call.data.get("destination", 0xFFFF)  # Broadcast by default
        message = call.data["message"]
        channel = call.data.get("channel", gateway.channel)
        
        await gateway.async_send_message(destination, channel, message)
        
        _LOGGER.info("Sent Lyceum message to %s: %s", hex(destination), message[:50])
    
    async def handle_relay_to_internet(call) -> None:
        """Handle relay_to_internet service for backbone mode."""
        # This would forward the message to a remote Lyceum relay server
        # during the bootstrapping phase when mesh coverage is limited
        message = call.data["message"]
        relay_url = call.data.get("relay_url", "https://relay.lyceum.example.org")
        
        await gateway.async_relay_to_internet(message, relay_url)
    
    hass.services.async_register(DOMAIN, "send_message", handle_send_message)
    hass.services.async_register(DOMAIN, "relay_to_internet", handle_relay_to_internet)
