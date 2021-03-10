"""Toyota API module"""
import requests
import logging

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

    def __init__(self, vin, locale, uuid=None, username=None, password=None, token=None):
        self._username = username
        self._password = password
        self._vin = vin
        self._locale = locale

        if token is None or uuid is None:
            token, uuid = self.authenticate()
            self._token = token
            self._uuid = uuid
        else:
            self._uuid = uuid
            self._token = token

    @staticmethod
    def _create_login_json(username, password, vin):
        login = {
            USERNAME: username,
            PASSWORD: password,
            VIN: vin,
        }
        return login

    @staticmethod
    def request(endpoint, headers):

        url = BASE_URL + endpoint

        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code != HTTP_OK:
            _LOGGER.error('HTTP error: {} text: {}'.format(response.status_code, response.text))
            return

        return response.json()

    def authenticate(self):
        headers = LOGIN_BASE_HEADERS
        headers.update({'X-TME-LC': self._locale})

        response = requests.post(ENDPOINT_AUTH, headers=headers, timeout=TIMEOUT, json=self._create_login_json(self._username, self._password, self._vin))

        if response.status_code != HTTP_OK:
            _LOGGER.error('Login failed, check your credentials! {}'.format(response.text))
            return

        result = response.json()

        token = result.get(TOKEN)
        uuid = result.get(UUID)

        return token, uuid

    def get_odometer(self):

        headers = {'Cookie': f'iPlanetDirectoryPro={self._token}'}
        endpoint = f'/vehicle/{self._vin}/addtionalInfo'

        data = self.request(endpoint, headers=headers)

        odometer = 0
        odometer_unit = ''
        fuel = 0
        for item in data:
            if item[TYPE] == 'mileage':
                odometer = item[VALUE]
                odometer_unit = item[UNIT]
            if item[TYPE] == 'Fuel':
                fuel = item[VALUE]
        return odometer, odometer_unit, fuel

    def get_parking(self):

        headers = {'Cookie': f'iPlanetDirectoryPro={self._token}', 'VIN': self._vin}
        endpoint = f'/users/{self._uuid}/vehicle/location'

        parking = self.request(endpoint, headers=headers)

        return parking

    def get_vehicle_information(self):

        headers = {'Cookie': f'iPlanetDirectoryPro={self._token}', 'uuid': self._uuid, 'X-TME-LOCALE': self._locale}
        endpoint = f'/vehicles/{self._vin}/remoteControl/status'

        data = self.request(endpoint, headers=headers)

        last_updated = data[VEHICLE_INFO][ACQUISITIONDATE]
        battery = data[VEHICLE_INFO][CHARGE_INFO]
        hvac = data[VEHICLE_INFO][HVAC]

        return battery, hvac, last_updated
