"""Custom coordinator entity base classes for Toyota Connected Services integration."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from mytoyota.models.vehicle import Vehicle

from . import VehicleData
from .const import DOMAIN


class ToyotaBaseEntity(CoordinatorEntity):
    """Defines a base Toyota entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[list[VehicleData]],
        entry_id: str,
        vehicle_index: int,
        description: EntityDescription,
    ) -> None:
        """Initialize the Toyota entity."""
        super().__init__(coordinator)

        self.index = vehicle_index
        self.vehicle: Vehicle = coordinator.data[self.index]["data"]

        self._attr_unique_id = f"{entry_id}_{self.vehicle.vin}/{description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.vehicle.vin)},
            name=self.vehicle.alias,
            model=self.vehicle._vehicle_info.car_model_name,
            manufacturer=DOMAIN.capitalize(),
        )
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.vehicle = self.coordinator.data[self.index]["data"]
        super()._handle_coordinator_update()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
