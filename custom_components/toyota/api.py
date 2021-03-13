"""API for Toyota Connected Services integration."""
import logging

import aiohttp
import async_timeout

from .const import (
    BATTERY,
    ENGINE,
    FUEL,
    FUEL_TYPE,
    HVAC,
    HYBRID,
    LAST_UPDATED,
    MODEL,
    NICKNAME,
    ODOMETER,
    ODOMETER_UNIT,
    PARKING,
    PRODUCTION_YEAR,
    TRANSMISSION,
    VEHICLE_INFO,
    VIN,
)
from .toyota import MyT, ToyotaHttpError, ToyotaNoCarError

# from homeassistant.util.async_ import gather_with_concurrency


_LOGGER = logging.getLogger(__name__)


class ToyotaApi:
    """Toyota API"""

    def __init__(
        self,
        username: str,
        password: str,
        locale: str,
        session: aiohttp.ClientSession,
        uuid: str = None,
        token: str = None,
    ) -> None:
        self.username = username
        self.password = password
        self.locale = locale
        self.uuid = uuid
        self.token = token
        self.session = session
        self.client = MyT(
            username=self.username,
            password=self.password,
            locale=self.locale,
            token=self.token,
            uuid=self.uuid,
            session=self.session,
        )

    async def get_token_and_uuid(self):
        """Tests if your credentials are valid."""
        token, uuid = self.client.perform_login(
            username=self.username, password=self.password
        )

        if token and uuid:
            return True, token, uuid

        return False, None, None

    async def get_cars(self):
        """Retrieve list of cars"""
        return await self.client.get_cars()

    async def gather_information(self):
        """Gather information from different endpoints and collect it."""
        vehicles = []

        async def with_timeout(task):
            async with async_timeout.timeout(10):
                return await task

        cars = await with_timeout(self.client.get_cars())

        for car in cars:
            vehicle = {
                NICKNAME: car[NICKNAME],
                MODEL: car[MODEL],
                VIN: car[VIN],
                HYBRID: car[HYBRID],
                PRODUCTION_YEAR: car["productionYear"],
                FUEL_TYPE: car[FUEL],
                ENGINE: car[ENGINE],
                TRANSMISSION: car[TRANSMISSION],
            }
            try:
                odometer, odometer_unit, fuel = await with_timeout(
                    self.client.get_odometer(car[VIN])
                )

                parking = await with_timeout(self.client.get_parking(car[VIN]))

                battery, hvac, last_updated = await with_timeout(
                    self.client.get_vehicle_information(car[VIN])
                )

                vehicle.update(
                    {
                        LAST_UPDATED: last_updated,
                        PARKING: parking["event"],
                        VEHICLE_INFO: {
                            ODOMETER: odometer,
                            ODOMETER_UNIT: odometer_unit,
                            FUEL: fuel,
                            BATTERY: battery,
                            HVAC: hvac,
                        },
                    }
                )

            except ToyotaNoCarError as ex:
                _LOGGER.error(ex)
            except ToyotaHttpError as ex:
                _LOGGER.error(ex)
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    "An unknown error occurred: %s",
                    ex,
                )
            finally:
                vehicles.append(vehicle)

        _LOGGER.debug("Vehicles: %s", vehicles)
        return vehicles
