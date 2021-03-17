"""Platform for Toyota sensor integration."""

from homeassistant.const import DEVICE_CLASS_TEMPERATURE, PERCENTAGE

from . import ToyotaEntity
from .const import (
    BATTERY,
    DATA_COORDINATOR,
    DETAILS,
    DOMAIN,
    FUEL,
    FUEL_TYPE,
    HVAC,
    HVAC_TEMPERATURE,
    HYBRID,
    ICON_BATTERY,
    ICON_CAR,
    ICON_FUEL,
    ICON_HVAC,
    ICON_ODOMETER,
    ICON_PARKING,
    IMAGE,
    MILEAGE,
    ODOMETER,
    ODOMETER_UNIT,
    PARKING,
    STATUS,
)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    sensors = []

    def check_if_enabled(service):
        """Check if Toyota Connected Services is enabled for the car."""
        if "error" in service:
            return False

        return True

    for index, _ in enumerate(coordinator.data):
        sensors.append(ToyotaCarSensor(coordinator, index))

        # If Connected Services is setup for the car, setup additional sensors
        if check_if_enabled(coordinator.data[index][STATUS][ODOMETER]):
            sensors.append(ToyotaFuelRemainingSensor(coordinator, index))
            sensors.append(ToyotaOdometerSensor(coordinator, index))
        if check_if_enabled(coordinator.data[index][STATUS][HVAC]):
            sensors.append(ToyotaHVACSensor(coordinator, index))
        if check_if_enabled(coordinator.data[index][STATUS][PARKING]):
            sensors.append(ToyotaParkingSensor(coordinator, index))
        if coordinator.data[index][DETAILS][HYBRID]:
            sensors.append(ToyotaEVSensor(coordinator, index))

    async_add_devices(sensors)


class ToyotaCarSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias}"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/car"

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
        return self.model

    @property
    def entity_picture(self):
        """Return entity picture."""
        return self.coordinator.data[self.index][DETAILS][IMAGE]


class ToyotaFuelRemainingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} fuel tank"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/fuel_tank"

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
        return self.coordinator.data[self.index][ODOMETER][FUEL]


class ToyotaOdometerSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} Odometer"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/odometer"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.coordinator.data[self.index][ODOMETER][ODOMETER_UNIT]

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_ODOMETER

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][DETAILS][MILEAGE]


class ToyotaHVACSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} HVAC"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/hvac"

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
        return self.coordinator.data[self.index][STATUS][HVAC]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][STATUS][HVAC][HVAC_TEMPERATURE]


class ToyotaParkingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} last parked"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/last_parked"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_PARKING

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data[self.index][STATUS][PARKING]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][STATUS][PARKING]["address"]


class ToyotaEVSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} battery"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.alias}/battery"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_BATTERY

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data[self.index][STATUS][BATTERY]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][STATUS][BATTERY][
            "ChargeRemainingAmount"
        ]
