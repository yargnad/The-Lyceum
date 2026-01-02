"""Sensor platform for Lyceum Gateway."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ATTR_RSSI, ATTR_SNR, ATTR_SENDER, ATTR_TIMESTAMP
from .gateway import LyceumGatewayDevice

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lyceum Gateway sensors."""
    gateway: LyceumGatewayDevice = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        LyceumLastMessageSensor(gateway, entry),
        LyceumMessageCountSensor(gateway, entry),
        LyceumRSSISensor(gateway, entry),
    ]
    
    async_add_entities(entities)


class LyceumBaseSensor(SensorEntity):
    """Base class for Lyceum sensors."""

    def __init__(
        self,
        gateway: LyceumGatewayDevice,
        entry: ConfigEntry,
    ) -> None:
        self._gateway = gateway
        self._entry = entry
        self._attr_has_entity_name = True

    async def async_added_to_hass(self) -> None:
        """Register callbacks when added to hass."""
        self._gateway.register_callback(self._handle_update)

    async def async_will_remove_from_hass(self) -> None:
        """Clean up when removed from hass."""
        self._gateway.unregister_callback(self._handle_update)

    @callback
    def _handle_update(self) -> None:
        """Handle updated data from gateway."""
        self.async_write_ha_state()

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._gateway.port)},
            "name": f"Lyceum Gateway ({self._gateway.port})",
            "manufacturer": "The Lyceum",
            "model": "E22-900T22U",
            "sw_version": "0.1.0",
        }


class LyceumLastMessageSensor(LyceumBaseSensor):
    """Sensor showing the last received message."""

    _attr_name = "Last Message"
    _attr_icon = "mdi:message-text"

    @property
    def unique_id(self) -> str:
        return f"{self._gateway.port}_last_message"

    @property
    def native_value(self) -> str | None:
        return self._gateway.last_message

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            ATTR_RSSI: self._gateway.last_rssi,
            ATTR_SNR: self._gateway.last_snr,
        }


class LyceumMessageCountSensor(LyceumBaseSensor):
    """Sensor showing message count."""

    _attr_name = "Message Count"
    _attr_icon = "mdi:counter"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def unique_id(self) -> str:
        return f"{self._gateway.port}_message_count"

    @property
    def native_value(self) -> int:
        return self._gateway.message_count


class LyceumRSSISensor(LyceumBaseSensor):
    """Sensor showing RSSI of last received message."""

    _attr_name = "Signal Strength"
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = "dBm"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        return f"{self._gateway.port}_rssi"

    @property
    def native_value(self) -> int:
        return self._gateway.last_rssi
