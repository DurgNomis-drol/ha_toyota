"""Constants for the Toyota Connected Services integration."""

from homeassistant.const import Platform

# PLATFORMS SUPPORTED
PLATFORMS = [Platform.BINARY_SENSOR, Platform.DEVICE_TRACKER, Platform.SENSOR]

# INTEGRATION ATTRIBUTES
DOMAIN = "toyota"
NAME = "Toyota Connected Services"
ISSUES_URL = "https://github.com/DurgNomis-drol/ha_toyota/issues"

# CONF
CONF_BRAND_MAPPING = {"T": "Toyota"}
CONF_METRIC_VALUES = "use_metric_values"

# DEFAULTS
DEFAULT_LOCALE = "en-gb"

# DATA COORDINATOR ATTRIBUTES
BUCKET = "bucket"
DATA = "data"
ENGINE = "engine"
FUEL_TYPE = "fuel"
HYBRID = "hybrid"
LAST_UPDATED = "last_updated"
VIN = "vin"
PERIODE_START = "periode_start"
STATISTICS = "statistics"
WARNING = "warning"

# ICONS
ICON_BATTERY = "mdi:car-battery"
ICON_CAR = "mdi:car-info"
ICON_CAR_DOOR = "mdi:car-door"
ICON_CAR_DOOR_LOCK = "mdi:car-door-lock"
ICON_CAR_LIGHTS = "mdi:car-parking-lights"
ICON_EV = "mdi:car-electric"
ICON_FRONT_DEFOGGER = "mdi:car-defrost-front"
ICON_FUEL = "mdi:gas-station"
ICON_HISTORY = "mdi:history"
ICON_KEY = "mdi:car-key"
ICON_ODOMETER = "mdi:counter"
ICON_PARKING = "mdi:map-marker"
ICON_RANGE = "mdi:map-marker-distance"
ICON_REAR_DEFOGGER = "mdi:car-defrost-rear"

# STARTUP LOG MESSAGE
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUES_URL}
-------------------------------------------------------------------
"""
