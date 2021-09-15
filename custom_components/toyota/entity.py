"""Custom coordinator entity base classes for Toyota Connected Services integration"""

from datetime import timedelta

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorEntity
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    AVERAGE_SPEED,
    DOMAIN,
    EV_DISTANCE,
    EV_DISTANCE_PERCENTAGE,
    FUEL_CONSUMED,
    HYBRID,
    ICON_HISTORY,
    MAX_SPEED,
    MODEL,
    NIGHT_TRIPS,
    TOTAL_DURATION,
    TRIPS,
)


class ToyotaBaseEntity(CoordinatorEntity):
    """Defines a base Toyota entity."""

    _attr_state_class = STATE_CLASS_MEASUREMENT

    def __init__(self, coordinator, index, sensor_name):
        """Initialize the Toyota entity."""
        super().__init__(coordinator)
        self.index = index
        self.sensor_name = sensor_name

        self.vehicle = self.coordinator.data[self.index]

    @property
    def device_info(self):
        """Return device info for the Toyota entity."""
        return {
            "identifiers": {(DOMAIN, self.vehicle.vin)},
            "name": self.vehicle.alias,
            "model": self.vehicle.details[MODEL],
            "manufacturer": DOMAIN.capitalize(),
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.vehicle.alias} {self.sensor_name}"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vehicle.vin}/{self.name}"


class StatisticsBaseEntity(ToyotaBaseEntity, SensorEntity):
    """Builds on Toyota base entity"""

    _attr_icon = ICON_HISTORY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.vehicle.odometer.unit

    def format_statistics_attributes(self, statistics):
        """Formats and returns statistics attributes."""

        def get_average_fuel_consumed(fuel_data):
            if FUEL_CONSUMED in fuel_data:
                return round(fuel_data[FUEL_CONSUMED], 2)
            return STATE_UNAVAILABLE

        def get_timedelta(time):
            return str(timedelta(seconds=time))

        if statistics is not None:
            attributes = {
                "Average_fuel_consumed": get_average_fuel_consumed(statistics),
                "Number_of_trips": statistics[TRIPS],
                "Number_of_night_trips": statistics[NIGHT_TRIPS],
                "Total_driving_time": get_timedelta(statistics[TOTAL_DURATION]),
                "Average_speed": round(statistics[AVERAGE_SPEED], 1),
                "Max_speed": round(statistics[MAX_SPEED], 1),
            }

            if self.vehicle.details[HYBRID]:
                attributes.update(
                    {
                        "EV_distance_percentage": statistics[EV_DISTANCE_PERCENTAGE],
                        "EV_distance": round(statistics[EV_DISTANCE], 1),
                    }
                )
        else:
            attributes = {
                "Average_fuel_consumed": "0",
                "Number_of_trips": "0",
                "Number_of_night_trips": "0",
                "Total_driving_time": "0",
                "Average_speed": "0",
                "Max_speed": "0",
            }

            if self.vehicle.details[HYBRID]:
                attributes.update(
                    {
                        "EV_distance_percentage": "0",
                        "EV_distance": "0",
                    }
                )
        return attributes
