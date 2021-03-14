"""Platform for Toyota sensor integration."""

from homeassistant.const import DEVICE_CLASS_TEMPERATURE, PERCENTAGE

from . import ToyotaEntity
from .const import (
    BATTERY,
    DASHBOARD,
    DATA_COORDINATOR,
    DOMAIN,
    ENGINE,
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
    LAST_UPDATED,
    ODOMETER,
    ODOMETER_UNIT,
    PARKING,
    PRODUCTION_YEAR,
    TRANSMISSION,
    VEHICLE_INFO,
    VIN,
)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    sensors = []

    for index, _ in enumerate(coordinator.data):
        sensors.append(ToyotaCarSensor(coordinator, index))
        # If Connected Services is setup for the car, setup additional sensors
        if coordinator.data[index][DASHBOARD][ODOMETER] is not None:
            sensors.append(ToyotaFuelRemainingSensor(coordinator, index))
            sensors.append(ToyotaOdometerSensor(coordinator, index))
            sensors.append(ToyotaHVACSensor(coordinator, index))
            sensors.append(ToyotaParkingSensor(coordinator, index))
            # If car is hybrid, add battery sensor
            if coordinator.data[index][VEHICLE_INFO][HYBRID]:
                sensors.append(ToyotaEVSensor(coordinator, index))

    async_add_devices(sensors)


class ToyotaCarSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname}"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/car"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        vehicle_info = self.coordinator.data[self.index][VEHICLE_INFO]
        return {
            "model_name": self.model,
            VIN: self.vin,
            HYBRID: vehicle_info[HYBRID],
            PRODUCTION_YEAR: vehicle_info[PRODUCTION_YEAR],
            ENGINE: vehicle_info[ENGINE],
            TRANSMISSION: vehicle_info[TRANSMISSION],
            FUEL_TYPE: self.coordinator.data[self.index][DASHBOARD][FUEL_TYPE],
            LAST_UPDATED: self.last_updated,
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_CAR

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.model


class ToyotaFuelRemainingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} fuel tank"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/fuel_tank"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            FUEL_TYPE: self.coordinator.data[self.index][DASHBOARD][FUEL_TYPE],
            LAST_UPDATED: self.last_updated,
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_FUEL

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][DASHBOARD][FUEL]


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
        return self.coordinator.data[self.index][DASHBOARD][ODOMETER_UNIT]

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            LAST_UPDATED: self.last_updated,
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_ODOMETER

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][DASHBOARD][ODOMETER]


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
        return {
            HVAC: self.coordinator.data[self.index][HVAC],
            LAST_UPDATED: self.last_updated,
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][HVAC][HVAC_TEMPERATURE]


class ToyotaParkingSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} last parked"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/last_parked"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_PARKING

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            PARKING: self.coordinator.data[self.index][PARKING],
            LAST_UPDATED: self.last_updated,
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][PARKING]["address"]


class ToyotaEVSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.nickname} battery"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.nickname}/battery"

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
        return {
            BATTERY: self.coordinator.data[self.index][BATTERY],
            LAST_UPDATED: self.last_updated,
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index][BATTERY]["ChargeRemainingAmount"]
