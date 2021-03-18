"""Constants for the Toyota Connected Services integration."""

DOMAIN = "toyota"
NAME = "Toyota Connected Services"
ISSUES_URL = "https://github.com/DurgNomis-drol/ha_toyota/issues"

DATA_CLIENT = "toyota_client"
DATA_COORDINATOR = "coordinator"

# CONF
CONF_LOCALE = "locale"
CONF_UUID = "uuid"
CONF_REGION_SUPPORTED = [
    "Europe",
]

# COORDINATOR DATA ATTRIBUTES
DETAILS = "details"
MODEL = "model"
ALIAS = "alias"
VIN = "vin"
STATUS = "status"
ODOMETER = "odometer"
MILEAGE = "mileage"
MILEAGE_UNIT = "mileage_unit"
FUEL = "Fuel"
FUEL_TYPE = "fuel_type"
PARKING = "parking"
BATTERY = "battery"
HVAC = "hvac"
HVAC_TEMPERATURE = "InsideTemperature"
HYBRID = "hybrid"
LAST_UPDATED = "last_updated"
IMAGE = "image"

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
