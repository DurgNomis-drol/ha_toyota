"""Constants for the Toyota Connected Services integration."""

DOMAIN = "toyota"
NAME = "Toyota Connected Services"
ISSUES_URL = "https://github.com/DurgNomis-drol/ha_toyota/issues"

DATA_CLIENT = "toyota_client"
DATA_COORDINATOR = "coordinator"

# CONF
CONF_NICKNAME = "nickname"
CONF_VIN = "vin_number"
CONF_LOCALE = "locale"
CONF_UUID = "uuid"

# COORDINATOR DATA ATTRIBUTES
VEHICLE_INFO = "vehicle_info"
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

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUES_URL}
-------------------------------------------------------------------
"""
