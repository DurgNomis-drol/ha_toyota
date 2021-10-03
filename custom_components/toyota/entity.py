"""Custom coordinator entity base classes for Toyota Connected Services integration"""

from datetime import timedelta

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    AVERAGE_SPEED,
    COACHING_ADVICE,
    DOMAIN,
    DRIVER_SCORE,
    DRIVER_SCORE_ACCELERATIONS,
    DRIVER_SCORE_BRAKING,
    EV_DISTANCE,
    EV_DISTANCE_PERCENTAGE,
    EV_DURATION,
    EV_DURATION_PERCENTAGE,
    FUEL_CONSUMED,
    HARD_ACCELERATION,
    HARD_BRAKING,
    HIGHWAY_DISTANCE,
    HIGHWAY_DISTANCE_PERCENTAGE,
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
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.vehicle.odometer.unit

    def get_statistics_attributes(self, statistics):
        """Formats and returns statistics attributes."""

        def get_timedelta(time):
            return str(timedelta(seconds=time))

        attr = {
            "Highway_distance": round(statistics.get(HIGHWAY_DISTANCE, 0), 1),
            "Highway_percentage": round(
                statistics.get(HIGHWAY_DISTANCE_PERCENTAGE, 0), 1
            ),
            "Number_of_trips": statistics.get(TRIPS, 0),
            "Number_of_night_trips": statistics.get(NIGHT_TRIPS, 0),
            "Total_driving_time": get_timedelta(statistics.get(TOTAL_DURATION, 0)),
            "Average_speed": round(statistics.get(AVERAGE_SPEED, 0), 1),
            "Max_speed": round(statistics.get(MAX_SPEED, 0), 1),
            "Hard_acceleration_count": statistics.get(HARD_ACCELERATION, 0),
            "Hard_braking_count": statistics.get(HARD_BRAKING, 0),
        }

        if FUEL_CONSUMED in statistics:
            attr.update(
                {
                    "Average_fuel_consumed": round(statistics.get(FUEL_CONSUMED, 0), 2),
                }
            )

        if COACHING_ADVICE in statistics:
            attr.update(
                {
                    "Coaching_advice_most_occurrence": statistics.get(
                        COACHING_ADVICE, 0
                    ),
                }
            )

        if DRIVER_SCORE in statistics:
            attr.update(
                {
                    "Average_driver_score": round(statistics.get(DRIVER_SCORE, 0), 1),
                    "Average_driver_score_accelerations": round(
                        statistics.get(DRIVER_SCORE_ACCELERATIONS, 0), 1
                    ),
                    "Average_driver_score_braking": round(
                        statistics.get(DRIVER_SCORE_BRAKING, 0), 1
                    ),
                }
            )

        if self.vehicle.details[HYBRID]:
            attr.update(
                {
                    "EV_distance": round(statistics.get(EV_DISTANCE, 0), 1),
                    "EV_driving_time": get_timedelta(statistics.get(EV_DURATION, 0)),
                    "EV_distance_percentage": round(
                        statistics.get(EV_DISTANCE_PERCENTAGE, 0), 1
                    ),
                    "EV_duration_percentage": round(
                        statistics.get(EV_DURATION_PERCENTAGE, 0), 1
                    ),
                }
            )

        return attr
