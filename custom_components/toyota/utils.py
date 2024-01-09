"""Utilities for Toyota integration."""
from __future__ import annotations

from mytoyota.models.endpoints.vehicle_guid import VehicleGuidModel
from mytoyota.models.summary import Summary


def round_number(number: int | float | None, places: int = 0) -> int | float | None:
    """Round a number if it is not None."""
    return None if number is None else round(number, places)


def format_statistics_attributes(statistics: Summary, vehicle_info: VehicleGuidModel):
    """Format and returns statistics attributes."""
    attr = {
        "Average_speed": round(statistics.average_speed, 1) if statistics.average_speed else None,
        "Countries": statistics.countries or [],
    }

    if vehicle_info.fuel_type is not None:
        attr["Fuel_consumed"] = round(statistics.fuel_consumed, 3) if statistics.fuel_consumed else None

    if vehicle_info.electrical_platform_code == 15 or vehicle_info.ev_vehicle is True:
        attr.update(
            {
                "EV_distance": round(statistics.ev_distance, 1) if statistics.ev_distance else None,
                "EV_duration": str(statistics.ev_duration),
            }
        )

    attr.update(
        {
            "From_date": statistics.from_date.strftime("%Y-%m-%d"),
            "To_date": statistics.to_date.strftime("%Y-%m-%d"),
        }
    )

    return attr
