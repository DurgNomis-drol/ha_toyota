"""Toyota integration"""
import asyncio
from datetime import timedelta
import logging

import async_timeout
from .toyota import MyT

from homeassistant.config_entries import SOURCE_REAUTH, ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_API_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util.async_ import gather_with_concurrency

from .const import DATA_CLIENT, DATA_COORDINATOR, DOMAIN
from .const import ODOMETER, ODOMETER_UNIT, FUEL, PARKING, BATTERY, HVAC, LAST_UPDATED, VEHICLE_INFO, NICKNAME, VIN
from .const import CONF_NICKNAME, CONF_VIN, CONF_LOCALE, CONF_UUID

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Toyota Connected Services component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Toyota Connected Services from a config entry."""
    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    locale = entry.data[CONF_LOCALE]
    nickname = entry.data[CONF_NICKNAME]
    vin = entry.data[CONF_VIN]
    uuid = entry.data[CONF_UUID]
    token = entry.data[CONF_API_TOKEN]

    # websession = aiohttp_client.async_get_clientsession(hass)
    client = ToyotaApi(username=email, password=password, locale=locale, vin=vin, uuid=uuid, token=token)

    async def async_update_data():
        """Fetch data from Toyota API."""
        return await client.gather_information(nickname=nickname, vin=vin)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),
    )

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
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

    def __init__(self, coordinator):
        """Initialize the Toyota entity."""
        super().__init__(coordinator)
        self.vin = self.coordinator.data[VIN]
        self.nickname = self.coordinator.data[NICKNAME]
        self.last_updated = self.coordinator.data[LAST_UPDATED]

    @property
    def device_info(self):
        """Return device info for the Toyota entity."""
        return {
            "identifiers": {(DOMAIN, self.vin)},
            "name": self.nickname,
            "manufacturer": "Toyota",
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {self.last_updated}


class ToyotaApi:
    """Toyota API"""

    def __init__(
        self,
        username: str,
        password: str,
        locale: str,
        vin: str,
        uuid: str = None,
        token: str = None,
         ) -> None:
        self.username = username
        self.password = password
        self.locale = locale
        self.uuid = uuid
        self.vin = vin
        self.token = token
        self.client = MyT(
            username=self.username, password=self.password, locale=self.locale, vin=self.vin, token=self.token
        )

    async def test_credentials(self, username, password):
        """Tests if your credentials are valid."""
        token, uuid = self.client.perform_login(username=username, password=password)
        if token is not None and uuid is not None:
            return token, uuid
        else:
            return False

    async def gather_information(self, nickname: str, vin: str) -> dict:
        """Gather information from different endpoints and collect it."""
        async def with_timeout(task):
            async with async_timeout.timeout(10):
                return await task

        odometer, odometer_unit, fuel = await with_timeout(self.client.get_odometer())

        parking = await with_timeout(self.client.get_parking())

        battery, hvac, last_updated = await with_timeout(self.client.get_vehicle_information())

        vehicle = {
            NICKNAME: nickname,
            VIN: vin,
            LAST_UPDATED: last_updated,
            PARKING: parking,
            VEHICLE_INFO: {
                ODOMETER: odometer,
                ODOMETER_UNIT: odometer_unit,
                FUEL: fuel,
                BATTERY: battery,
                HVAC: hvac
            }
        }

        _LOGGER.debug(vehicle)

        return vehicle

