"""Toyota integration."""
from __future__ import annotations

import asyncio
import asyncio.exceptions as asyncioexceptions
import logging
from datetime import timedelta
from typing import Optional, TypedDict

import httpcore
import httpx
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from mytoyota import MyT
from mytoyota.exceptions import ToyotaApiError, ToyotaInternalError, ToyotaLoginError
from mytoyota.models.summary import Summary
from mytoyota.models.vehicle import Vehicle

from .const import CONF_METRIC_VALUES, DOMAIN, PLATFORMS, STARTUP_MESSAGE

_LOGGER = logging.getLogger(__name__)


class StatisticsData(TypedDict):
    """Representing Statistics data."""

    day: Optional[Summary]
    week: Optional[Summary]
    month: Optional[Summary]
    year: Optional[Summary]


class VehicleData(TypedDict):
    """Representing Vehicle data."""

    data: Vehicle
    statistics: Optional[StatisticsData]
    metric_values: bool


async def async_setup_entry(  # pylint: disable=too-many-statements
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Set up Toyota Connected Services from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    use_metric_values = entry.data[CONF_METRIC_VALUES]

    client = MyT(
        username=email,
        password=password,
    )

    try:
        await client.login()
    except ToyotaLoginError as ex:
        raise ConfigEntryAuthFailed(ex) from ex
    except (httpx.ConnectTimeout, httpcore.ConnectTimeout) as ex:
        raise ConfigEntryNotReady("Unable to connect to Toyota Connected Services") from ex

    async def async_get_vehicle_data() -> Optional[list[VehicleData]]:
        """Fetch vehicle data from Toyota API."""
        try:
            vehicles = await asyncio.wait_for(client.get_vehicles(metric=use_metric_values), 15)
            vehicle_informations: list[VehicleData] = []
            if vehicles is not None:
                for vehicle in vehicles:
                    await vehicle.update()
                    vehicle_data = VehicleData(
                        data=vehicle, statistics=None, metric_values=use_metric_values
                    )

                    if vehicle.vin is not None:
                        # Use parallel request to get car statistics.
                        driving_statistics = await asyncio.gather(
                            vehicle.get_current_day_summary(),
                            vehicle.get_current_week_summary(),
                            vehicle.get_current_month_summary(),
                            vehicle.get_current_year_summary(),
                        )

                        vehicle_data["statistics"] = StatisticsData(
                            day=driving_statistics[0],
                            week=driving_statistics[1],
                            month=driving_statistics[2],
                            year=driving_statistics[3],
                        )

                    vehicle_informations.append(vehicle_data)

                _LOGGER.debug(vehicle_informations)
                return vehicle_informations

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
                "Update canceled! Toyota's API was too slow to respond. Will try again later..."
            ) from ex
        return None

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_get_vehicle_data,
        update_interval=timedelta(seconds=360),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
