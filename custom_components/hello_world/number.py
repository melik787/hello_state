from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
from homeassistant.const import UnitOfTemperature
import logging

_LOGGER = logging.getLogger(__name__)

# Default-Werte
DEFAULT_NAME = 'ww1Boost'
DEFAULT_MIN_VALUE = 30
DEFAULT_MAX_VALUE = 70
DEFAULT_STEP = 0.1

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
        self._value = 50  # Default value within range
        self._step = DEFAULT_STEP
        self._unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def unique_id(self):
        """Return a unique ID for this entity."""
        return self._name

    @property
    def name(self):
        """Return the display name of this entity."""
        return self._name

    @property
    def native_min_value(self):
        """Return the minimum value of this number."""
        return self._min_value

    @property
    def native_max_value(self):
        """Return the maximum value of this number."""
        return self._max_value

    @property
    def native_value(self):
        """Return the current value of this number."""
        return self._value
    
    @property
    def native_step(self):
        """Return the step size for this number."""
        return self._step
    
    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement for this number."""
        return self._unit_of_measurement

    async def async_set_value(self, value: float):
        """Set a new value for this number."""
        if self._min_value <= value <= self._max_value:
            self._value = value
            self.async_write_ha_state()
        else:
            _LOGGER.error("Value %s is out of range [%s, %s]", value, self._min_value, self._max_value)