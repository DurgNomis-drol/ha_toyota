"""Toyota integration"""
from __future__ import annotations

import asyncio
import asyncio.exceptions as asyncioexceptions
from datetime import timedelta
import logging
from typing import Any, TypedDict

import async_timeout
import httpcore
import httpx
from mytoyota import MyT
from mytoyota.exceptions import ToyotaApiError, ToyotaInternalError, ToyotaLoginError
from mytoyota.models.vehicle import Vehicle

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONF_UNIT_SYSTEM_METRIC,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_UNIT_SYSTEM_IMPERIAL_LITERS,
    CONF_USE_LITERS_PER_100_MILES,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)


class StatisticsData(TypedDict):
    """Representing Statistics data."""

    week: list[dict[str, Any]]
    month: list[dict[str, Any]]
    year: list[dict[str, Any]]


class VehicleData(TypedDict):
    """Representing Vehicle data."""

    data: Vehicle
    statistics: StatisticsData | None


async def with_timeout(task, timeout_seconds=15):
    """Run an async task with a timeout."""
    async with async_timeout.timeout(timeout_seconds):
        return await task


async def async_setup_entry(  # pylint: disable=too-many-statements
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Set up Toyota Connected Services from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    use_liters = entry.options.get(CONF_USE_LITERS_PER_100_MILES, False)

    client = MyT(
        username=email,
        password=password,
        disable_locale_check=True,
    )

    try:
        await client.login()
    except ToyotaLoginError as ex:
        raise ConfigEntryAuthFailed(ex) from ex
    except (httpx.ConnectTimeout, httpcore.ConnectTimeout) as ex:
        raise ConfigEntryNotReady(
            "Unable to connect to Toyota Connected Services"
        ) from ex

    async def async_get_vehicle_data() -> list[VehicleData]:
        """Fetch vehicle data from Toyota API."""

        try:

            vehicles = []

            cars = await with_timeout(client.get_vehicles())

            for car in cars:
                vehicle = await client.get_vehicle_status(car)

                car = VehicleData(data=vehicle, statistics=None)

                if vehicle.is_connected_services_enabled and vehicle.vin is not None:
                    if not vehicle.dashboard.is_metric:
                        _LOGGER.debug("The car is reporting data in imperial")
                        if use_liters:
                            _LOGGER.debug(
                                "Getting statistics in imperial and L/100 miles"
                            )
                            unit = CONF_UNIT_SYSTEM_IMPERIAL_LITERS
                        else:
                            _LOGGER.debug("Getting statistics in imperial and MPG")
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

                    car["statistics"] = StatisticsData(
                        week=data[0], month=data[1], year=data[0]
                    )

                vehicles.append(car)

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
        update_method=async_get_vehicle_data,
        update_interval=timedelta(seconds=120),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
