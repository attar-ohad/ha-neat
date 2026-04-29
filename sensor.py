from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

SENSORS = {
    "temperature": ("temp", "°C", "temperature"),
    "humidity": ("humidity", "%", "humidity"),
    "people": ("people", None, None),
    "illumination": ("illumination", "lx", None),
    "voc_index": ("vocIndex", None, None),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for device_id in coordinator.devices:
        for name, (key, unit, device_class) in SENSORS.items():
            entities.append(
                NeatSensor(coordinator, device_id, name, key, unit, device_class)
            )

    async_add_entities(entities)


class NeatSensor(CoordinatorEntity):

    def __init__(self, coordinator, device_id, name, key, unit, device_class):
        super().__init__(coordinator)
        self.device_id = device_id
        self.key = key
        self.name_type = name

        self._attr_unique_id = f"{device_id}_{name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class

    @property
    def name(self):
        meta = self.coordinator.device_meta.get(self.device_id, {})
        return f"{meta.get('name', self.device_id)} {self.name_type}"

    @property
    def device_info(self) -> DeviceInfo:
        meta = self.coordinator.device_meta.get(self.device_id, {})
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=meta.get("name", self.device_id),
            manufacturer="Neat",
            model=meta.get("model"),
        )

    @property
    def native_value(self):
        try:
            return self.coordinator.data[self.device_id]["endpointData"]["data"][0][self.key]
        except:
            return None
