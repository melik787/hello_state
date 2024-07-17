"""Config flow for Hello, state! integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
import ipaddress
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HelloStateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello, state!"""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        return self.async_show_menu(
            step_id="user",
            menu_options={
                "ip_known": "IP Adresse bekannt",
                "ip_unknown": "IP Adresse unbekannt"
            },
        )   
    
    async def async_step_ip_known(self, user_input=None):
        if user_input is not None:
            host = user_input[CONF_HOST]
            return self.async_create_entry(title="Hello world! IP known", data={CONF_HOST: host})
        
        return self.async_show_form(
            step_id="ip_known",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
        )
    
    async def async_step_ip_unknown(self, user_input=None):
        errors = {}
        if user_input is not None:
            subnet = user_input["subnet"]
            if self.is_valid_subnet(subnet):
                return self.async_create_entry(title="Hello world! IP unknown", data={CONF_HOST: subnet})
            else:
                errors["base"] = "invalid_subnet"
            
        return self.async_show_form(
            step_id="ip_unknown",
            data_schema=vol.Schema({vol.Required("subnet", default="192.168.0.0"): str}),
            errors=errors
        )  
    
    def is_valid_subnet(self, subnet):
        try:
            ipaddress.ip_network(subnet)
            return True
        except ValueError:
            _LOGGER.error("You entered an invalid subnet")
            return False
    
    # def scan_devices(self, subnet):