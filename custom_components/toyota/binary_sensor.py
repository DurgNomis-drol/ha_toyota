"""Binary sensor platform for Toyota integration"""

from homeassistant.components.binary_sensor import (
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

        if (
            coordinator.data[index].is_connected
            and coordinator.data[index].status is not None
        ):
            binary_sensors.append(
                ToyotaWindowBinarySensor(coordinator, index, "driverseat_window")
            )
            binary_sensors.append(
                ToyotaWindowBinarySensor(coordinator, index, "passengerseat_window")
            )
            binary_sensors.append(
                ToyotaWindowBinarySensor(coordinator, index, "rightrearseat_window")
            )
            binary_sensors.append(
                ToyotaWindowBinarySensor(coordinator, index, "leftrearseat_window")
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
            self.sensor_name.split("_")[0],
        )

        return {
            "warning": window.warning,
        }

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""

        window = getattr(
            self.coordinator.data[self.index].status.windows,
            self.sensor_name.split("_")[0],
        )

        if window.state == "close":
            return False

        return True
