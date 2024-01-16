[![GitHub Workflow Status][workflow-shield]][workflow]
[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]
[![GitHub Activity][commits-shield]][commits]
[![Installs][installs-shield]][installs]

<p align="center">
    <img src="https://brands.home-assistant.io/_/toyota/icon@2x.png" alt="logo" height="200">
</p>

<h2 align="center">Toyota EU community integration</h2>

<p align="center">
    This custom integration aims to provide plug-and-play integration for your Toyota vehicle.
</p>

## About

This is a custom integration the retrieves' data from the
Toyota EU MyToyota ctpa-oneapi API and makes them available in Home Assistant as different types of sensors.
As there is no official API from Toyota, I will try my best to keep
it working, but there are no promises.

With Version 2.0.0 the toyota Custom Component only supports the new Toyota ctpa-oneapi API!
This means that this version is **no longer compatible** with your vehicle **if you are still using the old [MyT](https://play.google.com/store/apps/details?id=app.mytoyota.toyota.com.mytoyota) app**! Before updating, please make sure that you are already using the new [MyToyota](https://play.google.com/store/apps/details?id=com.toyota.oneapp.eu) app and that your vehicle has already been migrated to the new API.

**If you already have an installation of the custom component, make sure when updating to a version >= 2.0 to completely remove the previous installation from your Home Assistant devices and HACS!
You should then perform a reboot and can then reinstall the custom component via HACS again.**

## Features

Only Europe is supported.
See [here](https://github.com/widewing/ha-toyota-na) for North America.

**Disclaimer: Features available depends on your car model and year.**

### Overview

- VIN (Vehicle Identification Number) sensor
- Fuel, battery and odometer information
- Current day, week, month and year statistics.
- Door and door lock sensors, including hood and trunk sensor.

### Binary sensor(s)

| <div style="width:250px">Name</div>      | Description                                           |
| ---------------------------------------- | ----------------------------------------------------- |
| `binary_sensor.<you_car_alias>_hood`     | If the hood is open of not.                           |
| `binary_sensor.<you_car_alias>_*_door`   | Door sensors, one is created for each door and trunk. |
| `binary_sensor.<you_car_alias>_*_lock`   | Lock sensors, one is created for each door and trunk. |
| `binary_sensor.<you_car_alias>_*_window` | Window sensors, one is created for window.            |

### Device tracker(s)

| <div style="width:250px">Name</div> | Description                         |
| ----------------------------------- | ----------------------------------- |
| `device_tracker.<you_car_alias>`    | Shows you last parking information. |

### Sensor(s)

| <div style="width:250px">Name</div>          | Description                                        |
| -------------------------------------------- | -------------------------------------------------- |
| `sensor.<you_car_alias>_vin`                 | Static data about your car.                        |
| `sensor.<you_car_alias>_odometer`            | Odometer information.                              |
| `sensor.<you_car_alias>_fuel_level`          | Fuel level information.                            |
| `sensor.<you_car_alias>_fuel_range`          | Fuel range information.                            |
| `sensor.<you_car_alias>_battery_level`       | Battery level information.                         |
| `sensor.<you_car_alias>_battery_range`       | Battery range information.                         |
| `sensor.<you_car_alias>_battery_range_ac`    | Battery range information when AC is on.           |
| `sensor.<you_car_alias>_total_range`         | Information about combined fuel and battery range. |
| `sensor.<you_car_alias>_current_day_stats`   | Statistics for current day.                        |
| `sensor.<you_car_alias>_current_week_stats`  | Statistics for current week.                       |
| `sensor.<you_car_alias>_current_month_stats` | Statistics for current month.                      |
| `sensor.<you_car_alias>_current_year_stats`  | Statistics for current year.                       |

### Statistics sensors

#### Important

When starting a new week, month or year, it will not show any information before your first trip. Even though a new month starts on the 1, you will need to wait for the 2 of the month before it is able to show you current month stats. This due to a limitation in Toyota API. This limitation also applies to weeks.
Due to this, this integration will list sensors as unavailable when no data is available.

#### Attributes available

**Disclaimer: Attributes available depends on your car model and year.**

All values will show `None` if no data is available for the periode.

| Attribute               | Description                                                                     |
| ----------------------- | ------------------------------------------------------------------------------- |
| `Distance`              | Distance driven (Displayed as sensor value).                                    |
| `Average_speed`         | The average speed in the respective period (can be km/h or mph).                |
| `Countries`             | The countries travelled through in the respective period.                       |
| `Duration`              | The total driving time in the respective period.                                |
| `Total_fuel_consumed`   | The total fuel consumption in the respective period (can be litres or gallons). |
| `Average_fuel_consumed` | The average fuel consumption in the respective period (can be l/100km or mpg).  |
| `EV_distance`           | The driving distiance in EV mode in the respective period .                     |
| `EV_duration`           | The driving time in EV mode in the respective period .                          |
| `From_date`             | Start date of the calculation period.                                           |
| `To_date`               | End date of the calculation period.                                             |

## Getting started

### Prerequisites

Use Home Assistant build 2023.12 or above.

If you can confirm that it is working as advertised on older version please open a PR.

**Note:** It is **_only_** tested against latest, but should work on older versions too.

**Note:** Future updates may change which version are required.

### HACS installation (Recommended)

Open HACS and search for `Toyota Connected Services` under integrations.
You can choose to install a specific version or from master (Not recommended).

### Manual Installation

1. Open the directory with your Home Assistant configuration (where you find `configuration.yaml`,
   usually `~/.homeassistant/`).
2. If you do not have a `custom_components` directory there, you need to create it.

#### Git clone method

This is a preferred method of manual installation, because it allows you to keep the `git` functionality,
allowing you to manually install updates just by running `git pull origin master` from the created directory.

Now you can clone the repository somewhere else and symlink it to Home Assistant like so:

1. Clone the repo.

   ```shell
   git clone https://github.com/DurgNomis-drol/ha_toyota.git
   ```

2. Create the symlink to `toyota` in the configuration directory.
   If you have non-standard directory for configuration, use it instead.

   ```shell
   ln -s ha_toyota/custom_components/toyota ~/.homeassistant/custom_components/toyota
   ```

#### Copy method

1. Download [ZIP](https://github.com/DurgNomis-drol/ha_toyota/archive/master.zip) with the code.
2. Unpack it.
3. Copy the `custom_components/toyota/` from the unpacked archive to `custom_components`
   in your Home Assistant configuration directory.

### Integration Setup

- Browse to your Home Assistant instance.
- In the sidebar click on [Configuration](https://my.home-assistant.io/redirect/config).
- From the configuration menu select: [Integrations](https://my.home-assistant.io/redirect/integrations).
- In the bottom right, click on the [Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=toyota) button.
- From the list, search and select “Toyota Connected Services”.
- Follow the instruction on screen to complete the set-up.
- After completing, the Toyota Connected Services integration will be immediately available for use.

## Contribution

Contributions are more the welcome. This project uses `poetry` and `pre-commit` to make sure that
we use a unified coding style throughout the code. Poetry can be installed by running `poetry install`.
Please run `poetry run pre-commit run --all-files` and make sure that all tests passes before
opening a PR or committing to the PR. All PR's must pass all checks for them to get approved.

### License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Credits

Under the hood this integration uses the [mytoyota](https://github.com/DurgNomis-drol/mytoyota) python package.

[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/DurgNomis-drol/ha_toyota.svg?style=for-the-badge
[releases]: https://github.com/DurgNomis-drol/ha_toyota/releases
[workflow-shield]: https://img.shields.io/github/actions/workflow/status/DurgNomis-drol/ha_toyota/linting.yml?branch=master&style=for-the-badge
[workflow]: https://github.com/DurgNomis-drol/ha_toyota/actions
[installs-shield]: https://img.shields.io/endpoint?style=for-the-badge&url=https%3A%2F%2Ftoyota-installs-for-shield-io-b910bxm1lt58.runkit.sh%2F
[installs]: https://analytics.home-assistant.io/custom_integrations.json
[commits-shield]: https://img.shields.io/github/commit-activity/y/DurgNomis-drol/ha_toyota.svg?style=for-the-badge
[commits]: https://github.com/DurgNomis-drol/ha_toyota/commits/master
