"""The Hello, state! integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the hello_state integration from YAML."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up hello_state from a config entry."""
    _LOGGER.info("Sensor entry setup")
    hass.async_create_task(
    hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    hass.async_create_task(
    hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    _LOGGER.info("Switch entry setup")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "switch")
    return unload_ok