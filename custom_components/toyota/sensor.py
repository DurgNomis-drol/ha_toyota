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
    ICON_HISTORY,
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
from .entity import ToyotaEntity


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform."""
    sensors = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):
        sensors.append(ToyotaCarSensor(coordinator, index))

        # If Connected Services is setup for the car, setup additional sensors
        if coordinator.data[index][SERVICES][CONNECTED_SERVICES]:
            sensors.append(ToyotaOdometerSensor(coordinator, index))
            if BATTERY_HEALTH in coordinator.data[index][DETAILS]:
                sensors.append(ToyotaStarterBatterySensor(coordinator, index))
            if FUEL in coordinator.data[index][STATUS][ODOMETER]:
                sensors.append(ToyotaFuelRemainingSensor(coordinator, index))

            # Statistics sensors
            sensors.append(ToyotaCurrentWeekSensor(coordinator, index))
            sensors.append(ToyotaCurrentMonthSensor(coordinator, index))
            sensors.append(ToyotaCurrentYearSensor(coordinator, index))

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
            license_plate = self.coordinator.data[self.index][DETAILS][LICENSE_PLATE]
            return None if license_plate is None else license_plate

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

        battery_health = (
            self.coordinator.data[self.index][DETAILS][BATTERY_HEALTH]
            .lower()
            .capitalize()
        )
        return None if battery_health is None else battery_health


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

        fuel = self.coordinator.data[self.index][STATUS][ODOMETER][FUEL]
        return None if fuel is None else fuel


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
        return self.mileage_unit

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_ODOMETER

    @property
    def state(self):
        """Return the state of the sensor."""

        mileage = self.coordinator.data[self.index][STATUS][ODOMETER][MILEAGE]
        return None if mileage is None else mileage


class ToyotaCurrentWeekSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} current week statistics"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/current_week_stats"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""

        from_dt = arrow.now().floor("week")

        attributes = self.format_statistics_attributes(
            self.coordinator.data[self.index][STATISTICS][WEEKLY]
        )
        attributes.update({"Weeknumber": from_dt.strftime("%V")})
        return attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.mileage_unit

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_HISTORY

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


class ToyotaCurrentMonthSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} current month statistics"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/current_month_stats"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""

        from_dt = arrow.now().floor("month")

        if from_dt == arrow.now():
            from_dt.shift(days=-1)

        attributes = self.format_statistics_attributes(
            self.coordinator.data[self.index][STATISTICS][MONTHLY]
        )
        attributes.update({"Month": from_dt.format("MMMM")})

        return attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.mileage_unit

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_HISTORY

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


class ToyotaCurrentYearSensor(ToyotaEntity):
    """Class for the fuel remaining sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} current year statistics"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/current_year_stats"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""

        from_dt = arrow.now().floor("year")

        if from_dt == arrow.now():
            from_dt.shift(days=-1)

        attributes = self.format_statistics_attributes(
            self.coordinator.data[self.index][STATISTICS][YEARLY]
        )
        attributes.update({"Year": from_dt.format("YYYY")})

        return attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.mileage_unit

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON_HISTORY

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
