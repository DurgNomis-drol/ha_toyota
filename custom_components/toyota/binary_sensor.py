"""Binary sensor platform for Toyota integration"""


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
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from mytoyota.models.vehicle import Vehicle

from . import VehicleData
from .const import DOMAIN, LAST_UPDATED, WARNING
from .entity import ToyotaBaseEntity


@dataclass
class ToyotaBinaryEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Vehicle], bool]
    attributes_fn: Callable[[Vehicle], Optional[dict[str, Any]]]


@dataclass
class ToyotaBinaryEntityDescription(
    BinarySensorEntityDescription, ToyotaBinaryEntityDescriptionMixin
):
    """Describes a Toyota binary entity."""


OVER_ALL_STATUS_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="over_all_status",
    translation_key="over_all_status",
    icon="mdi:alert",
    device_class=BinarySensorDeviceClass.PROBLEM,
    value_fn=lambda vehicle: vehicle.sensors.overallstatus == "OK",
    attributes_fn=lambda vehicle: {LAST_UPDATED: vehicle.sensors.last_updated},
)

HOOD_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="hood",
    translation_key="hood",
    icon="mdi:car-door",
    device_class=BinarySensorDeviceClass.DOOR,
    value_fn=lambda vehicle: not vehicle.sensors.hood.closed,
    attributes_fn=lambda vehicle: {
        WARNING: vehicle.sensors.hood.warning,
        LAST_UPDATED: vehicle.sensors.last_updated,
    },
)

KEY_ENTITY_DESCRIPTION = ToyotaBinaryEntityDescription(
    key="key_in_car",
    translation_key="key_in_car",
    icon="mdi:car-key",
    value_fn=lambda vehicle: vehicle.sensors.key.in_car,
    attributes_fn=lambda vehicle: {
        WARNING: vehicle.sensors.key.warning,
        LAST_UPDATED: vehicle.sensors.last_updated,
    },
)

DEFOGGER_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="front_defogger",
        translation_key="front_defogger",
        icon="mdi:car-defrost-front",
        value_fn=lambda vehicle: vehicle.hvac.front_defogger_is_on,
        attributes_fn=lambda vehicle: None,
    ),
    ToyotaBinaryEntityDescription(
        key="rear_defogger",
        translation_key="rear_defogger",
        icon="mdi:car-defrost-rear",
        value_fn=lambda vehicle: vehicle.hvac.rear_defogger_is_on,
        attributes_fn=lambda vehicle: None,
    ),
)

WINDOW_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="driverseat_window",
        translation_key="driverseat_window",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda vehicle: vehicle.sensors.windows.driver_seat.state != "close",
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.windows.driver_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="passengerseat_window",
        translation_key="passengerseat_window",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda vehicle: vehicle.sensors.windows.passenger_seat.state
        != "close",
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.windows.passenger_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="leftrearseat_window",
        translation_key="leftrearseat_window",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda vehicle: vehicle.sensors.windows.leftrear_seat.state != "close",
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.windows.leftrear_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="rightrearseat_window",
        translation_key="rightrearseat_window",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda vehicle: vehicle.sensors.windows.rightrear_seat.state
        != "close",
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.windows.rightrear_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
)

DOOR_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="driverseat_door",
        translation_key="driverseat_door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda vehicle: not vehicle.sensors.doors.driver_seat.closed,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.driver_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="driverseat_lock",
        translation_key="driverseat_lock",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda vehicle: vehicle.sensors.doors.driver_seat.locked,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.driver_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="passengerseat_door",
        translation_key="passengerseat_door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda vehicle: not vehicle.sensors.doors.passenger_seat.closed,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.passenger_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="passengerseat_lock",
        translation_key="passengerseat_lock",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda vehicle: vehicle.sensors.doors.passenger_seat.locked,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.passenger_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="leftrearseat_door",
        translation_key="leftrearseat_door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda vehicle: not vehicle.sensors.doors.leftrear_seat.closed,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.leftrear_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="leftrearseat_lock",
        translation_key="leftrearseat_lock",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda vehicle: vehicle.sensors.doors.leftrear_seat.locked,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.leftrear_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="rightrearseat_door",
        translation_key="rightrearseat_door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda vehicle: not vehicle.sensors.doors.rightrear_seat.closed,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.rightrear_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="rightrearseat_lock",
        translation_key="rightrearseat_lock",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda vehicle: vehicle.sensors.doors.rightrear_seat.locked,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.rightrear_seat.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="trunk_door",
        translation_key="trunk_door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda vehicle: not vehicle.sensors.doors.trunk.closed,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.trunk.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="trunk_lock",
        translation_key="trunk_lock",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda vehicle: vehicle.sensors.doors.trunk.locked,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.doors.trunk.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
)

LIGHT_ENTITY_DESCRIPTIONS: tuple[ToyotaBinaryEntityDescription, ...] = (
    ToyotaBinaryEntityDescription(
        key="hazardlights",
        translation_key="hazardlights",
        icon="mdi:car-light-high",
        device_class=BinarySensorDeviceClass.LIGHT,
        value_fn=lambda vehicle: vehicle.sensors.lights.hazardlights.off,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.lights.hazardlights.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="headlights",
        translation_key="headlights",
        icon="mdi:car-light-high",
        device_class=BinarySensorDeviceClass.LIGHT,
        value_fn=lambda vehicle: vehicle.sensors.lights.headlights.off,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.lights.headlights.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
        },
    ),
    ToyotaBinaryEntityDescription(
        key="taillights",
        translation_key="taillights",
        icon="mdi:car-light-high",
        device_class=BinarySensorDeviceClass.LIGHT,
        value_fn=lambda vehicle: vehicle.sensors.lights.taillights.off,
        attributes_fn=lambda vehicle: {
            WARNING: vehicle.sensors.lights.taillights.warning,
            LAST_UPDATED: vehicle.sensors.last_updated,
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
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.vehicle)

    @property
    def extra_state_attributes(self) -> Optional[dict[str, Any]]:
        """Return the attributes of the sensor."""
        return self.entity_description.attributes_fn(self.vehicle)
