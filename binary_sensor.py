from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for device_id in coordinator.devices:
        entities.append(PresenceSensor(coordinator, device_id))
        entities.append(ShutterSensor(coordinator, device_id))

    async_add_entities(entities)


class PresenceSensor(CoordinatorEntity, BinarySensorEntity):

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id
        self._attr_unique_id = f"{device_id}_presence"
        self._attr_device_class = "occupancy"

    @property
    def name(self):
        meta = self.coordinator.device_meta.get(self.device_id, {})
        return f"{meta.get('name', self.device_id)} Presence"

    @property
    def device_info(self):
        meta = self.coordinator.device_meta.get(self.device_id, {})
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=meta.get("name", self.device_id),
            manufacturer="Neat",
            model=meta.get("model"),
        )

    @property
    def is_on(self):
        try:
            return self.coordinator.data[self.device_id]["endpointData"]["data"][0]["people"] > 0
        except:
            return False


class ShutterSensor(CoordinatorEntity, BinarySensorEntity):

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id
        self._attr_unique_id = f"{device_id}_shutter"
        self._attr_device_class = "opening"

    @property
    def name(self):
        meta = self.coordinator.device_meta.get(self.device_id, {})
        return f"{meta.get('name', self.device_id)} Camera Shutter"

    @property
    def device_info(self):
        meta = self.coordinator.device_meta.get(self.device_id, {})
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=meta.get("name", self.device_id),
            manufacturer="Neat",
            model=meta.get("model"),
        )

    @property
    def is_on(self):
        try:
            return not self.coordinator.data[self.device_id]["endpointData"]["shutterClosed"]
        except:
            return False
