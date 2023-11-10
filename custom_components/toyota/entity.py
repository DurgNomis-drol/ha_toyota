"""Custom coordinator entity base classes for Toyota Connected Services integration"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from mytoyota.models.vehicle import Vehicle

from . import StatisticsData, VehicleData
from .const import DOMAIN


@dataclass
class ToyotaEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[
        [Vehicle | StatisticsData], bool | datetime | int | str | None
    ] | None = None
    attributes_fn: Callable[
        [Vehicle | StatisticsData], dict[str, Any] | None
    ] | None = None
    unit_fn: Callable[[Vehicle | StatisticsData], str | None] | str | None = None
    periode: str | None = None


@dataclass
class ToyotaEntityDescription(EntityDescription, ToyotaEntityDescriptionMixin):
    """Describes a Toyota entity."""


class ToyotaBaseEntity(CoordinatorEntity):
    """Defines a base Toyota entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[list[VehicleData]],
        entry_id: str,
        vehicle_index: int,
        description: ToyotaEntityDescription,
    ) -> None:
        """Initialize the Toyota entity."""
        super().__init__(coordinator)

        self.index = vehicle_index
        self.vehicle: Vehicle = coordinator.data[self.index]["data"]

        self._attr_unique_id = f"{entry_id}_{self.vehicle.vin}/{description.key}"
        self._attr_name = f"{self.vehicle.alias} {description.name}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.vehicle.vin)},
            name=self.vehicle.alias,
            model=self.vehicle.details.get("modelName"),
            manufacturer=DOMAIN.capitalize(),
        )
        self.entity_description = description

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the attributes of the sensor."""
        if self.vehicle is None:
            return None
        return self.entity_description.attributes_fn(self.vehicle)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.vehicle = self.coordinator.data[self.index]["data"]
        super()._handle_coordinator_update()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
