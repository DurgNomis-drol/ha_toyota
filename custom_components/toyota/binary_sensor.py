"""Binary sensor platform for Toyota integration"""

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_LIGHT,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_WINDOW,
    BinarySensorEntity,
)

from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    ICON_CAR_DOOR,
    ICON_CAR_DOOR_LOCK,
    ICON_CAR_LIGHTS,
    ICON_KEY,
    LAST_UPDATED,
    WARNING,
)
from .entity import ToyotaBaseEntity


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    binary_sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):

        if coordinator.data[index].is_connected:

            if coordinator.data[index].status.overallstatus:
                binary_sensors.extend(
                    [
                        ToyotaOverAllStatusBinarySensor(
                            coordinator, index, "over all status"
                        ),
                    ]
                )

            if coordinator.data[index].status.windows:
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

            if coordinator.data[index].status.lights:
                # Add light sensors if available
                binary_sensors.extend(
                    [
                        ToyotaLightBinarySensor(coordinator, index, "front lights"),
                        ToyotaLightBinarySensor(coordinator, index, "back lights"),
                        ToyotaLightBinarySensor(coordinator, index, "hazard lights"),
                    ]
                )

            if coordinator.data[index].status.doors:
                # Add door sensors if available
                binary_sensors.extend(
                    [
                        ToyotaDoorBinarySensor(coordinator, index, "hood"),
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
                        ToyotaDoorBinarySensor(coordinator, index, "tailgate door"),
                        ToyotaDoorLockBinarySensor(coordinator, index, "tailgate lock"),
                    ]
                )

            if coordinator.data[index].status.key:
                # Add key in car sensor if available
                binary_sensors.extend(
                    [ToyotaKeyBinarySensor(coordinator, index, "key_in_car")]
                )

    async_add_devices(binary_sensors, True)


class ToyotaDoorBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for door sensor"""

    _attr_device_class = DEVICE_CLASS_DOOR
    _attr_icon = ICON_CAR_DOOR

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        door = getattr(
            self.coordinator.data[self.index].status.doors,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: door.warning,
            LAST_UPDATED: self.coordinator.data[self.index].status.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the door is down open."""

        door = getattr(
            self.coordinator.data[self.index].status.doors,
            self.sensor_name.split(" ")[0],
        )

        return not door.closed


class ToyotaDoorLockBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for door locked sensor"""

    _attr_device_class = DEVICE_CLASS_DOOR
    _attr_icon = ICON_CAR_DOOR_LOCK

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        door = getattr(
            self.coordinator.data[self.index].status.doors,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: door.warning,
            LAST_UPDATED: self.coordinator.data[self.index].status.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the door is down open."""

        door = getattr(
            self.coordinator.data[self.index].status.doors,
            self.sensor_name.split(" ")[0],
        )

        return not door.locked


class ToyotaKeyBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for key in car binary sensor"""

    _attr_icon = ICON_KEY

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            WARNING: self.coordinator.data[self.index].status.key.warning,
        }

    @property
    def is_on(self):
        """Return true if key is in car."""
        return self.coordinator.data[self.index].status.key.in_car


class ToyotaLightBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for Light sensor"""

    _attr_device_class = DEVICE_CLASS_LIGHT
    _attr_icon = ICON_CAR_LIGHTS

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        light = getattr(
            self.coordinator.data[self.index].status.lights,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: light.warning,
            LAST_UPDATED: self.coordinator.data[self.index].status.last_updated,
        }

    @property
    def is_on(self):
        """Return true if light is on."""

        light = getattr(
            self.coordinator.data[self.index].status.lights,
            self.sensor_name.split(" ")[0],
        )

        return not light.off


class ToyotaOverAllStatusBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for the overall warning sensor"""

    _attr_device_class = DEVICE_CLASS_PROBLEM

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        return {
            LAST_UPDATED: self.coordinator.data[self.index].status.last_updated,
        }

    @property
    def is_on(self):
        """Return true if a overallstatus is not OK."""

        return not self.coordinator.data[self.index].status.overallstatus == "OK"


class ToyotaWindowBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for Window sensor"""

    _attr_device_class = DEVICE_CLASS_WINDOW

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        window = getattr(
            self.coordinator.data[self.index].status.windows,
            self.sensor_name.split(" ")[0],
        )

        return {
            WARNING: window.warning,
            LAST_UPDATED: self.coordinator.data[self.index].status.last_updated,
        }

    @property
    def is_on(self):
        """Return true if the window is down open."""

        window = getattr(
            self.coordinator.data[self.index].status.windows,
            self.sensor_name.split(" ")[0],
        )

        if window.state == "close":
            return False

        return True
