"""Constants for the Toyota Connected Services integration."""

DOMAIN = "toyota"
NAME = "Toyota Connected Services"
ISSUES_URL = "https://github.com/DurgNomis-drol/ha_toyota/issues"

DATA_CLIENT = "toyota_client"
DATA_COORDINATOR = "coordinator"

# CONF
CONF_LOCALE = "locale"
CONF_UUID = "uuid"

# COORDINATOR DATA ATTRIBUTES
VEHICLE_INFO = "vehicle_info"
DASHBOARD = "dashboard"
MODEL = "modelName"
NICKNAME = "alias"
VIN = "vin"
ODOMETER = "odometer"
ODOMETER_UNIT = "odometer_unit"
FUEL = "fuel"
FUEL_TYPE = "fuel_type"
PARKING = "parking"
BATTERY = "battery"
HVAC = "hvac"
HVAC_TEMPERATURE = "InsideTemperature"
ENGINE = "engine"
TRANSMISSION = "transmission"
HYBRID = "hybrid"
PRODUCTION_YEAR = "production_year"
LAST_UPDATED = "last_updated"

# ICONS
ICON_CAR = "mdi:car"
ICON_FUEL = "mdi:gas-station"
ICON_ODOMETER = "mdi:speedometer"
ICON_HVAC = "mdi:hvac"
ICON_PARKING = "mdi:map-marker"
ICON_BATTERY = "mdi:car-battery"

# DICT STRUCTURE FOR HOLDING INFORMATION
VEHICLE_DICT_FORMAT = {
    NICKNAME: None,
    DASHBOARD: {
        FUEL: None,
        FUEL_TYPE: None,
        ODOMETER: None,
        ODOMETER_UNIT: None,
    },
    HVAC: {},
    BATTERY: {},
    PARKING: {},
    VEHICLE_INFO: {
        ENGINE: None,
        TRANSMISSION: None,
        HYBRID: None,
        MODEL: None,
        PRODUCTION_YEAR: None,
        VIN: None,
    },
    LAST_UPDATED: None,
}

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUES_URL}
-------------------------------------------------------------------
"""
