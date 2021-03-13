"""Toyota API module"""
import logging

import aiohttp
from langcodes import Language
import requests

# ENDPOINTS
BASE_URL = "https://myt-agg.toyota-europe.com/cma/api"
BASE_URL_CARS = "https://cpb2cs.toyota-europe.com/vehicle"
ENDPOINT_AUTH = "https://ssoms.toyota-europe.com/authenticate"

TIMEOUT = 10

# LOGIN
USERNAME = "username"
PASSWORD = "password"

# JSON ATTRIBUTES
VIN = "vin"
TOKEN = "token"
UUID = "uuid"
CUSTOMERPROFILE = "customerProfile"
FUEL = "fuel"
MILEAGE = "mileage"
TYPE = "type"
VALUE = "value"
UNIT = "unit"
VEHICLE_INFO = "VehicleInfo"
ACQUISITIONDATE = "AcquisitionDatetime"
CHARGE_INFO = "ChargeInfo"
HVAC = "RemoteHvacInfo"

# HTTP
HTTP_OK = 200

# LOGGER
_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services API class."""

    def __init__(
        self,
        locale: str,
        session: aiohttp.ClientSession = None,
        uuid: str = None,
        username: str = None,
        password: str = None,
        token: str = None,
    ) -> None:
        """Toyota API"""
        if self.locale_is_valid(locale):
            self._locale = locale
        else:
            raise ToyotaLocaleNotValid(
                "Please provide a valid locale string! Valid format is: en-gb."
            )

        self.session = session
        self.username = username
        self.password = password
        self._token = token
        self._uuid = uuid

    @staticmethod
    def locale_is_valid(locale: str) -> bool:
        """Is locale string valid."""
        return Language.make(locale).is_valid()

    async def _request(self, endpoint: str, headers: dict):
        """Make the request."""

        async with self.session.get(
            endpoint, headers=headers, timeout=TIMEOUT
        ) as response:
            if response.status == HTTP_OK:
                resp = await response.json()
            elif response.status == 204:
                raise ToyotaNoCarError("Please setup connected services for your car!")
            else:
                raise ToyotaHttpError(
                    "HTTP: {} - {}".format(response.status, response.text)
                )

        return await resp

    def perform_login(self, username: str, password: str) -> tuple:
        """Performs login to toyota servers."""
        headers = {
            "X-TME-BRAND": "TOYOTA",
            "X-TME-LC": self._locale,
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "Content-Type": "application/json;charset=UTF-8",
        }

        response = requests.post(
            ENDPOINT_AUTH,
            headers=headers,
            json={USERNAME: username, PASSWORD: password},
        )
        if response.status_code != HTTP_OK:
            raise ToyotaLoginError(
                "Login failed, check your credentials! {}".format(response.text)
            )

        result = response.json()

        token = result.get(TOKEN)
        uuid = result[CUSTOMERPROFILE][UUID]

        return token, uuid

    async def get_cars(self) -> list:
        """Retrieves list of cars you have registered with MyT"""
        headers = {
            "X-TME-BRAND": "TOYOTA",
            "X-TME-LC": self._locale,
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "X-TME-TOKEN": self._token,
        }

        endpoint = (
            f"{BASE_URL_CARS}/user/{self._uuid}/vehicles?services=uio&legacy=true"
        )

        cars = await self._request(endpoint, headers=headers)

        return cars

    async def get_odometer(self, vin: str) -> tuple:
        """Get information from odometer."""
        odometer = 0
        odometer_unit = ""
        fuel = 0
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}"}
        endpoint = f"{BASE_URL}/vehicle/{vin}/addtionalInfo"

        data = await self._request(endpoint, headers=headers)

        for item in data:
            if item[TYPE] == MILEAGE:
                odometer = item[VALUE]
                odometer_unit = item[UNIT]
            if item[TYPE] == FUEL:
                fuel = item[VALUE]
        return odometer, odometer_unit, fuel

    async def get_parking(self, vin: str) -> dict:
        """Get where you have parked your car."""
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}", "VIN": vin}
        endpoint = f"{BASE_URL}/users/{self._uuid}/vehicle/location"

        parking = await self._request(endpoint, headers=headers)

        return parking

    async def get_vehicle_information(self, vin: str) -> tuple:
        """Get information about the vehicle."""
        headers = {
            "Cookie": f"iPlanetDirectoryPro={self._token}",
            "uuid": self._uuid,
            "X-TME-LOCALE": self._locale,
        }
        endpoint = f"{BASE_URL}/vehicles/{vin}/remoteControl/status"

        data = await self._request(endpoint, headers=headers)

        last_updated = data[VEHICLE_INFO][ACQUISITIONDATE]
        battery = data[VEHICLE_INFO][CHARGE_INFO]
        hvac = data[VEHICLE_INFO][HVAC]

        return battery, hvac, last_updated


class ToyotaLocaleNotValid(Exception):
    """Raise if locale string is not valid."""


class ToyotaLoginError(Exception):
    """Raise if a login error happens."""


class ToyotaHttpError(Exception):
    """Raise if http error happens."""


class ToyotaNoCarError(Exception):
    """Raise if 205 is returned (Means no car found)."""
