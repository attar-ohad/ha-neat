import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_TOKEN, CONF_ORG, CONF_DEVICES
import aiohttp

class NeatPulseConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.token = user_input[CONF_TOKEN]
            self.org = user_input[CONF_ORG]

            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"https://api.pulse.neat.no/v1/orgs/{self.org}/endpoints"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    data = await resp.json()

            self.devices = {
                d["id"]: f'{d.get("roomName", "Unknown")} ({d.get("model", "")})'
                for d in data.get("endpoints", [])
                if d.get("connected")
            }

            return await self.async_step_select_devices()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_TOKEN): str,
                vol.Required(CONF_ORG): str,
            })
        )

    async def async_step_select_devices(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Neat Pulse",
                data={
                    CONF_TOKEN: self.token,
                    CONF_ORG: self.org,
                    CONF_DEVICES: user_input[CONF_DEVICES],
                },
            )

        return self.async_show_form(
            step_id="select_devices",
            data_schema=vol.Schema({
                vol.Required(CONF_DEVICES): vol.MultiSelect(self.devices)
            })
        )
