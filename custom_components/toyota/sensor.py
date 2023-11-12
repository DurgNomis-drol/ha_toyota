"""Sensor platform for Toyota integration"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Union

import arrow
from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    PERCENTAGE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory, EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from mytoyota.models.vehicle import Vehicle

from . import StatisticsData, VehicleData
from .const import BUCKET, DATA, DOMAIN, LICENSE_PLATE, PERIODE_START, TOTAL_DISTANCE
from .entity import ToyotaBaseEntity
from .utils import format_statistics_attributes, round_number


@dataclass
class ToyotaSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Vehicle], bool | datetime | int | str | None] | None
    attributes_fn: Callable[[Vehicle], dict[str, Any] | None] | None
    unit_fn: Callable[[Vehicle | StatisticsData], str | None] | str | None


@dataclass
class ToyotaSensorEntityDescription(
    EntityDescription, ToyotaSensorEntityDescriptionMixin
):
    """Describes a Toyota sensor entity."""


LICENSE_PLATE_ENTITY_DESCRIPTION = ToyotaSensorEntityDescription(
    key="numberplate",
    name="numberplate",
    icon="mdi:car-info",
    entity_category=EntityCategory.DIAGNOSTIC,
    value_fn=lambda data: data.details.get(LICENSE_PLATE, STATE_UNKNOWN),
    attributes_fn=lambda data: data.details,
    unit_fn=None,
)

STARTER_BATTERY_HEALTH_ENTITY_DESCRIPTIONS = ToyotaSensorEntityDescription(
    key="starter_battery_health",
    name="starter battery health",
    icon="mdi:car_battery",
    value_fn=lambda vh: vh.details.get("batteryHealth").capitalize(),
    attributes_fn=None,
    unit_fn=None,
)

ODOMETER_ENTITY_DESCRIPTION = ToyotaSensorEntityDescription(
    key="odometer",
    name="odometer",
    icon="mdi:counter",
    value_fn=lambda vh: vh.dashboard.odometer,
    attributes_fn=None,
    unit_fn=lambda vh: LENGTH_KILOMETERS if vh.dashboard.is_metric else LENGTH_MILES,
)

FUEL_ENTITY_DESCRIPTIONS: tuple[ToyotaSensorEntityDescription, ...] = (
    ToyotaSensorEntityDescription(
        key="fuel_level",
        name="fuel level",
        icon="mdi:gas-station",
        unit_fn=PERCENTAGE,
        value_fn=lambda vh: round_number(vh.dashboard.fuel_level),
        attributes_fn=lambda vh: {
            "fueltype": vh.fueltype,
        },
    ),
    ToyotaSensorEntityDescription(
        key="fuel_range",
        name="fuel range",
        icon="mdi:map-marker-distance",
        unit_fn=lambda vh: LENGTH_KILOMETERS
        if vh.dashboard.is_metric
        else LENGTH_MILES,
        value_fn=lambda vh: round_number(vh.dashboard.fuel_range, 1),
        attributes_fn=None,
    ),
)

HYBRID_ENTITY_DESCRIPTIONS: tuple[ToyotaSensorEntityDescription, ...] = (
    ToyotaSensorEntityDescription(
        key="batter_level",
        name="battery level",
        icon="mdi:battery",
        unit_fn=PERCENTAGE,
        value_fn=lambda vh: round_number(vh.dashboard.battery_level),
        attributes_fn=None,
    ),
    ToyotaSensorEntityDescription(
        key="fuel_range",
        name="fuel range",
        icon="mdi:map-marker-distance",
        unit_fn=lambda vh: LENGTH_KILOMETERS
        if vh.dashboard.is_metric
        else LENGTH_MILES,
        value_fn=lambda vh: round_number(vh.dashboard.battery_range, 1),
        attributes_fn=None,
    ),
    ToyotaSensorEntityDescription(
        key="fuel_range_aircon",
        name="fuel range with aircon",
        icon="mdi:map-marker-distance",
        unit_fn=lambda vh: LENGTH_KILOMETERS
        if vh.dashboard.is_metric
        else LENGTH_MILES,
        value_fn=lambda vh: round_number(vh.dashboard.battery_range_with_aircon, 1),
        attributes_fn=None,
    ),
    ToyotaSensorEntityDescription(
        key="charging_status",
        name="charging status",
        icon="mdi:car-electric",
        value_fn=lambda vh: vh.dashboard.charging_status,
        attributes_fn=None,
        unit_fn=None,
    ),
    ToyotaSensorEntityDescription(
        key="remaining_charge_time",
        name="remaining charge time",
        icon="mdi:car-electric",
        value_fn=lambda vh: vh.dashboard.remaining_charge_time,
        attributes_fn=None,
        unit_fn=None,
    ),
)

HVAC_ENTITY_DESCRIPTIONS: tuple[ToyotaSensorEntityDescription, ...] = (
    ToyotaSensorEntityDescription(
        key="hvac_current_temperature",
        name="current temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        unit_fn=TEMP_CELSIUS,
        value_fn=lambda vh: vh.hvac.current_temperature,
        attributes_fn=lambda vh: {
            "last_acquired": vh.hvac.last_updated or "Not supported",
        },
    ),
    ToyotaSensorEntityDescription(
        key="hvac_target_temperature",
        name="target temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        unit_fn=TEMP_CELSIUS,
        value_fn=lambda vh: vh.hvac.target_temperature,
        attributes_fn=lambda vh: {
            "last_acquired": vh.hvac.last_updated or "Not supported",
        },
    ),
)


@dataclass
class ToyotaStatisticsSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    period: str


@dataclass
class ToyotaStatisticsSensorEntityDescription(
    EntityDescription, ToyotaStatisticsSensorEntityDescriptionMixin
):
    """Describes a Toyota statistics sensor entity."""


STATISTICS_ENTITY_DESCRIPTIONS: tuple[ToyotaStatisticsSensorEntityDescription, ...] = (
    ToyotaStatisticsSensorEntityDescription(
        key="current_week_statistics",
        name="current week statistics",
        icon="mdi:history",
        period="week",
    ),
    ToyotaStatisticsSensorEntityDescription(
        key="current_month_statistics",
        name="current month statistics",
        icon="mdi:history",
        period="month",
    ),
    ToyotaStatisticsSensorEntityDescription(
        key="current_year_statistics",
        name="current year statistics",
        icon="mdi:history",
        period="year",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: DataUpdateCoordinator[list[VehicleData]] = hass.data[DOMAIN][
        entry.entry_id
    ]

    sensors: list[Union[ToyotaSensor, ToyotaStatisticsSensor]] = []
    for index, vehicle in enumerate(coordinator.data):
        # vehicle = coordinator.data[index]["data"]

        sensors.append(
            ToyotaSensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                vehicle_index=index,
                description=LICENSE_PLATE_ENTITY_DESCRIPTION,
            )
        )

        # if vehicle.is_connected_services_enabled:
        #    for description in STATISTICS_ENTITY_DESCRIPTIONS:
        #        sensors.append(
        #            ToyotaStatisticsSensor(
        #                coordinator=coordinator,
        #                entry_id=entry.entry_id,
        #                vehicle_index=index,
        #                description=description,
        #            )
        #        )

        # if vehicle.details.get("batteryHealth") is not None:
        #    sensors.append(
        #        ToyotaSensor(
        #            coordinator=coordinator,
        #            entry_id=entry.entry_id,
        #            vehicle_index=index,
        #            description=STARTER_BATTERY_HEALTH_ENTITY_DESCRIPTIONS,
        #        )
        #    )

        # if vehicle.hvac:
        #    for description in HVAC_ENTITY_DESCRIPTIONS:
        #        sensors.append(
        #            ToyotaSensor(
        #                coordinator=coordinator,
        #                entry_id=entry.entry_id,
        #                vehicle_index=index,
        #                description=description,
        #            )
        #        )

        # if vehicle.hybrid:
        #    for description in HYBRID_ENTITY_DESCRIPTIONS:
        #        sensors.append(
        #            ToyotaSensor(
        #                coordinator=coordinator,
        #                entry_id=entry.entry_id,
        #                vehicle_index=index,
        #                description=description,
        #            )
        #        )

    async_add_devices(sensors)


class ToyotaSensor(ToyotaBaseEntity):
    """Representation of a Toyota sensor."""

    _attr_state_class = STATE_CLASS_MEASUREMENT

    @property
    def native_value(self) -> Optional[Union[datetime, str, int]]:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.vehicle) if self.vehicle else None

    @property
    def extra_state_attributes(self) -> Optional[dict[str, Any]]:
        """Return the attributes of the sensor."""
        return (
            self.entity_description.attributes_fn(self.vehicle)
            if self.vehicle
            else None
        )

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return unit of measurement."""
        return self.entity_description.unit_fn(self.vehicle) if self.vehicle else None


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
        super().__init__(coordinator, entry_id, vehicle_index, description)
        self.period = description.period
        self._attr_native_unit_of_measurement = (
            LENGTH_KILOMETERS if self.vehicle.dashboard.is_metric else LENGTH_MILES
        )

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data[self.index]["statistics"][self.period][0]

        attributes = format_statistics_attributes(
            data.get(DATA, {}), self.vehicle.hybrid
        )

        if self.period == "year":
            from_year = arrow.now().floor("year").format("YYYY")
            attributes.update(
                {"Year": data[BUCKET]["year"] if BUCKET in data else from_year}
            )
        elif self.period == "month":
            from_month = arrow.now().floor("month").format("MMMM")
            attributes.update({"Month": from_month})
        elif self.period == "week":
            from_dt = arrow.now().floor("week").format("YYYY-MM-DD")
            to_dt = arrow.now().ceil("week").format("YYYY-MM-DD")
            attributes.update(
                {
                    "From": data[BUCKET][PERIODE_START] if BUCKET in data else from_dt,
                    "To": to_dt,
                }
            )

        return attributes

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data[self.index]["statistics"][self.period][0]

        total_distance = round(data[DATA][TOTAL_DISTANCE], 1) if DATA in data else None
        return STATE_UNAVAILABLE if total_distance is None else total_distance

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.statistics = self.coordinator.data[self.index]["statistics"]
        super()._handle_coordinator_update()
