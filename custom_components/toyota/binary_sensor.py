"""Binary sensor platform for Toyota integration"""
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import ENTITY_CATEGORY_DIAGNOSTIC

from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    ICON_CAR_DOOR,
    ICON_CAR_DOOR_LOCK,
    ICON_CAR_LIGHTS,
    ICON_FRONT_DEFOGGER,
    ICON_KEY,
    ICON_REAR_DEFOGGER,
    LAST_UPDATED,
    WARNING,
)
from .entity import ToyotaBaseEntity


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    binary_sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):

        vehicle = coordinator.data[index]

        if vehicle.is_connected:

            if vehicle.sensors.overallstatus:
                binary_sensors.extend(
                    [
                        ToyotaOverAllStatusBinarySensor(
                            coordinator, index, "over all status"
                        ),
                    ]
                )

            if vehicle.sensors.windows:
                # Add window sensors if available
                binary_sensors.extend(
                    [
                        ToyotaWindowBinarySensor(
                            coordinator, index, "driverseat window"
                        ),
                        ToyotaWindowBinarySensor(
                            coordinator, index, "passengerseat window"
                        ),
                        ToyotaWindowBinarySensor(
                            coordinator, index, "leftrearseat window"
                        ),
                        ToyotaWindowBinarySensor(
                            coordinator, index, "rightrearseat window"
                        ),
                    ]
                )

            if vehicle.sensors.lights:
                # Add light sensors if available
                binary_sensors.extend(
                    [
                        ToyotaLightBinarySensor(coordinator, index, "front lights"),
                        ToyotaLightBinarySensor(coordinator, index, "back lights"),
                        ToyotaLightBinarySensor(coordinator, index, "hazard lights"),
                    ]
                )

            if vehicle.sensors.hood:
                # Add hood sensor if available
                binary_sensors.extend(
                    [
                        ToyotaHoodBinarySensor(coordinator, index, "hood"),
                    ]
                )

            if vehicle.sensors.doors:
                # Add door sensors if available
                binary_sensors.extend(
                    [
                        ToyotaDoorBinarySensor(coordinator, index, "driverseat door"),
                        ToyotaDoorLockBinarySensor(
                            coordinator, index, "driverseat lock"
                        ),
                        ToyotaDoorBinarySensor(
                            coordinator, index, "passengerseat door"
                        ),
                        ToyotaDoorLockBinarySensor(
                            coordinator, index, "passengerseat lock"
                        ),
                        ToyotaDoorBinarySensor(coordinator, index, "leftrearseat door"),
                        ToyotaDoorLockBinarySensor(
                            coordinator, index, "leftrearseat lock"
                        ),
                        ToyotaDoorBinarySensor(
                            coordinator, index, "rightrearseat door"
                        ),
                        ToyotaDoorLockBinarySensor(
                            coordinator, index, "rightrearseat lock"
                        ),
                        ToyotaDoorBinarySensor(coordinator, index, "trunk door"),
                        ToyotaDoorLockBinarySensor(coordinator, index, "trunk lock"),
                    ]
                )

            if vehicle.sensors.key:
                # Add key in car sensor if available
                binary_sensors.extend(
                    [ToyotaKeyBinarySensor(coordinator, index, "key_in_car")]
                )

            if vehicle.hvac and vehicle.hvac.legacy:
                # Add defogger sensors if hvac is set to legacy
                binary_sensors.extend(
                    [
                        ToyotaFrontDefoggerSensor(coordinator, index, "front defogger"),
                        ToyotaRearDefoggerSensor(coordinator, index, "rear defogger"),
                    ]
                )

    async_add_devices(binary_sensors, True)


class ToyotaHoodBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for the hood sensor"""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = ICON_CAR_DOOR
    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            WARNING: self.coordinator.data[self.index].sensors.hood.warning,
            LAST_UPDATED: self.coordinator.data[self.index].sensors.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the hood is open."""
        return not self.coordinator.data[self.index].sensors.hood.closed


class ToyotaDoorBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for door sensor"""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = ICON_CAR_DOOR
    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        door = getattr(
            self.coordinator.data[self.index].sensors.doors,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: door.warning,
            LAST_UPDATED: self.coordinator.data[self.index].sensors.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the door is open."""

        door = getattr(
            self.coordinator.data[self.index].sensors.doors,
            self.sensor_name.split(" ")[0],
        )

        return not door.closed


class ToyotaDoorLockBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for door locked sensor"""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = ICON_CAR_DOOR_LOCK
    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        door = getattr(
            self.coordinator.data[self.index].sensors.doors,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: door.warning,
            LAST_UPDATED: self.coordinator.data[self.index].sensors.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the door is unlocked."""

        door = getattr(
            self.coordinator.data[self.index].sensors.doors,
            self.sensor_name.split(" ")[0],
        )

        return not door.locked


class ToyotaKeyBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for key in car binary sensor"""

    _attr_icon = ICON_KEY
    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            WARNING: self.coordinator.data[self.index].sensors.key.warning,
        }

    @property
    def is_on(self):
        """Return true if key is in car."""
        return self.coordinator.data[self.index].sensors.key.in_car


class ToyotaLightBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for Light sensor"""

    _attr_device_class = BinarySensorDeviceClass.LIGHT
    _attr_icon = ICON_CAR_LIGHTS
    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        light = getattr(
            self.coordinator.data[self.index].sensors.lights,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: light.warning,
            LAST_UPDATED: self.coordinator.data[self.index].sensors.last_updated,
        }

    @property
    def is_on(self):
        """Return true if light is on."""

        light = getattr(
            self.coordinator.data[self.index].sensors.lights,
            self.sensor_name.split(" ")[0],
        )

        return not light.off


class ToyotaOverAllStatusBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for the overall warning sensor"""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        return {
            LAST_UPDATED: self.coordinator.data[self.index].sensors.last_updated,
        }

    @property
    def is_on(self):
        """Return true if a overallstatus is not OK."""

        return not self.coordinator.data[self.index].sensors.overallstatus == "OK"


class ToyotaWindowBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for Window sensor"""

    _attr_device_class = BinarySensorDeviceClass.WINDOW
    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        window = getattr(
            self.coordinator.data[self.index].sensors.windows,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: window.warning,
            LAST_UPDATED: self.coordinator.data[self.index].sensors.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the window is down."""

        window = getattr(
            self.coordinator.data[self.index].sensors.windows,
            self.sensor_name.split(" ")[0],
        )

        if window.state == "close":
            return False

        return True


class ToyotaFrontDefoggerSensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for HVAC sensor"""

    _attr_icon = ICON_FRONT_DEFOGGER

    @property
    def is_on(self):
        """Return true if the defogger is on."""

        return self.coordinator.data[self.index].hvac.front_defogger_on


class ToyotaRearDefoggerSensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for HVAC sensor"""

    _attr_icon = ICON_REAR_DEFOGGER

    @property
    def is_on(self):
        """Return true if the defogger is on."""

        return self.coordinator.data[self.index].hvac.rear_defogger_on
