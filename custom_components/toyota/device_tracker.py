"""Device tracker for Toyota Connected Services"""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.const import STATE_UNAVAILABLE

from .const import (
    CONNECTED_SERVICES,
    DATA_COORDINATOR,
    DETAILS,
    DOMAIN,
    ICON_CAR,
    IMAGE,
    PARKING,
    SERVICES,
    STATUS,
)
from .entity import ToyotaBaseEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the BMW ConnectedDrive tracker from config entry."""
    tracker = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):
        if coordinator.data[index][SERVICES][CONNECTED_SERVICES]:
            tracker.append(ToyotaParkingTracker(coordinator, index, "parking location"))

    async_add_devices(tracker, True)


class ToyotaParkingTracker(ToyotaBaseEntity, TrackerEntity):
    """BMW Connected Drive device tracker."""

    _attr_force_update = False
    _attr_icon = ICON_CAR

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return (
            float(self.coordinator.data[self.index][STATUS][PARKING]["event"]["lat"])
            if self.coordinator.data[self.index][STATUS][PARKING]
            else STATE_UNAVAILABLE
        )

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return (
            float(self.coordinator.data[self.index][STATUS][PARKING]["event"]["lon"])
            if self.coordinator.data[self.index][STATUS][PARKING]
            else STATE_UNAVAILABLE
        )

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def entity_picture(self):
        """Return entity picture."""
        return self.coordinator.data[self.index][DETAILS][IMAGE]
