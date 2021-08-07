"""Custom coordinator entity base classes for Toyota Connected Services integration"""

from datetime import timedelta

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorEntity
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ALIAS,
    AVERAGE_SPEED,
    DATA,
    DETAILS,
    DOMAIN,
    EV_DISTANCE,
    EV_DISTANCE_PERCENTAGE,
    FUEL_CONSUMED,
    HYBRID,
    ICON_HISTORY,
    MAX_SPEED,
    MILEAGE_UNIT,
    MODEL,
    NIGHT_TRIPS,
    ODOMETER,
    STATUS,
    TOTAL_DURATION,
    TRIPS,
    VIN,
)


class ToyotaBaseEntity(CoordinatorEntity):
    """Defines a base Toyota entity."""

    def __init__(self, coordinator, index, sensor_name):
        """Initialize the Toyota entity."""
        super().__init__(coordinator)
        self.index = index
        self.sensor_name = sensor_name

        self.vin = self.coordinator.data[self.index][VIN]
        self.alias = self.coordinator.data[self.index][ALIAS]
        self.model = self.coordinator.data[self.index][DETAILS][MODEL]
        self.hybrid = self.coordinator.data[self.index][DETAILS][HYBRID]
        self.mileage_unit = ""
        if "odometer" in self.coordinator.data[self.index][STATUS]:
            self.mileage_unit = self.coordinator.data[self.index][STATUS][ODOMETER][
                MILEAGE_UNIT
            ]

    @property
    def device_info(self):
        """Return device info for the Toyota entity."""
        return {
            "identifiers": {(DOMAIN, self.vin)},
            "name": self.alias,
            "model": self.model,
            "manufacturer": DOMAIN.capitalize(),
            "Hybrid": self.hybrid,
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.alias} {self.sensor_name}"

    @property
    def unique_id(self):
        """Return a unique identifier for this entity."""
        return f"{self.vin}/{self.name}"


class StatisticsBaseEntity(ToyotaBaseEntity, SensorEntity):
    """Builds on Toyota base entity"""

    _attr_icon = ICON_HISTORY
    _attr_state_class = STATE_CLASS_MEASUREMENT

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.mileage_unit

    def format_statistics_attributes(self, statistics):
        """Formats and returns statistics attributes."""

        def get_average_fuel_consumed(fuel_data):
            if FUEL_CONSUMED in fuel_data:
                return fuel_data[FUEL_CONSUMED] + "/100" + self.mileage_unit
            return STATE_UNAVAILABLE

        def get_timedelta(time):
            return str(timedelta(seconds=time))

        if statistics is not None:
            attributes = {
                "Average_fuel_consumed": get_average_fuel_consumed(statistics[DATA]),
                "Number_of_trips": statistics[DATA][TRIPS],
                "Number_of_night_trips": statistics[DATA][NIGHT_TRIPS],
                "Total_driving_time": get_timedelta(statistics[DATA][TOTAL_DURATION]),
                "Average_speed": round(statistics[DATA][AVERAGE_SPEED], 1),
                "Max_speed": statistics[DATA][MAX_SPEED],
            }

            if self.hybrid:
                attributes.update(
                    {
                        "EV_distance_percentage": statistics[DATA][
                            EV_DISTANCE_PERCENTAGE
                        ],
                        "EV_distance": round(statistics[DATA][EV_DISTANCE], 1),
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

            if self.hybrid:
                attributes.update(
                    {
                        "EV_distance_percentage": "0",
                        "EV_distance": "0",
                    }
                )
        return attributes
