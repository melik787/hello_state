"""Config flow for Hello, state! integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from aiohttp import ClientTimeout
import ipaddress
import logging
import aiohttp
import asyncio

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HelloStateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello, state!"""

    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self) -> None:
        self._devices = {}
        self._host = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        return self.async_show_menu(
            step_id="user",
            menu_options={
                "ip_known": "IP address",
                "ip_unknown": "IP subnet scan"
            },
        )   
    
    async def async_step_ip_known(self, user_input=None):
        if user_input is not None:
            host = user_input[CONF_HOST]
            if self.is_valid_ip(host):
                if await self.check_ip_device(host):
                    return self.async_create_entry(title="Hello world! IP known", data={CONF_HOST: host})
        
        return self.async_show_form(
            step_id="ip_known",
            data_schema=vol.Schema({vol.Required(CONF_HOST, default="192.168.0.0"): str}),
        )
    
    async def async_step_ip_unknown(self, user_input=None):
        errors = {}
        if user_input is not None:
            subnet = user_input["subnet"]
            if self.is_valid_subnet(subnet):
                self._devices = await self.scan_devices(subnet)
                if self._devices:    
                    return await self.async_step_select_device()
                else:
                    errors["base"] = "no devices found"
            else:
                errors["base"] = "invalid_subnet"
            
        return self.async_show_form(
            step_id="ip_unknown",
            data_schema=vol.Schema({vol.Required("subnet", default="192.168.0"): str}),
            errors=errors
        )  
    
    async def async_step_select_device(self, user_input=None):
        if user_input is not None:
            selected_ip = user_input["device"]
            return self.async_create_entry(title="Hello world! IP unknown", data={CONF_HOST: selected_ip})
        
        return self.async_show_form(
            step_id="select_device",
            data_schema=vol.Schema({
                vol.Required("device"): vol.In(list(self._devices.keys()))
            }),
            description_placeholders={"devices": ", ".join(self._devices.keys())}
        )  
        
    def is_valid_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            _LOGGER.error("You entered an invalid IP")
            return False
    
    def is_valid_subnet(self, subnet):
        cntPeriod = subnet.count('.')
        if cntPeriod != 2:
            _LOGGER.error("Invalid subnet")
            return False
        ip = subnet + ".0"
        return self.is_valid_ip(ip)
        
    async def check_ip_device(self, ip):
        async with aiohttp.ClientSession() as session:
            return await self.check_device(session, ip)
    
    async def scan_devices(self, subnet):
        devices = {}
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(1, 255):
                ip = f"{subnet}.{i}"
                tasks.append(self.check_device(session, ip))

            results = await asyncio.gather(*tasks)

            for ip, is_device in zip([f"{subnet}.{i}" for i in range(1, 255)], results):
                if is_device:
                    devices[ip] = f"my-PV Device {ip}"

        return devices
    
    async def check_device(self, session, ip):
        try:
            timeout = ClientTimeout(total=10)
            async with session.get(f"http://{ip}/mypv_dev.jsn", timeout=timeout) as response:
                return response.status == 200
        except aiohttp.ClientError as e:
            return False
        except asyncio.TimeoutError as e:
            return False