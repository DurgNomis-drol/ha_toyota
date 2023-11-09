"""Sensor platform for Toyota sensor integration."""
import arrow
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    BATTERY_HEALTH,
    BUCKET,
    DATA,
    DATA_COORDINATOR,
    DOMAIN,
    FUEL_TYPE,
    ICON_BATTERY,
    ICON_CAR,
    ICON_EV,
    ICON_EV_BATTERY,
    ICON_FUEL,
    ICON_ODOMETER,
    ICON_RANGE,
    LAST_UPDATED,
    LICENSE_PLATE,
    PERIODE_START,
    TOTAL_DISTANCE,
)
from .entity import StatisticsBaseEntity, ToyotaBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
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
            if vehicle.energy.level:
                sensors.append(
                    ToyotaFuelRemainingSensor(coordinator, index, "fuel tank")
                )

            if vehicle.energy.range:
                sensors.append(ToyotaRangeSensor(coordinator, index, "range"))

            if vehicle.energy.chargeinfo:
                sensors.append(ToyotaEVSensor(coordinator, index, "EV battery status"))
                sensors.append(
                    ToyotaEVBatterySensor(coordinator, index, "EV remaining charge")
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

            if vehicle.hvac:
                sensors.append(ToyotaHVACSensor(coordinator, index, "hvac"))

    async_add_entities(sensors, True)


class ToyotaCarSensor(ToyotaBaseEntity):
    """Class for car details and numberplate sensor."""

    _attr_icon = ICON_CAR
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data[self.index].details

    @property
    def state(self) -> StateType:
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
    def state(self) -> StateType:
        """Return the state of the sensor."""
        mileage = None

        if self.coordinator.data[self.index].odometer:
            mileage = self.coordinator.data[self.index].odometer.mileage
        return None if mileage is None else mileage


class ToyotaStarterBatterySensor(ToyotaBaseEntity):
    """Class for the starter battery health sensor."""

    _attr_icon = ICON_BATTERY

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""

        return (
            self.coordinator.data[self.index]
            .details[BATTERY_HEALTH]
            .lower()
            .capitalize()
        )


class ToyotaFuelRemainingSensor(ToyotaBaseEntity):
    """Class for the fuel/energy remaining sensor."""

    _attr_icon = ICON_FUEL
    _attr_unit_of_measurement = PERCENTAGE

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            FUEL_TYPE: self.vehicle.energy.type,
        }

    @property
    def state(self) -> StateType:
        """Return fuellevel/battery capacity of the vehicle."""
        level = self.coordinator.data[self.index].energy.level
        return round(level, 1) if level else None


class ToyotaRangeSensor(ToyotaBaseEntity):
    """Class for range sensor."""

    _attr_icon = ICON_RANGE

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.vehicle.odometer.unit

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "Range_with_aircon_on": self.coordinator.data[
                self.index
            ].energy.range_with_aircon,
            LAST_UPDATED: self.coordinator.data[self.index].energy.last_updated,
        }

    @property
    def state(self):
        """Return remaining range."""

        return self.coordinator.data[self.index].energy.range


class ToyotaEVSensor(ToyotaBaseEntity):
    """Class for EV sensor."""

    _attr_icon = ICON_EV

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        return {
            "Start_time": self.coordinator.data[self.index].energy.chargeinfo.get(
                "start_time", None
            ),
            "End_time": self.coordinator.data[self.index].energy.chargeinfo.get(
                "end_time", None
            ),
            "Remaining_time": self.coordinator.data[self.index].energy.chargeinfo.get(
                "remaining_time", None
            ),
        }

    @property
    def state(self):
        """Return battery information for EV's."""

        return self.coordinator.data[self.index].energy.chargeinfo.get("status", None)


class ToyotaEVBatterySensor(ToyotaBaseEntity):
    """Class for EV battery sensor."""

    _attr_icon = ICON_EV_BATTERY
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_unit_of_measurement = PERCENTAGE

    @property
    def state(self) -> StateType:
        """Return remaining charge of the EV battery."""
        level = self.coordinator.data[self.index].energy.chargeinfo.get(
            "remaining_amount", None
        )
        return round(level, 0) if level else None


class ToyotaHVACSensor(ToyotaBaseEntity):
    """Class for hvac temperature sensor"""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        hvac = self.coordinator.data[self.index].hvac

        attributes = {
            "target_temperature": hvac.target_temperature,
            LAST_UPDATED: hvac.last_updated,
            "legacy": hvac.legacy,
        }

        if hvac.legacy:
            attributes["blower_status"] = hvac.blower_on
        else:
            attributes |= {
                "started_at": hvac.started_at,
                "status": hvac.status,
                "type": hvac.type,
                "duration": hvac.duration,
                "options": hvac.options,
                "command_id": hvac.options,
            }

        return attributes

    @property
    def native_value(self):
        """Return current temperature."""
        return self.coordinator.data[self.index].hvac.current_temperature


class ToyotaTargetTemperatureSensor(ToyotaBaseEntity):
    """Class for hvac temperature sensor"""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS

    @property
    def native_value(self):
        """Return current temperature."""
        return self.coordinator.data[self.index].hvac.target_temperature


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
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data[self.index].statistics.weekly[0]

        total_distance = round(data[DATA][TOTAL_DISTANCE], 1) if DATA in data else None
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
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data[self.index].statistics.monthly[0]

        total_distance = round(data[DATA][TOTAL_DISTANCE], 1) if DATA in data else None
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
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data[self.index].statistics.yearly[0]

        total_distance = round(data[DATA][TOTAL_DISTANCE], 1) if DATA in data else None
        return STATE_UNAVAILABLE if total_distance is None else total_distance
