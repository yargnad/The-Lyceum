"""
Lyceum LoRa Gateway Integration for Home Assistant

This integration allows using an E22-900T22U USB LoRa module as a
Lyceum network gateway. It provides:

- Sensor: Last received message, RSSI, link quality
- Service: Send message to the Lyceum mesh
- Events: Incoming messages for automations
- Guardian Mode: Contribute compute resources to the Pneuma network

Use Case: Backbone relay during The Lyceum bootstrapping phase,
using your home's internet to relay messages between distant nodes.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_GUARDIAN_ENABLED,
    CONF_GUARDIAN_SKILLS,
    CONF_GUARDIAN_CPU_LIMIT,
    CONF_GUARDIAN_MEMORY_LIMIT,
    CONF_GUARDIAN_SYMBOLONS,
    CONF_GUARDIAN_EARN_TOKENS,
    DEFAULT_GUARDIAN_CPU,
    DEFAULT_GUARDIAN_MEMORY,
    EVENT_JOB_COMPLETED,
)
from .gateway import LyceumGatewayDevice
from .guardian import GuardianDaemon, GuardianConfig, ResourceLimits

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
    
    # Create Guardian if enabled
    guardian = None
    if entry.data.get(CONF_GUARDIAN_ENABLED, False):
        guardian_config = GuardianConfig(
            enabled=True,
            node_id=entry.data.get("node_id", "!ha_guardian"),
            skills=entry.data.get(CONF_GUARDIAN_SKILLS, ["relay"]),
            limits=ResourceLimits(
                cpu_percent=entry.data.get(CONF_GUARDIAN_CPU_LIMIT, DEFAULT_GUARDIAN_CPU),
                memory_mb=entry.data.get(CONF_GUARDIAN_MEMORY_LIMIT, DEFAULT_GUARDIAN_MEMORY),
            ),
            symbolons=entry.data.get(CONF_GUARDIAN_SYMBOLONS, []),
            earn_tokens=entry.data.get(CONF_GUARDIAN_EARN_TOKENS, True),
        )
        guardian = GuardianDaemon(hass, guardian_config)
        await guardian.async_start()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "gateway": gateway,
        "guardian": guardian,
    }
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    await async_setup_services(hass, gateway, guardian)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["gateway"].async_stop()
        if data["guardian"]:
            await data["guardian"].async_stop()
    
    return unload_ok


async def async_setup_services(
    hass: HomeAssistant,
    gateway: LyceumGatewayDevice,
    guardian: GuardianDaemon | None,
) -> None:
    """Set up Lyceum Gateway services."""
    
    async def handle_send_message(call) -> None:
        """Handle the send_message service call."""
        destination = call.data.get("destination", 0xFFFF)
        message = call.data["message"]
        channel = call.data.get("channel", gateway.channel)
        
        await gateway.async_send_message(destination, channel, message)
        _LOGGER.info("Sent Lyceum message to %s: %s", hex(destination), message[:50])
    
    async def handle_relay_to_internet(call) -> None:
        """Handle relay_to_internet service for backbone mode."""
        message = call.data["message"]
        relay_url = call.data.get("relay_url", "https://relay.lyceum.example.org")
        await gateway.async_relay_to_internet(message, relay_url)
    
    async def handle_guardian_stats(call) -> dict:
        """Get Guardian statistics."""
        if not guardian:
            return {"error": "Guardian not enabled"}
        return guardian.stats
    
    async def handle_start_symbolon(call) -> None:
        """Start a Symbolon application."""
        if not guardian or not guardian._symbolon_runtime:
            _LOGGER.warning("Symbolon runtime not available")
            return
        name = call.data["name"]
        await guardian._symbolon_runtime.start_symbolon(name)
    
    async def handle_stop_symbolon(call) -> None:
        """Stop a Symbolon application."""
        if not guardian or not guardian._symbolon_runtime:
            return
        name = call.data["name"]
        await guardian._symbolon_runtime.stop_symbolon(name)
    
    hass.services.async_register(DOMAIN, "send_message", handle_send_message)
    hass.services.async_register(DOMAIN, "relay_to_internet", handle_relay_to_internet)
    hass.services.async_register(DOMAIN, "guardian_stats", handle_guardian_stats)
    hass.services.async_register(DOMAIN, "start_symbolon", handle_start_symbolon)
    hass.services.async_register(DOMAIN, "stop_symbolon", handle_stop_symbolon)

