"""Custom coordinator entity base class for Toyota Connected Servers integration"""

from datetime import timedelta

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
    MAX_SPEED,
    MODEL,
    NIGHT_TRIPS,
    TOTAL_DURATION,
    TRIPS,
    VIN,
)


class ToyotaEntity(CoordinatorEntity):
    """Defines a base Toyota entity."""

    def __init__(self, coordinator, index):
        """Initialize the Toyota entity."""
        super().__init__(coordinator)
        self.index = index
        self.vin = self.coordinator.data[self.index][VIN]
        self.alias = self.coordinator.data[self.index][ALIAS]
        self.hybrid = self.coordinator.data[self.index][DETAILS][HYBRID]

    @property
    def device_info(self):
        """Return device info for the Toyota entity."""
        return {
            "identifiers": {(DOMAIN, self.vin)},
            "name": self.alias,
            "model": self.coordinator.data[self.index][DETAILS][MODEL],
            "manufacturer": "Toyota",
            "Hybrid": self.hybrid,
        }

    def format_statistics_attributes(self, statistics):
        """Formats and returns statistics attributes."""

        def get_fuel_consumed(fuel_data):
            if FUEL_CONSUMED in fuel_data:
                return fuel_data[FUEL_CONSUMED]
            return "Unavailable for this car."

        def get_timedelta(time):
            return str(timedelta(seconds=time))

        if statistics is not None:
            attributes = {
                "Total_fuel_consumed": get_fuel_consumed(statistics[DATA]),
                "Number_of_trips": statistics[DATA][TRIPS],
                "Number_of_night_trips": statistics[DATA][NIGHT_TRIPS],
                "Total_driving_time": get_timedelta(statistics[DATA][TOTAL_DURATION]),
                "Average_speed": round(statistics[DATA][AVERAGE_SPEED], 1),
                "Max_speed": statistics[DATA][MAX_SPEED],
            }

            if self.hybrid:
                attributes.update(
                    {
                        "EV_distance_percentage": statistics[DATA][EV_DISTANCE_PERCENTAGE],
                        "EV_distance": round(statistics[DATA][EV_DISTANCE], 1),
                    }
                )
        else:
            attributes = {
                "Total_fuel_consumed": "0",
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
