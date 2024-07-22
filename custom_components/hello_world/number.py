from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
import logging

_LOGGER = logging.getLogger(__name__)

# Default-Werte
DEFAULT_NAME = 'Custom Number'
DEFAULT_MIN_VALUE = 30
DEFAULT_MAX_VALUE = 70

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up the custom number entity."""
    name = entry.options.get('name', DEFAULT_NAME)
    async_add_entities([CustomNumberEntity(name)])

class CustomNumberEntity(NumberEntity):
    """Representation of a custom number entity."""

    def __init__(self, name):
        """Initialize the number entity."""
        self._name = name
        self._min_value = DEFAULT_MIN_VALUE
        self._max_value = DEFAULT_MAX_VALUE
        self._value = self._min_value  # Default value to min_value

    @property
    def unique_id(self):
        """Return a unique ID for this entity."""
        return self._name

    @property
    def name(self):
        """Return the display name of this entity."""
        return self._name

    @property
    def min_value(self):
        """Return the minimum value of this number."""
        return self._min_value

    @property
    def max_value(self):
        """Return the maximum value of this number."""
        return self._max_value

    @property
    def value(self):
        """Return the current value of this number."""
        return self._value

    async def async_set_value(self, value: float):
        """Set a new value for this number."""
        if self._min_value <= value <= self._max_value:
            self._value = value
            self.async_write_ha_state()
        else:
            _LOGGER.error("Value %s is out of range [%s, %s]", value, self._min_value, self._max_value)