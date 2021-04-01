"""Constants for the Toyota Connected Services integration."""

PLATFORMS = ["sensor", "device_tracker"]

DOMAIN = "toyota"
NAME = "Toyota Connected Services"
ISSUES_URL = "https://github.com/DurgNomis-drol/ha_toyota/issues"

# CONF
CONF_LOCALE = "locale"
CONF_REGION_SUPPORTED = [
    "europe",
]

# DATA COORDINATOR
DATA_CLIENT = "toyota_client"
DATA_COORDINATOR = "coordinator"

# DATA COORDINATOR ATTRIBUTES
ALIAS = "alias"
BATTERY_HEALTH = "batteryHealth"
CONNECTED_SERVICES = "connectedServices"
DETAILS = "details"
ENGINE = "engine"
FUEL = "Fuel"
FUEL_TYPE = "fuel"
HYBRID = "hybrid"
IMAGE = "imageUrl"
LICENSE_PLATE = "licensePlate"
MILEAGE = "mileage"
MILEAGE_UNIT = "mileage_unit"
MODEL = "modelName"
ODOMETER = "odometer"
PARKING = "parking"
STATUS = "status"
SERVICES = "servicesEnabled"
VIN = "vin"

# ICONS
ICON_BATTERY = "mdi:car-battery"
ICON_CAR = "mdi:car"
ICON_FUEL = "mdi:gas-station"
ICON_ODOMETER = "mdi:counter"
ICON_PARKING = "mdi:map-marker"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUES_URL}
-------------------------------------------------------------------
"""
