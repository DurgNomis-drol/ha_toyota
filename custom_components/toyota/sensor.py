"""Platform for Toyota sensor integration."""

from homeassistant.const import DEVICE_CLASS_TEMPERATURE, PERCENTAGE

from . import ToyotaEntity
from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    FUEL,
    HVAC,
    HVAC_TEMPERATURE,
    ICON_FUEL,
    ICON_HVAC,
    ICON_ODOMETER,
    ICON_PARKING,
    ODOMETER,
    ODOMETER_UNIT,
    PARKING,
    VEHICLE_INFO,
)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    sensors = []

    for _ in enumerate(coordinator.data):
        sensors.append(ToyotaFuelRemainingSensor(coordinator))
        sensors.append(ToyotaOdometerSensor(coordinator))
        sensors.append(ToyotaHVACSensor(coordinator))
        sensors.append(ToyotaParkingSensor(coordinator))

    async_add_devices(sensors)


class ToyotaFuelRemainingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} Fuel Remaining Percentage"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/fuel_remaining_percentage"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_FUEL

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[VEHICLE_INFO][FUEL]


class ToyotaOdometerSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} Odometer"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/odometer"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.coordinator.data[VEHICLE_INFO][ODOMETER_UNIT]

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_ODOMETER

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[VEHICLE_INFO][ODOMETER]


class ToyotaHVACSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} HVAC"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/hvac"

    @property
    def device_class(self):
        """Return the class of this device, from DEVICE_CLASS_*"""
        return DEVICE_CLASS_TEMPERATURE

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_HVAC

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {self.coordinator.data[VEHICLE_INFO][HVAC]}

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[VEHICLE_INFO][HVAC][HVAC_TEMPERATURE]


class ToyotaParkingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} Parking"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/parking"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_PARKING

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {self.coordinator.data[PARKING]}

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[PARKING]["address"]
