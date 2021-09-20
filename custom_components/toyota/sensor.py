"""Sensor platform for Toyota sensor integration."""
import arrow

from homeassistant.const import PERCENTAGE, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    BATTERY_HEALTH,
    BUCKET,
    DATA,
    DATA_COORDINATOR,
    DOMAIN,
    FUEL_TYPE,
    ICON_BATTERY,
    ICON_CAR,
    ICON_FUEL,
    ICON_ODOMETER,
    LICENSE_PLATE,
    PERIODE_START,
    TOTAL_DISTANCE,
)
from .entity import StatisticsBaseEntity, ToyotaBaseEntity


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):

        vehicle = coordinator.data[index]

        sensors.append(ToyotaCarSensor(coordinator, index, "numberplate"))

        # If Connected Services is setup for the car, setup additional sensors
        if vehicle.is_connected:

            if BATTERY_HEALTH in vehicle.details:
                sensors.append(
                    ToyotaStarterBatterySensor(
                        coordinator, index, "starter battery health"
                    )
                )
            if vehicle.odometer.fuel:
                sensors.append(
                    ToyotaFuelRemainingSensor(coordinator, index, "fuel tank")
                )

            sensors.extend(
                [
                    ToyotaOdometerSensor(coordinator, index, "odometer"),
                    ToyotaCurrentWeekSensor(
                        coordinator, index, "current week statistics"
                    ),
                    ToyotaCurrentMonthSensor(
                        coordinator, index, "current month statistics"
                    ),
                    ToyotaCurrentYearSensor(
                        coordinator, index, "current year statistics"
                    ),
                ]
            )

    async_add_devices(sensors, True)


class ToyotaCarSensor(ToyotaBaseEntity):
    """Class for car details and numberplate sensor."""

    _attr_icon = ICON_CAR

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data[self.index].details

    @property
    def state(self):
        """Return the state of the sensor."""
        if LICENSE_PLATE in self.coordinator.data[self.index].details:
            license_plate = self.coordinator.data[self.index].details[LICENSE_PLATE]
            return None if license_plate is None else license_plate

        return STATE_UNKNOWN


class ToyotaOdometerSensor(ToyotaBaseEntity):
    """Class for the odometer sensor."""

    _attr_icon = ICON_ODOMETER

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.vehicle.odometer.unit

    @property
    def state(self):
        """Return the state of the sensor."""
        mileage = None

        if self.coordinator.data[self.index].odometer:
            mileage = self.coordinator.data[self.index].odometer.mileage
        return None if mileage is None else mileage


class ToyotaStarterBatterySensor(ToyotaBaseEntity):
    """Class for the starter battery health sensor."""

    _attr_icon = ICON_BATTERY

    @property
    def state(self):
        """Return the state of the sensor."""

        return (
            self.coordinator.data[self.index]
            .details[BATTERY_HEALTH]
            .lower()
            .capitalize()
        )


class ToyotaFuelRemainingSensor(ToyotaBaseEntity):
    """Class for the fuel remaining sensor."""

    _attr_icon = ICON_FUEL
    _attr_unit_of_measurement = PERCENTAGE

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            FUEL_TYPE: self.vehicle.details[FUEL_TYPE],
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.index].odometer.fuel


class ToyotaCurrentWeekSensor(StatisticsBaseEntity):
    """Class for current week statistics sensor."""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data[self.index].statistics.weekly[0]
        from_dt = arrow.now().floor("week").format("YYYY-MM-DD")
        to_dt = arrow.now().ceil("week").format("YYYY-MM-DD")

        attributes = self.get_statistics_attributes(data.get(DATA, {}))
        attributes.update(
            {
                "From": data[BUCKET][PERIODE_START] if BUCKET in data else from_dt,
                "To": to_dt,
            }
        )
        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        total_distance = None
        data = self.coordinator.data[self.index].statistics.weekly[0]

        if DATA in data:
            total_distance = round(data[DATA][TOTAL_DISTANCE], 1)

        return STATE_UNAVAILABLE if total_distance is None else total_distance


class ToyotaCurrentMonthSensor(StatisticsBaseEntity):
    """Class for current month statistics sensor."""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data[self.index].statistics.monthly[0]
        from_month = arrow.now().floor("month").format("MMMM")

        attributes = self.get_statistics_attributes(data.get(DATA, {}))
        attributes.update({"Month": from_month})

        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        total_distance = None
        data = self.coordinator.data[self.index].statistics.monthly[0]

        if DATA in data:
            total_distance = round(data[DATA][TOTAL_DISTANCE], 1)

        return STATE_UNAVAILABLE if total_distance is None else total_distance


class ToyotaCurrentYearSensor(StatisticsBaseEntity):
    """Class for current year statistics sensor."""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data[self.index].statistics.yearly[0]
        from_year = arrow.now().floor("year").format("YYYY")

        attributes = self.get_statistics_attributes(data.get(DATA, {}))
        attributes.update(
            {"Year": data[BUCKET]["year"] if BUCKET in data else from_year}
        )

        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        total_distance = None
        data = self.coordinator.data[self.index].statistics.yearly[0]

        if DATA in data:
            total_distance = round(data[DATA][TOTAL_DISTANCE], 1)

        return STATE_UNAVAILABLE if total_distance is None else total_distance
