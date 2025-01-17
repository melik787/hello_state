"""The Hello, state! integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the hello_state integration from YAML."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up hello_state from a config entry."""
    _LOGGER.info("Sensor and Switch entry setup")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch", "number"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch", "number"])
    return unload_ok