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
Toyota EU MyT API and makes them available in Home Assistant as different types of sensors.
As there is no official API from Toyota, I will try my best to keep
it working, but there are no promises.

## Features

Only Europe is supported.
See [here](https://github.com/widewing/ha-toyota-na) for North America.

**Disclaimer: Features available depends on your car model and year.**

### Overview

- Numberplate and starter battery sensors
- Fuel, battery and odometer information
- Current week, month and year statistics.
- HVAC, Window and lights sensors
- Door and door lock sensors, including hood and trunk sensor.
- Is key in car and over all status sensor.

### Binary sensor(s)

| <div style="width:250px">Name</div>     | Description                                                                         |
| --------------------------------------- | ----------------------------------------------------------------------------------- |
| `binary_sensor.corolla_hood`            | If the hood is open of not.                                                         |
| `binary_sensor.corolla_*_defogger`      | Defogger is on sensor, one is created for front and rear if available               |
| `binary_sensor.corolla_*_door`          | Door sensor, one is created for each door and trunk.                                |
| `binary_sensor.corolla_*_lock`          | Lock sensor, one is created for each door and trunk.                                |
| `binary_sensor.corolla_*_lights`        | Light sensor, one is created for front, back and hazard lights.                     |
| `binary_sensor.corolla_over_all_status` | Over all status of the vehicle, if warning is true for a sensor, this will show it. |
| `binary_sensor.corolla_key_in_car`      | If key is in the car.                                                               |
| `binary_sensor.corolla_*_window`        | Window sensor, one is created for window.                                           |

### Device tracker(s)

| <div style="width:250px">Name</div> | Description                        |
| ----------------------------------- | ---------------------------------- |
| `device_tracker.corolla`            | Shows you last parked information. |

### Sensor(s)

| <div style="width:250px">Name</div>  | Description                                                              |
| ------------------------------------ | ------------------------------------------------------------------------ |
| `sensor.corolla`                     | Static data about your car.                                              |
| `sensor.corolla_ev_battery_status`   | EV battery information                                                   |
| `sensor.corolla_ev_remaining_charge` | EV battery remaining charge (in per cent of full capacity)               |
| `sensor.corolla_fuel_tank`           | Fuel tank information.                                                   |
| `sensor.corolla_hvac`                | HVAC sensor showing current and target temperature, including other data |
| `sensor.corolla_odometer`            | Odometer information.                                                    |
| `sensor.corolla_range`               | Remaining range sensor                                                   |
| `sensor.aygo_starter_battery`        | Starter battery health.                                                  |
| `sensor.corolla_current_week_stats`  | Statistics for current week.                                             |
| `sensor.corolla_current_month_stats` | Statistics for current month.                                            |
| `sensor.corolla_current_year_stats`  | Statistics for current year.                                             |

### Statistics sensors

#### Important

When starting a new week, month or year, it will not show any information before your first trip. Even though a new month starts on the 1, you will need to wait for the 2 of the month before it is able to show you current month stats. This due to a limitation in Toyota API. This limitation also applies to weeks.
Due to this, this integration will list sensors as unavailable when no data is available.

#### Attributes available

**Disclaimer: Attributes available depends on your car model and year.**

All values will show zero if no data is available for the periode.

| Attribute                            | Description                                                                                         |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `Highway_distance`                   | Distance driven on Highway/Motorway.                                                                |
| `Highway_percentage`                 | Percentage driven on Highway/Motorway.                                                              |
| `Number_of_trips`                    | Number of trips performed. A trip is started when you start the engine.                             |
| `Number_of_night_trips`              | Number of trips performed at night.                                                                 |
| `Total_driving_time`                 | Total time driven.                                                                                  |
| `Average_speed`                      | Average speed.                                                                                      |
| `Max_speed`                          | Max speed achieved.                                                                                 |
| `Hard_acceleration_count`            | Hard accelerations counter. Can be very sensitive.                                                  |
| `Hard_braking_count`                 | Hard braking counter. Can be very sensitive.                                                        |
| `Average_fuel_consumed`              | Average fuel consumed. If car is in km then this will show L/100km. If in mi then it will show Mpg. |
| `Coaching_advice_most_occurrence`    | Coaching advice most occurrence.                                                                    |
| `Average_driver_score`               | Average driver score.                                                                               |
| `Average_driver_score_accelerations` | Average driver score for accelerations.                                                             |
| `Average_driver_score_braking`       | Average driver score for braking.                                                                   |
| `EV_distance`                        | Distance which have been driven on electric.                                                        |
| `EV_distance_percentage`             | Percentage of the distance driven on electric.                                                      |
| `EV_driving_time`                    | Driving time on electric.                                                                           |
| `EV_duration_percentage`             | Percentage of the driving time on electric.                                                         |

## Getting started

### Prerequisites

Use Home Assistant build 2021.4 or above.

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
