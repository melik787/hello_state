from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_HOST
import random

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Hello, state! sensor."""
    host = entry.data[CONF_HOST]
    async_add_entities([HelloStateSensor(host)], True)

class HelloStateSensor(SensorEntity):
    """Representation of a Hello, state! sensor."""

    def __init__(self, host: str):
        """Initialize the sensor."""
        self._host = host
        self._state = 69

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Device {self._host}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"hello_state_{self._host}"


