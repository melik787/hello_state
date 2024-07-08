from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Hello, state! sensor."""
    host = entry.data[CONF_HOST]
    async_add_entities([MySwitch(host)], True)
    return True

class MySwitch(SwitchEntity):
    def __init__(self, host):
        """Initialize the switch"""
        self._name = f"Switch ww1Boost {host}"
        self._is_on = False
    
    @property
    def is_on(self):
        return self._is_on

    @property
    def name(self):
        return self._name
    
    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()

    
    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()

