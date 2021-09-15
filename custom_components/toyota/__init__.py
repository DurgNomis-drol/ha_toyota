"""Toyota integration"""
import asyncio
import asyncio.exceptions as asyncioexceptions
from datetime import timedelta
import logging

import async_timeout
import httpcore
import httpx
from mytoyota.client import MyT
from mytoyota.exceptions import ToyotaApiError, ToyotaInternalError, ToyotaLoginError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_REGION,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONF_UNIT_SYSTEM_METRIC,
    LENGTH_MILES,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_USE_LITERS_PER_100_MILES,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEFAULT_LOCALE,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE, CONF_UNIT_SYSTEM_IMPERIAL_LITERS,
)

_LOGGER = logging.getLogger(__name__)

# Update sensors every 5 minutes
UPDATE_INTERVAL = timedelta(seconds=90)


async def with_timeout(task, timeout_seconds=15):
    """Run an async task with a timeout."""
    async with async_timeout.timeout(timeout_seconds):
        return await task


async def async_setup_entry(  # pylint: disable=too-many-statements
    hass: HomeAssistant, entry: ConfigEntry
):
    """Set up Toyota Connected Services from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    region = entry.data[CONF_REGION]
    use_liters = entry.options.get(CONF_USE_LITERS_PER_100_MILES, False)

    client = MyT(
        username=email,
        password=password,
        locale=DEFAULT_LOCALE,
        region=region.lower(),
    )

    await client.login()

    async def async_update_data():
        """Fetch data from Toyota API."""

        try:

            vehicles = []

            cars = await with_timeout(client.get_vehicles())

            for car in cars:
                vehicle = await client.get_vehicle_status(car)

                if vehicle.odometer.unit == LENGTH_MILES:
                    _LOGGER.debug("The car is reporting data in imperial")
                    if use_liters:
                        _LOGGER.debug("Get statistics in imperial and L/100 miles")
                        unit = CONF_UNIT_SYSTEM_IMPERIAL_LITERS
                    else:
                        _LOGGER.debug("Get statistics in imperial and MPG")
                        unit = CONF_UNIT_SYSTEM_IMPERIAL
                else:
                    _LOGGER.debug("The car is reporting data in metric")
                    unit = CONF_UNIT_SYSTEM_METRIC

                # Use parallel request to get car statistics.
                data = await asyncio.gather(
                    *[
                        client.get_driving_statistics(
                            vehicle.vin, interval="isoweek", unit=unit
                        ),
                        client.get_driving_statistics(vehicle.vin, unit=unit),
                        client.get_driving_statistics(
                            vehicle.vin, interval="year", unit=unit
                        ),
                    ]
                )

                vehicle.statistics.weekly = data[0]
                vehicle.statistics.monthly = data[1]
                vehicle.statistics.yearly = data[2]

                vehicles.append(vehicle)

            _LOGGER.debug(vehicles)
            return vehicles

        except ToyotaLoginError as ex:
            _LOGGER.error(ex)
        except ToyotaInternalError as ex:
            _LOGGER.debug(ex)
        except ToyotaApiError as ex:
            raise UpdateFailed(ex) from ex
        except (httpx.ConnectTimeout, httpcore.ConnectTimeout) as ex:
            raise UpdateFailed("Unable to connect to Toyota Connected Services") from ex
        except (
            asyncioexceptions.CancelledError,
            asyncioexceptions.TimeoutError,
            httpx.ReadTimeout,
        ) as ex:

            raise UpdateFailed(
                "Update canceled! Toyota's API was too slow to respond."
                " Will try again later..."
            ) from ex

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
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
