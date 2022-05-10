"""Device tracker platform for Toyota Connected Services"""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import VehicleData
from .const import DOMAIN, IMAGE
from .entity import ToyotaBaseEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the Toyota Connected Services tracker from config entry."""
    coordinator: DataUpdateCoordinator[list[VehicleData]] = hass.data[DOMAIN][
        entry.entry_id
    ]

    async_add_devices(
        ToyotaParkingTracker(
            coordinator=coordinator,
            entry_id=entry.entry_id,
            vehicle_index=index,
            description=EntityDescription(
                key="parking_location",
                name="parking location",
            ),
        )
        for index, vehicle in enumerate(coordinator.data)
        if vehicle["data"].is_connected_services_enabled
        and vehicle["data"].parkinglocation
    )


class ToyotaParkingTracker(ToyotaBaseEntity, TrackerEntity):
    """Toyota Connected Services device tracker."""

    coordinator: DataUpdateCoordinator[list[VehicleData]]

    @property
    def latitude(self):
        """Return latitude value of the device."""
        parking = self.coordinator.data[self.index]["data"].parkinglocation
        return parking.latitude if parking else None

    @property
    def longitude(self):
        """Return longitude value of the device."""
        parking = self.coordinator.data[self.index]["data"].parkinglocation
        return parking.longitude if parking else None

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def entity_picture(self):
        """Return entity picture."""
        if IMAGE in self.vehicle.details:
            return self.vehicle.details[IMAGE]
        return None
