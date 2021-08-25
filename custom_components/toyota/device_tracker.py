"""Device tracker platform for Toyota Connected Services"""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from .const import (
    CONNECTED_SERVICES,
    DATA_COORDINATOR,
    DETAILS,
    DOMAIN,
    IMAGE,
    PARKING,
    SERVICES,
    STATUS,
)
from .entity import ToyotaBaseEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the Toyota Connected Services tracker from config entry."""
    tracker = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):
        if coordinator.data[index][SERVICES][CONNECTED_SERVICES]:
            tracker.append(ToyotaParkingTracker(coordinator, index, "parking location"))

    async_add_devices(tracker, True)


class ToyotaParkingTracker(ToyotaBaseEntity, TrackerEntity):
    """Toyota Connected Services device tracker."""

    @property
    def latitude(self):
        """Return latitude value of the device."""
        if PARKING in self.coordinator.data[self.index][STATUS]:
            return float(
                self.coordinator.data[self.index][STATUS][PARKING]["event"]["lat"]
            )
        return None

    @property
    def longitude(self):
        """Return longitude value of the device."""
        if PARKING in self.coordinator.data[self.index][STATUS]:
            return float(
                self.coordinator.data[self.index][STATUS][PARKING]["event"]["lon"]
            )
        return None

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def entity_picture(self):
        """Return entity picture."""
        if IMAGE in self.coordinator.data[self.index][DETAILS]:
            return self.coordinator.data[self.index][DETAILS][IMAGE]
        return None
