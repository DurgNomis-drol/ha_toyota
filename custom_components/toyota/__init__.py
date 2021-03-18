"""Toyota integration"""
import asyncio
from datetime import timedelta
import logging

from mytoyota.client import MyT
from mytoyota.exceptions import ToyotaLoginError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_TOKEN, CONF_EMAIL, CONF_PASSWORD, CONF_REGION
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ALIAS,
    CONF_LOCALE,
    CONF_UUID,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DETAILS,
    DOMAIN,
    HYBRID,
    MODEL,
    STARTUP_MESSAGE,
    VIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "device_tracker"]

# Update sensors every 5 minutes
UPDATE_INTERVAL = timedelta(seconds=300)


async def async_setup(_hass: HomeAssistant, _config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Toyota Connected Services from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    locale = entry.data[CONF_LOCALE]
    uuid = entry.data[CONF_UUID]
    token = entry.data[CONF_API_TOKEN]
    region = entry.data[CONF_REGION]

    client = MyT(
        username=email,
        password=password,
        locale=locale,
        uuid=uuid,
        region=region.lower(),
        token=token,
    )

    async def async_update_data():
        """Fetch data from Toyota API."""

        vehicles = []

        try:
            vehicles = await client.gather_information()
        except ToyotaLoginError as ex:
            _LOGGER.error(ex)
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error(ex)

        _LOGGER.debug(vehicles)
        return vehicles

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=UPDATE_INTERVAL,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    # Setup components
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class ToyotaEntity(CoordinatorEntity):
    """Defines a base Toyota entity."""

    def __init__(self, coordinator, index):
        """Initialize the Toyota entity."""
        super().__init__(coordinator)
        self.index = index
        self.vin = self.coordinator.data[self.index][VIN]
        self.alias = self.coordinator.data[self.index][ALIAS]
        self.model = self.coordinator.data[self.index][DETAILS][MODEL]
        self.hybrid = self.coordinator.data[self.index][DETAILS][HYBRID]

    @property
    def device_info(self):
        """Return device info for the Toyota entity."""
        return {
            "identifiers": {(DOMAIN, self.vin)},
            "name": self.alias,
            "model": self.model,
            "manufacturer": "ha_toyota",
        }
