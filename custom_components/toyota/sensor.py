"""Sensor platform for Toyota integration."""
from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional, Union

import arrow
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    PERCENTAGE,
    STATE_UNKNOWN,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from mytoyota.models.vehicle import Vehicle

from . import StatisticsData, VehicleData
from .const import BUCKET, DATA, DOMAIN, LICENSE_PLATE, PERIODE_START, TOTAL_DISTANCE
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


LICENSE_PLATE_ENTITY_DESCRIPTION = ToyotaSensorEntityDescription(
    key="license_plate",
    translation_key="license_plate",
    icon="mdi:car-info",
    entity_category=EntityCategory.DIAGNOSTIC,
    device_class=SensorDeviceClass.ENUM,
    native_unit_of_measurement=None,
    state_class=None,
    value_fn=lambda vehicle: vehicle.details.get(LICENSE_PLATE, STATE_UNKNOWN),
    attributes_fn=lambda vehicle: vehicle.details,
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

    period: str


@dataclass
class ToyotaStatisticsSensorEntityDescription(SensorEntityDescription, ToyotaStatisticsSensorEntityDescriptionMixin):
    """Describes a Toyota statistics sensor entity."""


STATISTICS_ENTITY_DESCRIPTIONS: tuple[ToyotaStatisticsSensorEntityDescription, ...] = (
    ToyotaStatisticsSensorEntityDescription(
        key="current_day_statistics",
        translation_key="current_day_statistics",
        icon="mdi:history",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        period="day",
    ),
    ToyotaStatisticsSensorEntityDescription(
        key="current_week_statistics",
        translation_key="current_week_statistics",
        icon="mdi:history",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        period="week",
    ),
    ToyotaStatisticsSensorEntityDescription(
        key="current_month_statistics",
        translation_key="current_month_statistics",
        icon="mdi:history",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        period="month",
    ),
    ToyotaStatisticsSensorEntityDescription(
        key="current_year_statistics",
        translation_key="current_year_statistics",
        icon="mdi:history",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        period="year",
    ),
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

        sensors.append(
            ToyotaSensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=LICENSE_PLATE_ENTITY_DESCRIPTION,
            )
        )

        if vehicle.is_connected_services_enabled:
            for description in STATISTICS_ENTITY_DESCRIPTIONS:
                sensors.append(
                    ToyotaStatisticsSensor(
                        coordinator=coordinator,
                        entry_id=entry.entry_id,
                        vehicle_index=index,
                        description=description,
                    )
                )

        if vehicle.details.get("batteryHealth") is not None:
            sensors.append(
                ToyotaSensor(
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    vehicle_index=index,
                    description=STARTER_BATTERY_HEALTH_ENTITY_DESCRIPTIONS,
                )
            )

        sensors.append(
            ToyotaSensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=ODOMETER_ENTITY_DESCRIPTION_KM
                if vehicle.dashboard.is_metric
                else ODOMETER_ENTITY_DESCRIPTION_MILES,
            )
        )

        sensors.append(
            ToyotaSensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=FUEL_LEVEL_ENTITY_DESCRIPTION,
            )
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
        self.period = description.period
        self._attr_native_unit_of_measurement = LENGTH_KILOMETERS if self.vehicle.dashboard.is_metric else LENGTH_MILES

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data[self.index]["statistics"][self.period][0]
        return round(data[DATA][TOTAL_DISTANCE], 1) if DATA in data else None

    def _get_time_period_attributes(self, data: dict[str, Any]):
        """Get time period attributes."""
        now = arrow.now()
        if self.period == "day":
            dt = now.floor("day").format("YYYY-MM-DD")
            return {"Day": data[BUCKET]["date"] if BUCKET in data else dt}
        elif self.period == "week":
            from_dt = now.floor("week").format("YYYY-MM-DD")
            to_dt = now.ceil("week").format("YYYY-MM-DD")
            return {
                "From": data[BUCKET][PERIODE_START] if BUCKET in data else from_dt,
                "To": to_dt,
            }
        elif self.period == "month":
            from_month = now.floor("month").format("MMMM")
            return {"Month": from_month}
        elif self.period == "year":
            from_year = now.floor("year").format("YYYY")
            return {"Year": data[BUCKET]["year"] if BUCKET in data else from_year}
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data[self.index]["statistics"][self.period][0]
        attributes = format_statistics_attributes(data.get(DATA, {}), self.vehicle.hybrid)
        attributes.update(self._get_time_period_attributes(data))
        return attributes

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.statistics = self.coordinator.data[self.index]["statistics"]
        super()._handle_coordinator_update()
