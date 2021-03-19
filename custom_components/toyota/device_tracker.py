"""Device tracker for Toyota Connected Services"""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from . import ToyotaEntity
from .const import DATA_COORDINATOR, DOMAIN, ICON_CAR, PARKING, STATUS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the BMW ConnectedDrive tracker from config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    tracker = []

    def check_if_enabled(service):
        """Check if Toyota Connected Services is enabled for the car."""
        if "error" in service:
            return False

        return True

    for index, _ in enumerate(coordinator.data):
        if check_if_enabled(coordinator.data[index][STATUS][PARKING]):
            tracker.append(ToyotaParkingTracker(coordinator, index))

    async_add_devices(tracker, True)


class ToyotaParkingTracker(ToyotaEntity, TrackerEntity):
    """BMW Connected Drive device tracker."""

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return float(self.coordinator.data[self.index][STATUS][PARKING]["event"]["lat"])

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return float(self.coordinator.data[self.index][STATUS][PARKING]["event"]["lon"])

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias}"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/last_parked"

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON_CAR

    @property
    def force_update(self):
        """All updates do not need to be written to the state machine."""
        return False
