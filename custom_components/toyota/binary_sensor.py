"""Binary sensor platform for Toyota integration."""


from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from mytoyota.models.vehicle import Vehicle

from . import VehicleData
from .const import DOMAIN, LAST_UPDATED
from .entity import ToyotaBaseEntity


@dataclass
class ToyotaBinaryEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Vehicle], Optional[bool]]
    attributes_fn: Callable[[Vehicle], Optional[dict[str, Any]]]


@dataclass
class ToyotaBinaryEntityDescription(BinarySensorEntityDescription, ToyotaBinaryEntityDescriptionMixin):
    """Describes a Toyota binary entity."""


HOOD_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="hood",
    translation_key="hood",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.DOOR,
    value_fn=lambda vehicle: not vehicle.lock_status.hood.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

FRONT_DRIVER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="driverseat_lock",
    translation_key="driverseat_lock",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.LOCK,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.driver_seat.locked,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

FRONT_DRIVER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="driverseat_door",
    translation_key="driverseat_door",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.DOOR,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.driver_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

FRONT_DRIVER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="driverseat_window",
    translation_key="driverseat_window",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.WINDOW,
    value_fn=lambda vehicle: not vehicle.lock_status.windows.driver_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

FRONT_PASSENGER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="passengerseat_lock",
    translation_key="passengerseat_lock",
    icon="mdi:car-door-lock",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.LOCK,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.passenger_seat.locked,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

FRONT_PASSENGER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="passengerseat_door",
    translation_key="passengerseat_door",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.DOOR,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.passenger_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

FRONT_PASSENGER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="passengerseat_window",
    translation_key="passengerseat_window",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.WINDOW,
    value_fn=lambda vehicle: not vehicle.lock_status.windows.passenger_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

REAR_DRIVER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="leftrearseat_lock",
    translation_key="leftrearseat_lock",
    icon="mdi:car-door-lock",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.LOCK,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.driver_rear_seat.locked,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

REAR_DRIVER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="leftrearseat_door",
    translation_key="leftrearseat_door",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.DOOR,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.driver_rear_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

REAR_DRIVER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="leftrearseat_window",
    translation_key="leftrearseat_window",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.WINDOW,
    value_fn=lambda vehicle: not vehicle.lock_status.windows.driver_rear_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

REAR_PASSENGER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="rightrearseat_lock",
    translation_key="rightrearseat_lock",
    icon="mdi:car-door-lock",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.LOCK,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.passenger_seat.locked,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

REAR_PASSENGER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="rightrearseat_door",
    translation_key="rightrearseat_door",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.DOOR,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.passenger_rear_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

REAR_PASSENGER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="rightrearseat_window",
    translation_key="rightrearseat_window",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.WINDOW,
    value_fn=lambda vehicle: not vehicle.lock_status.windows.passenger_rear_seat.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

TRUNK_DOOR_LOCK_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="trunk_lock",
    translation_key="trunk_lock",
    icon="mdi:car-door-lock",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.LOCK,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.trunk.locked,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)

TRUNK_DOOR_OPEN_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="trunk_door",
    translation_key="trunk_door",
    icon="mdi:car-door",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=BinarySensorDeviceClass.WINDOW,
    value_fn=lambda vehicle: not vehicle.lock_status.doors.trunk.closed,
    attributes_fn=lambda vehicle: {
        LAST_UPDATED: vehicle.lock_status.last_updated,
    },
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator: DataUpdateCoordinator[list[VehicleData]] = hass.data[DOMAIN][entry.entry_id]

    binary_sensors: list[ToyotaBinarySensor] = []
    for index, _ in enumerate(coordinator.data):
        vehicle = coordinator.data[index]["data"]
        capabilities_descriptions = [
            (
                vehicle._vehicle_info.extended_capabilities.bonnet_status,
                HOOD_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.front_driver_door_lock_status,
                FRONT_DRIVER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.front_driver_door_open_status,
                FRONT_DRIVER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.front_driver_door_window_status,
                FRONT_DRIVER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.front_passenger_door_lock_status,
                FRONT_PASSENGER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.front_passenger_door_open_status,
                FRONT_PASSENGER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.front_passenger_door_window_status,
                FRONT_PASSENGER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.rear_driver_door_lock_status,
                REAR_DRIVER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.rear_driver_door_open_status,
                REAR_DRIVER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.rear_driver_door_window_status,
                REAR_DRIVER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.rear_passenger_door_lock_status,
                REAR_PASSENGER_DOOR_LOCK_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.rear_passenger_door_open_status,
                REAR_PASSENGER_DOOR_OPEN_STATUS_ENTITY_DESCRIPTION,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.rear_passenger_door_window_status,
                REAR_PASSENGER_DOOR_WINDOW_STATUS_ENTITY_DESCRIPTION,
            ),
        ]

        for capability, description in capabilities_descriptions:
            if capability:
                binary_sensors.append(
                    ToyotaBinarySensor(
                        coordinator=coordinator,
                        entry_id=entry.entry_id,
                        vehicle_index=index,
                        description=description,
                    )
                )

        # TODO: Find matching capabilities in _vehicle_info
        binary_sensors.append(
            ToyotaBinarySensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=TRUNK_DOOR_LOCK_ENTITY_DESCRIPTION,
            )
        )
        binary_sensors.append(
            ToyotaBinarySensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=TRUNK_DOOR_OPEN_ENTITY_DESCRIPTION,
            )
        )

    async_add_devices(binary_sensors, True)


class ToyotaBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Representation of a Toyota binary sensor."""

    @property
    def is_on(self) -> Optional[bool]:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.vehicle)

    @property
    def extra_state_attributes(self) -> Optional[dict[str, Any]]:
        """Return the attributes of the sensor."""
        return self.entity_description.attributes_fn(self.vehicle)
