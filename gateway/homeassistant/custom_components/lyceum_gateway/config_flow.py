"""Config flow for Lyceum Gateway integration."""
from __future__ import annotations

import logging
from typing import Any

import serial.tools.list_ports
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_PORT,
    CONF_CHANNEL,
    CONF_AES_KEY,
    CONF_NODE_ID,
    CONF_BACKBONE_MODE,
    CONF_RELAY_URL,
    DEFAULT_CHANNEL,
    DEFAULT_NODE_ID,
    DEFAULT_RELAY_URL,
)

_LOGGER = logging.getLogger(__name__)


def get_serial_ports() -> list[str]:
    """Get available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


class LyceumGatewayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lyceum Gateway."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        # Get available serial ports
        ports = await self.hass.async_add_executor_job(get_serial_ports)
        
        if not ports:
            return self.async_abort(reason="no_serial_ports")

        if user_input is not None:
            # Validate the port exists
            if user_input[CONF_PORT] not in ports:
                errors[CONF_PORT] = "port_not_found"
            
            # Validate AES key if provided
            if user_input.get(CONF_AES_KEY):
                try:
                    key_bytes = bytes.fromhex(user_input[CONF_AES_KEY])
                    if len(key_bytes) not in (16, 24, 32):
                        errors[CONF_AES_KEY] = "invalid_key_length"
                except ValueError:
                    errors[CONF_AES_KEY] = "invalid_hex"
            
            if not errors:
                # Create unique ID from port
                await self.async_set_unique_id(user_input[CONF_PORT])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"Lyceum Gateway ({user_input[CONF_PORT]})",
                    data=user_input,
                )

        # Build schema with discovered ports
        data_schema = vol.Schema({
            vol.Required(CONF_PORT): vol.In(ports),
            vol.Optional(CONF_CHANNEL, default=DEFAULT_CHANNEL): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=83)
            ),
            vol.Optional(CONF_NODE_ID, default=DEFAULT_NODE_ID): str,
            vol.Optional(CONF_AES_KEY): str,
            vol.Optional(CONF_BACKBONE_MODE, default=False): bool,
            vol.Optional(CONF_RELAY_URL, default=DEFAULT_RELAY_URL): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "ports": ", ".join(ports),
            },
        )
