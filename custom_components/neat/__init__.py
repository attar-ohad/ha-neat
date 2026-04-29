from .const import DOMAIN
from .coordinator import NeatCoordinator

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})

    coordinator = NeatCoordinator(
        hass,
        entry.data["token"],
        entry.data["org_id"],
        entry.data["devices"],
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "binary_sensor"]
    )

    return True
