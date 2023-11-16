"""Binary sensor platform for Toyota integration"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory, EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from mytoyota.models.vehicle import Vehicle

from . import VehicleData
from .const import DOMAIN, LAST_UPDATED, WARNING
from .entity import ToyotaBaseEntity


@dataclass
class ToyotaBinaryEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Vehicle], bool | datetime | int | str | None] | None
    attributes_fn: Callable[[Vehicle], dict[str, Any] | None] | None


@dataclass
class ToyotaBinaryEntityDescription(
    EntityDescription, ToyotaBinaryEntityDescriptionMixin
):
    """Describes a Toyota binary entity."""

STARTER_BATTERY_HEALTH_ENTITY_DESCRIPTIONS = ToyotaBinaryEntityDescription(
    key="starter_battery_health",
    name="Starter battery health",
    icon="mdi:car-battery",
    device_class=BinarySensorDeviceClass.PROBLEM,
    entity_category=EntityCategory.DIAGNOSTIC,
    value_fn=lambda vh: vh.details.get("batteryHealth") == "good",
    attributes_fn=lambda vh: None,
)

OVER_ALL_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="over_all_status",
    name="over all status",
    icon="mdi:alert",
    device_class=BinarySensorDeviceClass.PROBLEM,
    value_fn=lambda vh: vh.sensors.overallstatus == "OK",
    attributes_fn=lambda vh: {LAST_UPDATED: vh.sensors.last_updated},
)

HOOD_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="hood",
    name="hood",
    device_class=BinarySensorDeviceClass.DOOR,
    entity_category=EntityCategory.DIAGNOSTIC,
    value_fn=lambda vh: False if vh.sensors.hood.closed else True,
    attributes_fn=lambda vh: {
        WARNING: vh.sensors.hood.warning,
        LAST_UPDATED: vh.sensors.last_updated,
    },
)

KEY_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="key_in_car",
    name="key in car",
    icon="mdi:car-key",
    entity_category=EntityCategory.DIAGNOSTIC,
    value_fn=lambda vh: vh.sensors.key.in_car,
    attributes_fn=lambda vh: {
        WARNING: vh.sensors.key.warning,
        LAST_UPDATED: vh.sensors.last_updated,
    },
)

DEFOGGER_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="front_defogger",
        name="front defogger",
        icon="mdi:car-defrost-front",
        value_fn=lambda vh: vh.hvac.front_defogger_is_on,
        attributes_fn=None,
    ),
    ToyotaBinaryEntityDescription(
        key="rear_defogger",
        name="rear defogger",
        icon="mdi:car-defrost-rear",
        value_fn=lambda vh: vh.hvac.rear_defogger_is_on,
        attributes_fn=None,
    ),
)

WINDOW_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="driverseat_window",
        name="driverseat window",
        device_class=BinarySensorDeviceClass.WINDOW,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.windows.driver_seat.state != "close",
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.windows.driver_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="passengerseat_window",
        name="passengerseat window",
        device_class=BinarySensorDeviceClass.WINDOW,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.windows.passenger_seat.state != "close",
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.windows.passenger_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="leftrearseat_window",
        name="leftrearseat window",
        device_class=BinarySensorDeviceClass.WINDOW,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.windows.leftrear_seat.state != "close",
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.windows.leftrear_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="rightrearseat_window",
        name="rightrearseat window",
        device_class=BinarySensorDeviceClass.WINDOW,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.windows.rightrear_seat.state != "close",
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.windows.rightrear_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
)

DOOR_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="driverseat_door",
        name="driverseat door",
        device_class=BinarySensorDeviceClass.DOOR,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: False if vh.sensors.doors.driver_seat.closed else True,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.driver_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="driverseat_lock",
        name="driverseat lock",
        device_class=BinarySensorDeviceClass.LOCK,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.doors.driver_seat.locked,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.driver_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="passengerseat_door",
        name="passengerseat door",
        device_class=BinarySensorDeviceClass.DOOR,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: False if vh.sensors.doors.passenger_seat.closed else True,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.passenger_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="passengerseat_lock",
        name="passengerseat lock",
        device_class=BinarySensorDeviceClass.LOCK,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.doors.passenger_seat.locked,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.passenger_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="leftrearseat_door",
        name="leftrearseat door",
        device_class=BinarySensorDeviceClass.DOOR,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: False if vh.sensors.doors.leftrear_seat.closed else True,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.leftrear_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="leftrearseat_lock",
        name="leftrearseat lock",
        device_class=BinarySensorDeviceClass.LOCK,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.doors.leftrear_seat.locked,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.leftrear_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="rightrearseat_door",
        name="rightrearseat door",
        device_class=BinarySensorDeviceClass.DOOR,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: False if vh.sensors.doors.rightrear_seat.closed else True,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.rightrear_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="rightrearseat_lock",
        name="rightrearseat lock",
        device_class=BinarySensorDeviceClass.LOCK,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.doors.rightrear_seat.locked,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.rightrear_seat.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="trunk_door",
        name="trunk",
        device_class=BinarySensorDeviceClass.WINDOW,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: False if vh.sensors.doors.trunk.closed else True,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.trunk.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="trunk_lock",
        name="trunk lock",
        device_class=BinarySensorDeviceClass.LOCK,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.doors.trunk.locked,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.doors.trunk.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
)

LIGHT_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="hazardlights",
        name="hazardlights",
        device_class=BinarySensorDeviceClass.LIGHT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.lights.hazardlights.off,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.lights.hazardlights.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="headlights",
        name="headlights",
        device_class=BinarySensorDeviceClass.LIGHT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.lights.headlights.off,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.lights.headlights.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="taillights",
        name="taillights",
        device_class=BinarySensorDeviceClass.LIGHT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda vh: vh.sensors.lights.taillights.off,
        attributes_fn=lambda vh: {
            WARNING: vh.sensors.lights.taillights.warning,
            LAST_UPDATED: vh.sensors.last_updated,
        },
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    binary_sensors = []

    coordinator: DataUpdateCoordinator[list[VehicleData]] = hass.data[DOMAIN][
        entry.entry_id
    ]

    for index, vehicle in enumerate(coordinator.data):
        vehicle = coordinator.data[index]["data"]

        if vehicle.details.get("batteryHealth") is not None:
            binary_sensors.append(
                ToyotaBinarySensor(
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    vehicle_index=index,
                    description=STARTER_BATTERY_HEALTH_ENTITY_DESCRIPTIONS,
                )
            )

        if vehicle.is_connected_services_enabled:
            if vehicle.hvac and vehicle.hvac.legacy:
                # Add defogger sensors if hvac is set to legacy
                for description in DEFOGGER_ENTITY_DESCRIPTIONS:
                    binary_sensors.append(
                        ToyotaBinarySensor(
                            coordinator=coordinator,
                            entry_id=entry.entry_id,
                            vehicle_index=vehicle,
                            description=description,
                        )
                    )

            if vehicle.sensors:
                if vehicle.sensors.overallstatus:
                    binary_sensors.append(
                        ToyotaBinarySensor(
                            coordinator=coordinator,
                            entry_id=entry.entry_id,
                            vehicle_index=vehicle,
                            description=OVER_ALL_STATUS_ENTITY_DESCRIPTION,
                        )
                    )

                if vehicle.sensors.windows:
                    # Add window sensors if available
                    for description in WINDOW_ENTITY_DESCRIPTIONS:
                        binary_sensors.append(
                            ToyotaBinarySensor(
                                coordinator=coordinator,
                                entry_id=entry.entry_id,
                                vehicle_index=vehicle,
                                description=description,
                            )
                        )

                if vehicle.sensors.lights:
                    # Add light sensors if available
                    for description in LIGHT_ENTITY_DESCRIPTIONS:
                        binary_sensors.append(
                            ToyotaBinarySensor(
                                coordinator=coordinator,
                                entry_id=entry.entry_id,
                                vehicle_index=vehicle,
                                description=description,
                            )
                        )

                if vehicle.sensors.hood:
                    # Add hood sensor if available
                    binary_sensors.append(
                        ToyotaBinarySensor(
                            coordinator=coordinator,
                            entry_id=entry.entry_id,
                            vehicle_index=vehicle,
                            description=HOOD_ENTITY_DESCRIPTION,
                        )
                    )

                if vehicle.sensors.doors:
                    # Add door sensors if available
                    for description in DOOR_ENTITY_DESCRIPTIONS:
                        binary_sensors.append(
                            ToyotaBinarySensor(
                                coordinator=coordinator,
                                entry_id=entry.entry_id,
                                vehicle_index=vehicle,
                                description=description,
                            )
                        )

                if vehicle.sensors.key:
                    # Add key in car sensor if available
                    binary_sensors.append(
                        ToyotaBinarySensor(
                            coordinator=coordinator,
                            entry_id=entry.entry_id,
                            vehicle_index=vehicle,
                            description=KEY_ENTITY_DESCRIPTION,
                        )
                    )

    async_add_devices(binary_sensors, True)


class ToyotaBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Representation of a Toyota binary sensor."""

    @property
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        if self.vehicle is None:
            return None
        return self.entity_description.value_fn(self.vehicle)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the attributes of the sensor."""
        if self.vehicle is None:
            return None
        return self.entity_description.attributes_fn(self.vehicle)
