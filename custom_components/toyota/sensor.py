"""Sensor platform for Toyota integration."""
from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, Optional, Union

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import LENGTH_KILOMETERS, LENGTH_MILES, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from mytoyota.models.vehicle import Vehicle

from . import StatisticsData, VehicleData
from .const import DOMAIN
from .entity import ToyotaBaseEntity
from .utils import format_statistics_attributes, round_number

_LOGGER = logging.getLogger(__name__)


@dataclass
class ToyotaSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Vehicle], StateType]
    attributes_fn: Callable[[Vehicle], Optional[dict[str, Any]]]


@dataclass
class ToyotaSensorEntityDescription(SensorEntityDescription, ToyotaSensorEntityDescriptionMixin):
    """Describes a Toyota sensor entity."""


# TODO: There is currently no information on the licence plate. Add it, wehen available
VIN_ENTITY_DESCRIPTION = ToyotaSensorEntityDescription(
    key="vin",
    translation_key="vin",
    icon="mdi:car-info",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=SensorDeviceClass.ENUM,
    native_unit_of_measurement=None,
    state_class=None,
    value_fn=lambda vehicle: vehicle.vin,
    attributes_fn=lambda vehicle: vehicle._vehicle_info.dict(),
)
STARTER_BATTERY_HEALTH_ENTITY_DESCRIPTIONS = ToyotaSensorEntityDescription(
    key="starter_battery_health",
    translation_key="starter_battery_health",
    icon="mdi:car_battery",
    device_class=SensorDeviceClass.ENUM,
    native_unit_of_measurement=None,
    state_class=None,
    value_fn=lambda vehicle: vehicle.details.get("batteryHealth").capitalize(),
    attributes_fn=lambda vehicle: None,  # noqa : ARG005
)
ODOMETER_ENTITY_DESCRIPTION_KM = ToyotaSensorEntityDescription(
    key="odometer",
    translation_key="odometer",
    icon="mdi:counter",
    device_class=SensorDeviceClass.DISTANCE,
    native_unit_of_measurement=LENGTH_KILOMETERS,
    state_class=SensorStateClass.MEASUREMENT,
    value_fn=lambda vehicle: vehicle.dashboard.odometer,
    suggested_display_precision=0,
    attributes_fn=lambda vehicle: None,  # noqa : ARG005
)
ODOMETER_ENTITY_DESCRIPTION_MILES = ToyotaSensorEntityDescription(
    key="odometer",
    translation_key="odometer",
    icon="mdi:counter",
    device_class=SensorDeviceClass.DISTANCE,
    native_unit_of_measurement=LENGTH_MILES,
    state_class=SensorStateClass.MEASUREMENT,
    value_fn=lambda vehicle: vehicle.dashboard.odometer,
    suggested_display_precision=0,
    attributes_fn=lambda vehicle: None,  # noqa : ARG005
)
FUEL_LEVEL_ENTITY_DESCRIPTION = ToyotaSensorEntityDescription(
    key="fuel_level",
    translation_key="fuel_level",
    icon="mdi:gas-station",
    device_class=None,
    native_unit_of_measurement=PERCENTAGE,
    state_class=SensorStateClass.MEASUREMENT,
    value_fn=lambda vehicle: round_number(vehicle.dashboard.fuel_level, 0),
    suggested_display_precision=0,
    attributes_fn=lambda vehicle: None,  # noqa : ARG005
)


@dataclass
class ToyotaStatisticsSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    period: Literal["day", "week", "month", "year"]


@dataclass
class ToyotaStatisticsSensorEntityDescription(SensorEntityDescription, ToyotaStatisticsSensorEntityDescriptionMixin):
    """Describes a Toyota statistics sensor entity."""


STATISTICS_ENTITY_DESCRIPTIONS_DAILY = ToyotaStatisticsSensorEntityDescription(
    key="current_day_statistics",
    translation_key="current_day_statistics",
    icon="mdi:history",
    device_class=SensorDeviceClass.DISTANCE,
    state_class=SensorStateClass.MEASUREMENT,
    suggested_display_precision=0,
    period="day",
)

STATISTICS_ENTITY_DESCRIPTIONS_WEEKLY = ToyotaStatisticsSensorEntityDescription(
    key="current_week_statistics",
    translation_key="current_week_statistics",
    icon="mdi:history",
    device_class=SensorDeviceClass.DISTANCE,
    state_class=SensorStateClass.MEASUREMENT,
    suggested_display_precision=0,
    period="week",
)

STATISTICS_ENTITY_DESCRIPTIONS_MONTHLY = ToyotaStatisticsSensorEntityDescription(
    key="current_month_statistics",
    translation_key="current_month_statistics",
    icon="mdi:history",
    device_class=SensorDeviceClass.DISTANCE,
    state_class=SensorStateClass.MEASUREMENT,
    suggested_display_precision=0,
    period="month",
)

STATISTICS_ENTITY_DESCRIPTIONS_YEARLY = ToyotaStatisticsSensorEntityDescription(
    key="current_year_statistics",
    translation_key="current_year_statistics",
    icon="mdi:history",
    device_class=SensorDeviceClass.DISTANCE,
    state_class=SensorStateClass.MEASUREMENT,
    suggested_display_precision=0,
    period="year",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: DataUpdateCoordinator[list[VehicleData]] = hass.data[DOMAIN][entry.entry_id]

    sensors: list[Union[ToyotaSensor, ToyotaStatisticsSensor]] = []
    for index, _ in enumerate(coordinator.data):
        vehicle = coordinator.data[index]["data"]
        capabilities_descriptions = [
            (
                True,
                VIN_ENTITY_DESCRIPTION,
                ToyotaSensor,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.telemetry_capable,
                STATISTICS_ENTITY_DESCRIPTIONS_DAILY,
                ToyotaStatisticsSensor,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.telemetry_capable,
                STATISTICS_ENTITY_DESCRIPTIONS_WEEKLY,
                ToyotaStatisticsSensor,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.telemetry_capable,
                STATISTICS_ENTITY_DESCRIPTIONS_MONTHLY,
                ToyotaStatisticsSensor,
            ),
            (
                vehicle._vehicle_info.extended_capabilities.telemetry_capable,
                STATISTICS_ENTITY_DESCRIPTIONS_YEARLY,
                ToyotaStatisticsSensor,
            ),
        ]

        sensors.extend(
            sensor_type(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=description,
            )
            for capability, description, sensor_type in capabilities_descriptions
            if capability
        )

    async_add_devices(sensors)


class ToyotaSensor(ToyotaBaseEntity, SensorEntity):
    """Representation of a Toyota sensor."""

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.vehicle)

    @property
    def extra_state_attributes(self) -> Optional[dict[str, Any]]:
        """Return the attributes of the sensor."""
        return self.entity_description.attributes_fn(self.vehicle)


class ToyotaStatisticsSensor(ToyotaSensor):
    """Representation of a Toyota statistics sensor."""

    statistics: StatisticsData

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[list[VehicleData]],
        entry_id: str,
        vehicle_index: int,
        description: ToyotaStatisticsSensorEntityDescription,
    ) -> None:
        """Initialise the ToyotaStatisticsSensor class."""
        super().__init__(coordinator, entry_id, vehicle_index, description)
        self.period: Literal["day", "week", "month", "year"] = description.period
        self._attr_native_unit_of_measurement = LENGTH_KILOMETERS if self.metric_values else LENGTH_MILES

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        data = self.statistics[self.period]
        return round(data.distance, 1) if data else None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.statistics[self.period]
        if data is not None:
            return format_statistics_attributes(data, self.vehicle._vehicle_info)
        else:
            return None
