"""Sensor platform for Toyota sensor integration."""
import arrow

from homeassistant.const import PERCENTAGE, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    BATTERY_HEALTH,
    BUCKET,
    CONNECTED_SERVICES,
    DATA,
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
    MONTHLY,
    ODOMETER,
    SERVICES,
    STATISTICS,
    STATUS,
    TOTAL_DISTANCE,
    WEEKLY,
    YEARLY,
)
from .entity import StatisticsBaseEntity, ToyotaBaseEntity


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):
        sensors.append(ToyotaCarSensor(coordinator, index, "numberplate"))

        # If Connected Services is setup for the car, setup additional sensors
        if coordinator.data[index][SERVICES][CONNECTED_SERVICES]:
            sensors.append(ToyotaOdometerSensor(coordinator, index, "odometer"))
            if BATTERY_HEALTH in coordinator.data[index][DETAILS]:
                sensors.append(
                    ToyotaStarterBatterySensor(
                        coordinator, index, "starter battery health"
                    )
                )
            if FUEL in coordinator.data[index][STATUS][ODOMETER]:
                sensors.append(
                    ToyotaFuelRemainingSensor(coordinator, index, "fuel tank")
                )

            # Statistics sensors
            sensors.append(
                ToyotaCurrentWeekSensor(coordinator, index, "current week statistics")
            )
            sensors.append(
                ToyotaCurrentMonthSensor(coordinator, index, "current month statistics")
            )
            sensors.append(
                ToyotaCurrentYearSensor(coordinator, index, "current year statistics")
            )

    async_add_devices(sensors, True)


class ToyotaCarSensor(ToyotaBaseEntity):
    """Class for car details and numberplate sensor."""

    _attr_icon = ICON_CAR

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data[self.index][DETAILS]

    @property
    def state(self):
        """Return the state of the sensor."""
        if LICENSE_PLATE in self.coordinator.data[self.index][DETAILS]:
            license_plate = self.coordinator.data[self.index][DETAILS][LICENSE_PLATE]
            return None if license_plate is None else license_plate

        return STATE_UNKNOWN


class ToyotaOdometerSensor(ToyotaBaseEntity):
    """Class for the odometer sensor."""

    _attr_icon = ICON_ODOMETER

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.mileage_unit

    @property
    def state(self):
        """Return the state of the sensor."""
        mileage = None

        if ODOMETER in self.coordinator.data[self.index][STATUS]:
            mileage = self.coordinator.data[self.index][STATUS][ODOMETER][MILEAGE]
        return None if mileage is None else mileage


class ToyotaStarterBatterySensor(ToyotaBaseEntity):
    """Class for the starter battery health sensor."""

    _attr_icon = ICON_BATTERY

    @property
    def state(self):
        """Return the state of the sensor."""

        battery_health = (
            self.coordinator.data[self.index][DETAILS][BATTERY_HEALTH]
            .lower()
            .capitalize()
        )
        return None if battery_health is None else battery_health


class ToyotaFuelRemainingSensor(ToyotaBaseEntity):
    """Class for the fuel remaining sensor."""

    _attr_icon = ICON_FUEL
    _attr_unit_of_measurement = PERCENTAGE

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            FUEL_TYPE: self.coordinator.data[self.index][DETAILS][FUEL_TYPE],
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        fuel = None

        if ODOMETER in self.coordinator.data[self.index][STATUS]:
            fuel = self.coordinator.data[self.index][STATUS][ODOMETER][FUEL]
        return None if fuel is None else fuel


class ToyotaCurrentWeekSensor(StatisticsBaseEntity):
    """Class for current week statistics sensor."""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        statistics = None
        data = self.coordinator.data[self.index][STATISTICS][WEEKLY][0]
        from_dt = arrow.now().floor("week").format("YYYY-MM-DD")
        to_dt = arrow.now().ceil("week").format("YYYY-MM-DD")

        if DATA in data:
            statistics = data[DATA]

        attributes = self.format_statistics_attributes(statistics)
        attributes.update(
            {
                "From": data[BUCKET]["week_start"] if BUCKET in data else from_dt,
                "To": to_dt,
            }
        )
        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        total_distance = None
        data = self.coordinator.data[self.index][STATISTICS][WEEKLY][0]

        if DATA in data:
            total_distance = round(data[DATA][TOTAL_DISTANCE], 1)

        return STATE_UNAVAILABLE if total_distance is None else total_distance


class ToyotaCurrentMonthSensor(StatisticsBaseEntity):
    """Class for current month statistics sensor."""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        statistics = None
        data = self.coordinator.data[self.index][STATISTICS][MONTHLY][0]
        from_month = arrow.now().floor("month").format("MMMM")

        if DATA in data:
            statistics = data[DATA]

        attributes = self.format_statistics_attributes(statistics)
        attributes.update({"Month": from_month})

        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        total_distance = None
        data = self.coordinator.data[self.index][STATISTICS][MONTHLY][0]

        if DATA in data:
            total_distance = round(data[DATA][TOTAL_DISTANCE], 1)

        return STATE_UNAVAILABLE if total_distance is None else total_distance


class ToyotaCurrentYearSensor(StatisticsBaseEntity):
    """Class for current year statistics sensor."""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        statistics = None
        data = self.coordinator.data[self.index][STATISTICS][YEARLY][0]
        from_year = arrow.now().floor("year").format("YYYY-MM-DD")

        if DATA in data:
            statistics = data[DATA]

        attributes = self.format_statistics_attributes(statistics)
        attributes.update(
            {"Year": data[BUCKET]["year"] if BUCKET in data else from_year}
        )

        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        total_distance = None
        data = self.coordinator.data[self.index][STATISTICS][YEARLY][0]

        if DATA in data:
            total_distance = round(data[DATA][TOTAL_DISTANCE], 1)

        return STATE_UNAVAILABLE if total_distance is None else total_distance
