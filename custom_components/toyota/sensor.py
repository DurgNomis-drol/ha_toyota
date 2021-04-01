"""Platform for Toyota sensor integration."""

from homeassistant.const import PERCENTAGE, STATE_UNKNOWN

from . import ToyotaEntity
from .const import (
    BATTERY_HEALTH,
    CONNECTED_SERVICES,
    DATA_COORDINATOR,
    DETAILS,
    DOMAIN,
    FUEL,
    FUEL_TYPE,
    ICON_BATTERY,
    ICON_CAR,
    ICON_FUEL,
    ICON_ODOMETER,
    LICENSE_PLATE,
    MILEAGE,
    MILEAGE_UNIT,
    ODOMETER,
    SERVICES,
    STATUS,
)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):
        sensors.append(ToyotaCarSensor(coordinator, index))

        # If Connected Services is setup for the car, setup additional sensors
        if coordinator.data[index][SERVICES][CONNECTED_SERVICES]:
            sensors.append(ToyotaStarterBatterySensor(coordinator, index))
            sensors.append(ToyotaOdometerSensor(coordinator, index))
            if FUEL in coordinator.data[index][STATUS][ODOMETER]:
                sensors.append(ToyotaFuelRemainingSensor(coordinator, index))

    async_add_devices(sensors, True)


class ToyotaCarSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias}"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/car"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data[self.index][DETAILS]

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_CAR

    @property
    def state(self):
        """Return the state of the sensor."""
        if LICENSE_PLATE in self.coordinator.data[self.index][DETAILS]:
            return self.coordinator.data[self.index][DETAILS][LICENSE_PLATE]

        return STATE_UNKNOWN


class ToyotaStarterBatterySensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} starter battery health"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/starter_battery_condition"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_BATTERY

    @property
    def state(self):
        """Return the state of the sensor."""
        if BATTERY_HEALTH in self.coordinator.data[self.index][DETAILS]:
            return (
                self.coordinator.data[self.index][DETAILS][BATTERY_HEALTH]
                .lower()
                .capitalize()
            )

        return STATE_UNKNOWN


class ToyotaFuelRemainingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} fuel tank"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/fuel_tank"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            FUEL_TYPE: self.coordinator.data[self.index][DETAILS][FUEL_TYPE],
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_FUEL

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][STATUS][ODOMETER][FUEL]


class ToyotaOdometerSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} Odometer"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/odometer"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.coordinator.data[self.index][STATUS][ODOMETER][MILEAGE_UNIT]

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_ODOMETER

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][STATUS][ODOMETER][MILEAGE]
