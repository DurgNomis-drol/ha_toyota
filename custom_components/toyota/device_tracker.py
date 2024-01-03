"""Device tracker platform for Toyota Connected Services."""

from typing import Optional

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import VehicleData
from .const import DOMAIN, ICON_PARKING
from .entity import ToyotaBaseEntity

PARKING_TRACKER_DESCRIPTION: EntityDescription = EntityDescription(
    key="parking_location",
    translation_key="parking_location",
    icon=ICON_PARKING,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the Toyota Connected Services tracker from config entry."""
    coordinator: DataUpdateCoordinator[list[VehicleData]] = hass.data[DOMAIN][entry.entry_id]

    async_add_devices(
        ToyotaParkingTracker(
            coordinator=coordinator,
            entry_id=entry.entry_id,
            vehicle_index=index,
            description=PARKING_TRACKER_DESCRIPTION,
        )
        for index, vehicle in enumerate(coordinator.data)
        if vehicle["data"].location
    )


class ToyotaParkingTracker(ToyotaBaseEntity, TrackerEntity):
    """Toyota Connected Services device tracker."""

    coordinator: DataUpdateCoordinator[list[VehicleData]]

    @property
    def latitude(self) -> Optional[float]:
        """Return latitude value of the device."""
        location = self.vehicle.location
        return location.latitude if location else None

    @property
    def longitude(self) -> Optional[float]:
        """Return longitude value of the device."""
        location = self.vehicle.location
        return location.longitude if location else None

    @property
    def source_type(self) -> str:
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def entity_picture(self) -> Optional[str]:
        """Return entity picture."""
        return self.vehicle._vehicle_info.image
