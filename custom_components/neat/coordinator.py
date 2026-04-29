from datetime import timedelta
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import API_BASE, SCAN_INTERVAL

class NeatCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, token, org, devices):
        self.session = aiohttp.ClientSession()
        self.token = token
        self.org = org
        self.devices = devices
        self.last_data = {}
        self.device_meta = {}

        super().__init__(
            hass,
            logger=None,
            name="Neat Pulse",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        new_data = {}

        for device in self.devices:
            url = f"{API_BASE}/orgs/{self.org}/endpoints/{device}/sensor"

            try:
                async with self.session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        new_data[device] = data
                        self.last_data[device] = data

                        # שמות אמיתיים
                        self.device_meta[device] = {
                            "name": data.get("endpointData", {}).get("roomName", device),
                            "model": data.get("endpointData", {}).get("model", "")
                        }
                    else:
                        new_data[device] = self.last_data.get(device)

            except:
                new_data[device] = self.last_data.get(device)

        return new_data
