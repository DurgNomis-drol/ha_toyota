"""Toyota API module"""
import json
import logging

import aiohttp
from langcodes import Language

# ENDPOINTS
BASE_URL = "https://myt-agg.toyota-europe.com/cma/api"
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
        vin: str,
        locale: str,
        session: aiohttp.ClientSession,
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

        if self.vin_is_valid(vin):
            self._vin = vin
        else:
            raise ToyotaVinNotValid("Please provide a valid vin-number!")

        self.session = session
        self.username = username
        self.password = password
        self._token = token
        self._uuid = uuid

    @staticmethod
    def vin_is_valid(vin: str) -> bool:
        """Is vin number the correct length."""
        return len(vin) == 17

    @staticmethod
    def locale_is_valid(locale: str) -> bool:
        """Is locale string valid."""
        return Language.make(locale).is_valid()

    @staticmethod
    def _create_login_json(username: str, password: str) -> str:
        """Create login json."""
        login_dict = {
            USERNAME: username,
            PASSWORD: password,
        }
        return json.dumps(login_dict)

    async def _request(self, endpoint: str, headers: dict):
        """Make the request."""
        url = BASE_URL + endpoint

        async with self.session.get(url, headers=headers, timeout=TIMEOUT) as response:
            if response.status != HTTP_OK:
                raise ToyotaHttpError(
                    "HTTP error: {} text: {}".format(response.status, response.text)
                )

        return await response.json()

    async def perform_login(self, username: str, password: str) -> tuple:
        """Performs login to toyota servers."""
        headers = {
            "X-TME-BRAND": "TOYOTA",
            "X-TME-LC": self._locale,
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "Content-Type": "application/json;charset=UTF-8",
        }

        async with self.session.post(
            ENDPOINT_AUTH,
            headers=headers,
            json={USERNAME: username, PASSWORD: password},
        ) as response:
            if response.status != HTTP_OK:
                raise ToyotaLoginError(
                    "Login failed, check your credentials! {}".format(response.text)
                )

        result = await response.json()

        token = result.get(TOKEN)
        uuid = result.get(UUID)

        return token, uuid

    async def get_odometer(self) -> tuple:
        """Get information from odometer."""
        odometer = 0
        odometer_unit = ""
        fuel = 0
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}"}
        endpoint = f"/vehicle/{self._vin}/addtionalInfo"

        data = await self._request(endpoint, headers=headers)

        for item in data:
            if item[TYPE] == MILEAGE:
                odometer = item[VALUE]
                odometer_unit = item[UNIT]
            if item[TYPE] == FUEL:
                fuel = item[VALUE]
        return odometer, odometer_unit, fuel

    async def get_parking(self) -> str:
        """Get where you have parked your car."""
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}", "VIN": self._vin}
        endpoint = f"/users/{self._uuid}/vehicle/location"

        parking = await self._request(endpoint, headers=headers)

        return parking

    async def get_vehicle_information(self) -> tuple:
        """Get information about the vehicle."""
        headers = {
            "Cookie": f"iPlanetDirectoryPro={self._token}",
            "uuid": self._uuid,
            "X-TME-LOCALE": self._locale,
        }
        endpoint = f"/vehicles/{self._vin}/remoteControl/status"

        data = await self._request(endpoint, headers=headers)

        last_updated = data[VEHICLE_INFO][ACQUISITIONDATE]
        battery = data[VEHICLE_INFO][CHARGE_INFO]
        hvac = data[VEHICLE_INFO][HVAC]

        return battery, hvac, last_updated


class ToyotaVinNotValid(Exception):
    """Raise if vin is not valid."""


class ToyotaLocaleNotValid(Exception):
    """Raise if locale string is not valid."""


class ToyotaLoginError(Exception):
    """Raise if a login error happens."""


class ToyotaHttpError(Exception):
    """Raise if http error happens."""
