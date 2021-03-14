"""API for Toyota Connected Services integration."""
from asyncio import gather
import logging

import aiohttp
import async_timeout

from .const import (
    BATTERY,
    DASHBOARD,
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
    VEHICLE_DICT_FORMAT,
    VEHICLE_INFO,
    VIN,
)
from .toyota import MyT, ToyotaHttpError, ToyotaNoCarError

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

    async def get_car_data(self, car):
        """Gather information from different endpoints and format it."""

        async def with_timeout(task):
            async with async_timeout.timeout(10):
                return await task

        # GET PREDEFINED DICT FORMAT
        vehicle = VEHICLE_DICT_FORMAT

        # ALIAS
        vehicle[NICKNAME] = car[NICKNAME]

        # DASHBOARD
        vehicle[DASHBOARD].update(
            {
                FUEL_TYPE: car[FUEL],
            }
        )

        # VEHICLE INFORMATION
        vehicle[VEHICLE_INFO].update(
            {
                ENGINE: car[ENGINE],
                TRANSMISSION: car[TRANSMISSION],
                MODEL: car[MODEL],
                VIN: car[VIN],
                HYBRID: car[HYBRID],
                PRODUCTION_YEAR: car["productionYear"],
            }
        )

        try:
            odometer, odometer_unit, fuel = await with_timeout(
                self.client.get_odometer(car[VIN])
            )

            parking = await with_timeout(self.client.get_parking(car[VIN]))

            battery, hvac, last_updated = await with_timeout(
                self.client.get_vehicle_information(car[VIN])
            )

            vehicle[LAST_UPDATED] = last_updated
            vehicle[PARKING] = parking["event"]
            vehicle[HVAC] = hvac
            vehicle[BATTERY] = battery

            vehicle[DASHBOARD].update(
                {
                    ODOMETER: odometer,
                    ODOMETER_UNIT: odometer_unit,
                    FUEL: fuel,
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
            return vehicle

    async def gather_information(self):
        """Gather information from all cars registered to the account."""

        valid, cars = await self.get_cars()

        if valid:
            vehicles = await gather(*[self.get_car_data(car) for car in cars])

            _LOGGER.debug("Vehicles: %s", vehicles)
            return vehicles

        _LOGGER.error("Cannot find any cars in your account.")
