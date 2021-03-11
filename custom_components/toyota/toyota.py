"""Toyota API module"""
import requests
import logging

from langcodes import Language

# ENDPOINTS
BASE_URL = "https://myt-agg.toyota-europe.com/cma/api"
ENDPOINT_AUTH = 'https://ssoms.toyota-europe.com/authenticate'

# HEADERS
LOGIN_BASE_HEADERS = {'X-TME-BRAND': 'TOYOTA', 'Accept': 'application/json, text/plain, */*', 'Sec-Fetch-Dest': 'empty'}
TRIPS_BASE_HEADER = {'X-TME-TOKEN': None}

TIMEOUT = 10

# LOGIN
USERNAME = 'username'
PASSWORD = 'password'

# JSON ATTRIBUTES
VIN = 'vin'
TOKEN = 'token'
UUID = 'uuid'
CUSTOMERPROFILE = 'customerProfile'
FUEL = "fuel"
MILEAGE = "mileage"
TYPE = 'type'
VALUE = 'value'
UNIT = 'unit'
VEHICLE_INFO = 'VehicleInfo'
ACQUISITIONDATE = 'AcquisitionDatetime'
CHARGE_INFO = 'ChargeInfo'
HVAC = 'RemoteHvacInfo'

# HTTP
HTTP_OK = 200

# LOGGER
_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:

    def __init__(
        self,
        vin: str,
        locale: str,
        uuid: str = None,
        username: str = None,
        password: str = None,
        token: str = None
    ) -> None:
        """Toyota API"""

        if self.locale_is_valid(locale):
            self._locale = locale
        else:
            _LOGGER.error("Please provide a valid locale string! Valid format is: en-gb.")

        if self.vin_is_valid(vin):
            self._vin = vin
        else:
            _LOGGER.error("Please provide a valid vin-number!")

        if token is None or uuid is None:
            token, uuid = self.authenticate(username, password)
            self.token = token
            self.uuid = uuid
        else:
            self.token = token
            self.uuid = uuid

    @staticmethod
    def vin_is_valid(vin: str) -> bool:
        return len(vin) == 17

    @staticmethod
    def locale_is_valid(locale: str) -> bool:
        return Language.make(locale).is_valid()

    @staticmethod
    def create_login_json(username: str, password: str, vin: str) -> dict:
        login = {
            USERNAME: username,
            PASSWORD: password,
            VIN: vin,
        }
        return login

    @staticmethod
    def request(endpoint: str, headers: dict):

        url = BASE_URL + endpoint

        response = requests.get(
            url,
            headers=headers,
            timeout=TIMEOUT
        )

        if response.status_code != HTTP_OK:
            _LOGGER.error('HTTP error: {} text: {}'.format(response.status_code, response.text))
            return False

        return response.json()

    def authenticate(self, username: str, password: str):
        headers = LOGIN_BASE_HEADERS
        headers.update({'X-TME-LC': self._locale})

        response = requests.post(
            ENDPOINT_AUTH,
            headers=headers,
            timeout=TIMEOUT,
            json=self.create_login_json(username, password, self._vin)
        )

        if response.status_code != HTTP_OK:
            _LOGGER.error('Login failed, check your credentials! {}'.format(response.text))
            return False

        result = response.json()

        token = result.get(TOKEN)
        uuid = result.get(UUID)

        return token, uuid

    async def get_odometer(self) -> tuple:

        odometer = 0
        odometer_unit = ''
        fuel = 0
        headers = {'Cookie': f'iPlanetDirectoryPro={self._token}'}
        endpoint = f'/vehicle/{self._vin}/addtionalInfo'

        data = self.request(
            endpoint,
            headers=headers
        )

        for item in data:
            if item[TYPE] == MILEAGE:
                odometer = item[VALUE]
                odometer_unit = item[UNIT]
            if item[TYPE] == FUEL:
                fuel = item[VALUE]
        return odometer, odometer_unit, fuel

    async def get_parking(self) -> str:

        headers = {'Cookie': f'iPlanetDirectoryPro={self._token}', 'VIN': self._vin}
        endpoint = f'/users/{self._uuid}/vehicle/location'

        parking = self.request(
            endpoint,
            headers=headers
        )

        return parking

    async def get_vehicle_information(self) -> tuple:

        headers = {'Cookie': f'iPlanetDirectoryPro={self._token}', 'uuid': self._uuid, 'X-TME-LOCALE': self._locale}
        endpoint = f'/vehicles/{self._vin}/remoteControl/status'

        data = self.request(
            endpoint,
            headers=headers
        )

        last_updated = data[VEHICLE_INFO][ACQUISITIONDATE]
        battery = data[VEHICLE_INFO][CHARGE_INFO]
        hvac = data[VEHICLE_INFO][HVAC]

        return battery, hvac, last_updated
