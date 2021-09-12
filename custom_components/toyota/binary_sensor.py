"""Binary sensor platform for Toyota integration"""

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_LIGHT,
    DEVICE_CLASS_WINDOW,
    BinarySensorEntity,
)

from .const import DATA_COORDINATOR, DOMAIN
from .entity import ToyotaBaseEntity


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    binary_sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):

        if coordinator.data[index].is_connected:

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
                            coordinator, index, "rightrearseat window"
                        ),
                        ToyotaWindowBinarySensor(
                            coordinator, index, "leftrearseat window"
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

    async_add_devices(binary_sensors, True)


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
            "warning": window.warning,
        }

    @property
    def is_on(self):
        """Return true if th window is down open."""

        window = getattr(
            self.coordinator.data[self.index].status.windows,
            self.sensor_name.split(" ")[0],
        )

        if window.state == "close":
            return False

        return True


class ToyotaLightBinarySensor(ToyotaBaseEntity, BinarySensorEntity):
    """Class for Light sensor"""

    _attr_device_class = DEVICE_CLASS_LIGHT

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        light = getattr(
            self.coordinator.data[self.index].status.lights,
            self.sensor_name.split(" ")[0],
        )

        return {
            "warning": light.warning,
        }

    @property
    def is_on(self):
        """Return true if light is on."""

        light = getattr(
            self.coordinator.data[self.index].status.lights,
            self.sensor_name.split(" ")[0],
        )

        return not light.off
