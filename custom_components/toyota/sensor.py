"""Platform for Toyota sensor integration."""
import arrow

from homeassistant.const import PERCENTAGE, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    BATTERY_HEALTH,
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

        fuel = self.coordinator.data[self.index][STATUS][ODOMETER][FUEL]
        return None if fuel is None else fuel


class ToyotaCurrentWeekSensor(StatisticsBaseEntity):
    """Class for current week statistics sensor."""

    _attr_last_reset = arrow.now().span("week", week_start=7)[0].datetime

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        from_dt = arrow.now().span("week", week_start=7)[0]

        statistics = self.coordinator.data[self.index][STATISTICS][WEEKLY]

        if from_dt == arrow.now():
            statistics = None

        attributes = self.format_statistics_attributes(statistics)
        attributes.update({"Weeknumber": from_dt.strftime("%V")})
        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""

        total_distance = None

        if self.coordinator.data[self.index][STATISTICS][WEEKLY] is not None:
            total_distance = round(
                self.coordinator.data[self.index][STATISTICS][WEEKLY][DATA][
                    TOTAL_DISTANCE
                ],
                1,
            )
        return STATE_UNAVAILABLE if total_distance is None else total_distance


class ToyotaCurrentMonthSensor(StatisticsBaseEntity):
    """Class for current month statistics sensor."""

    _attr_last_reset = arrow.now().floor("month").datetime

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        from_dt = arrow.now().floor("month")

        statistics = self.coordinator.data[self.index][STATISTICS][MONTHLY]

        if from_dt == arrow.now():
            statistics = None

        attributes = self.format_statistics_attributes(statistics)
        attributes.update({"Month": from_dt.format("MMMM")})

        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""

        total_distance = None

        if self.coordinator.data[self.index][STATISTICS][MONTHLY] is not None:
            total_distance = round(
                self.coordinator.data[self.index][STATISTICS][MONTHLY][DATA][
                    TOTAL_DISTANCE
                ],
                1,
            )
        return STATE_UNAVAILABLE if total_distance is None else total_distance


class ToyotaCurrentYearSensor(StatisticsBaseEntity):
    """Class for current year statistics sensor."""

    _attr_last_reset = arrow.now().floor("year").datetime

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        from_dt = arrow.now().floor("year")

        statistics = self.coordinator.data[self.index][STATISTICS][YEARLY]

        if from_dt == arrow.now():
            statistics = None

        attributes = self.format_statistics_attributes(statistics)
        attributes.update({"Year": from_dt.format("YYYY")})

        return attributes

    @property
    def state(self):
        """Return the state of the sensor."""

        total_distance = None

        if self.coordinator.data[self.index][STATISTICS][YEARLY] is not None:
            total_distance = round(
                self.coordinator.data[self.index][STATISTICS][YEARLY][DATA][
                    TOTAL_DISTANCE
                ],
                1,
            )
        return STATE_UNAVAILABLE if total_distance is None else total_distance
