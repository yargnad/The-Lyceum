"""Binary sensor platform for Lyceum Gateway."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .gateway import LyceumGatewayDevice


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lyceum Gateway binary sensors."""
    gateway: LyceumGatewayDevice = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([
        LyceumConnectionSensor(gateway, entry),
    ])


class LyceumConnectionSensor(BinarySensorEntity):
    """Binary sensor showing gateway connection state."""

    _attr_name = "Gateway Connected"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(
        self,
        gateway: LyceumGatewayDevice,
        entry: ConfigEntry,
    ) -> None:
        self._gateway = gateway
        self._entry = entry

    @property
    def unique_id(self) -> str:
        return f"{self._gateway.port}_connected"

    @property
    def is_on(self) -> bool:
        return self._gateway._running and self._gateway._gateway is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._gateway.port)},
            "name": f"Lyceum Gateway ({self._gateway.port})",
            "manufacturer": "The Lyceum",
            "model": "E22-900T22U",
        }
