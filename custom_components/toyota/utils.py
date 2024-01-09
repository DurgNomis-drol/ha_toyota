"""Utilities for Toyota integration."""
from __future__ import annotations

from typing import Optional, Union

from mytoyota.models.endpoints.vehicle_guid import VehicleGuidModel
from mytoyota.models.summary import Summary


def round_number(number: int | float | None, places: int = 0) -> int | float | None:
    """Round a number if it is not None."""
    return None if number is None else round(number, places)


def mask_string(string: str) -> str:
    """Mask all except the last 5 digits of a given string with asteriks."""
    return "*" * (len(string) - 5) + string[-5:] if len(string) >= 5 else "*****"


def format_vin_sensor_attributes(
    vehicle_info: VehicleGuidModel,
) -> dict[str, Optional[Union[str, bool, dict[str, bool]]]]:
    """Format and returns vin sensor attributes."""
    return {
        "Vin": mask_string(vehicle_info.vin),
        "Contract_id": mask_string(vehicle_info.contract_id),
        "Katashiki_code": mask_string(vehicle_info.katashiki_code),
        "ASI_code": vehicle_info.asi_code,
        "IMEI": mask_string(vehicle_info.imei),
        "Brand": vehicle_info.brand,
        "Car_line_name": vehicle_info.car_line_name,
        "Car_model_year": vehicle_info.car_model_year,
        "Car_model_name": vehicle_info.car_model_name,
        "Color": vehicle_info.color,
        "Generation": vehicle_info.generation,
        "Manufactured_date": None
        if vehicle_info.manufactured_date is None
        else vehicle_info.manufactured_date.strftime("%Y-%m-%d"),
        "Date_of_first_use": None
        if vehicle_info.date_of_first_use is None
        else vehicle_info.date_of_first_use.strftime("%Y-%m-%d"),
        "Transmission_type": vehicle_info.transmission_type,
        "Fuel_type": vehicle_info.fuel_type,
        "Electrical_platform_code": vehicle_info.electrical_platform_code,
        "EV_vehicle": vehicle_info.ev_vehicle,
        "Features": {
            key: value for key, value in vehicle_info.features.dict().items() if value is True
        },
        "Extended_capabilities": {
            key: value
            for key, value in vehicle_info.extended_capabilities.dict().items()
            if value is True
        },
        "Remote_service_capabilities": {
            key: value
            for key, value in vehicle_info.remote_service_capabilities.dict().items()
            if value is True
        },
    }


def format_statistics_attributes(
    statistics: Summary, vehicle_info: VehicleGuidModel
) -> dict[str, Optional[str]]:
    """Format and returns statistics attributes."""
    attr = {
        "Average_speed": round(statistics.average_speed, 1) if statistics.average_speed else None,
        "Countries": statistics.countries or [],
    }

    if vehicle_info.fuel_type is not None:
        attr["Fuel_consumed"] = (
            round(statistics.fuel_consumed, 3) if statistics.fuel_consumed else None
        )

    if vehicle_info.electrical_platform_code == 15 or vehicle_info.ev_vehicle is True:
        attr.update(
            {
                "EV_distance": round(statistics.ev_distance, 1)
                if statistics.ev_distance
                else None,
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
