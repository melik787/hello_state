"""Config flow for Hello, state! integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN

class HelloStateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello, state!"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            return self.async_create_entry(
                title=f"Hello {host}",
                data={CONF_HOST: host},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )
