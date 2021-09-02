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
AVERAGE_SPEED = "averageSpeedInKmph"
BATTERY_HEALTH = "batteryHealth"
BUCKET = "bucket"
CONNECTED_SERVICES = "connectedServices"
DATA = "data"
MONTHLY = "monthly"
WEEKLY = "weekly"
YEARLY = "yearly"
DETAILS = "details"
ENGINE = "engine"
EV_DISTANCE = "evDistanceInKm"
EV_DISTANCE_PERCENTAGE = "evDistancePercentage"
FUEL = "Fuel"
FUEL_CONSUMED = "totalFuelConsumedInL"
FUEL_TYPE = "fuel"
HYBRID = "hybrid"
IMAGE = "imageUrl"
LICENSE_PLATE = "licensePlate"
MAX_SPEED = "maxSpeedInKmph"
MILEAGE = "mileage"
MILEAGE_UNIT = "mileage_unit"
MODEL = "modelName"
NIGHT_TRIPS = "nightTripsCount"
ODOMETER = "odometer"
PARKING = "parking"
PERIODE_START = "periode_start"
SERVICES = "servicesEnabled"
STATISTICS = "statistics"
STATUS = "status"
TOTAL_DURATION = "totalDurationInSec"
TOTAL_DISTANCE = "totalDistanceInKm"
TRIPS = "tripCount"
VIN = "vin"

# ICONS
ICON_BATTERY = "mdi:car-battery"
ICON_CAR = "mdi:car"
ICON_FUEL = "mdi:gas-station"
ICON_ODOMETER = "mdi:counter"
ICON_PARKING = "mdi:map-marker"
ICON_HISTORY = "mdi:history"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUES_URL}
-------------------------------------------------------------------
"""
