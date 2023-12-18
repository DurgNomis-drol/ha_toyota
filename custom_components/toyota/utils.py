"""Utilities for Toyota integration."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from .const import (
    AVERAGE_SPEED,
    COACHING_ADVICE,
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
    MAX_SPEED,
    NIGHT_TRIPS,
    TOTAL_DURATION,
    TRIPS,
)


def round_number(number: int | float | None, places: int = 0) -> int | float | None:
    """Round a number if it is not None."""
    return None if number is None else round(number, places)


def format_statistics_attributes(statistics: dict[str, Any], is_hybrid: bool):
    """Format and returns statistics attributes."""

    def get_timedelta(time):
        return str(timedelta(seconds=time))

    attr = {
        "Highway_distance": round(statistics.get(HIGHWAY_DISTANCE, 0), 1),
        "Highway_percentage": round(statistics.get(HIGHWAY_DISTANCE_PERCENTAGE, 0), 1),
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
                "Coaching_advice_most_occurrence": statistics.get(COACHING_ADVICE, 0),
            }
        )

    if DRIVER_SCORE in statistics:
        attr.update(
            {
                "Average_driver_score": round(statistics.get(DRIVER_SCORE, 0), 1),
                "Average_driver_score_accelerations": round(statistics.get(DRIVER_SCORE_ACCELERATIONS, 0), 1),
                "Average_driver_score_braking": round(statistics.get(DRIVER_SCORE_BRAKING, 0), 1),
            }
        )

    if is_hybrid:
        attr.update(
            {
                "EV_distance": round(statistics.get(EV_DISTANCE, 0), 1),
                "EV_driving_time": get_timedelta(statistics.get(EV_DURATION, 0)),
                "EV_distance_percentage": round(statistics.get(EV_DISTANCE_PERCENTAGE, 0), 1),
                "EV_duration_percentage": round(statistics.get(EV_DURATION_PERCENTAGE, 0), 1),
            }
        )

    return attr
