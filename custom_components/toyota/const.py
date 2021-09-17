"""Constants for the Toyota Connected Services integration."""

# PLATFORMS SUPPORTED
PLATFORMS = ["binary_sensor", "sensor", "device_tracker"]

# INTEGRATION ATTRIBUTES
DOMAIN = "toyota"
NAME = "Toyota Connected Services"
ISSUES_URL = "https://github.com/DurgNomis-drol/ha_toyota/issues"

# CONF
CONF_REGION_SUPPORTED = [
    "europe",
]
CONF_UNIT_SYSTEM_IMPERIAL_LITERS = "imperial_liters"
CONF_USE_LITERS_PER_100_MILES = "use_liters"

# DEFAULTS
DEFAULT_LOCALE = "en-gb"

# DATA COORDINATOR
DATA_CLIENT = "toyota_client"
DATA_COORDINATOR = "coordinator"

# DATA COORDINATOR ATTRIBUTES
AVERAGE_SPEED = "averageSpeedInKmph"
BATTERY_HEALTH = "batteryHealth"
BUCKET = "bucket"
COACHING_ADVICE = "coachingAdviceMostOccurrence"
DATA = "data"
DRIVER_SCORE = "averageDriverScore"
DRIVER_SCORE_ACCELERATIONS = "averageAccelerationDriverScore"
DRIVER_SCORE_BRAKING = "averageBrakingDriverScore"
ENGINE = "engine"
EV_DISTANCE = "evDistanceInKm"
EV_DURATION = "evDurationInSec"
EV_DISTANCE_PERCENTAGE = "evDistancePercentage"
EV_DURATION_PERCENTAGE = "evDurationPercentage"
FUEL_CONSUMED = "totalFuelConsumedInL"
FUEL_TYPE = "fuel"
HARD_ACCELERATION = "hardAccelerationCount"
HARD_BRAKING = "hardBrakingCount"
HIGHWAY_DISTANCE = "highwayDistanceInKm"
HIGHWAY_DISTANCE_PERCENTAGE = "highwayDistancePercentage"
HYBRID = "hybrid"
IMAGE = "imageUrl"
LAST_UPDATED = "last_updated"
LICENSE_PLATE = "licensePlate"
MAX_SPEED = "maxSpeedInKmph"
MODEL = "modelName"
NIGHT_TRIPS = "nightTripsCount"
PERIODE_START = "periode_start"
STATISTICS = "statistics"
TOTAL_DURATION = "totalDurationInSec"
TOTAL_DISTANCE = "totalDistanceInKm"
TRIPS = "tripCount"
WARNING = "warning"

# ICONS
ICON_BATTERY = "mdi:car-battery"
ICON_CAR = "mdi:car-info"
ICON_CAR_DOOR = "mdi:car-door"
ICON_CAR_DOOR_LOCK = "mdi:car-door-lock"
ICON_CAR_LIGHTS = "mdi:car-parking-lights"
ICON_FUEL = "mdi:gas-station"
ICON_HISTORY = "mdi:history"
ICON_KEY = "mdi:car-key"
ICON_ODOMETER = "mdi:counter"
ICON_PARKING = "mdi:map-marker"

# STARTUP LOG MESSAGE
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUES_URL}
-------------------------------------------------------------------
"""
