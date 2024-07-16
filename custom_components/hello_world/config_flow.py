"""Config flow for Hello, state! integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN

class HelloStateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello, state!"""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if user_input is not None:
            if user_input["button"] == "button_1":
                return await self.async_step_host()
            elif user_input["button"] == "button_2":
                return await self.async_step_host()

        return self.async_show_menu(
            step_id="user",
            menu_options=[
                {"button": "button_1", "description": "IP bekannt"},
                {"button": "button_2", "description": "IP unbekannt"},
            ],
        )
    
    async def async_step_host(self, user_input=None):
        if user_input is not None:
            host = user_input[CONF_HOST]
            return self.async_create_entry(title="Hello world!", data={CONF_HOST: host})
        
        return self.async_show_form(
            step_id="host",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
        )