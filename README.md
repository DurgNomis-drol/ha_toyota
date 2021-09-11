[![GitHub Workflow Status][workflow-shield]][workflow]
[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]
[![Installs][installs-shield]][installs]

<p align="center">
    <img src="https://brands.home-assistant.io/_/toyota/icon@2x.png" alt="logo" height="200">
</p>

<h2 align="center">Toyota community integration</h2>

<p align="center">
    This custom integration aims to provide plug-and-play integration for your Toyota vehicle.
</p>

## About

This is a custom integration the retrieves' data from the
Toyota MyT API and makes them available in Home Assistant as different types of sensors.
As there is no official API from Toyota, I will try my best to keep
it working, but there are no promises.

## Features

Only Europe is supported right now. If you want to help add other regions, please open an issue over at [`mytoyota`](https://github.com/DurgNomis-drol/mytoyota).

This component will set up the following platforms:

| Platform         | Name                              | Description                       |
| ---------------- | --------------------------------- | --------------------------------- |
| `sensor`         | `sensor.aygo`                     | Static data about your car        |
| `sensor`         | `sensor.aygo_odometer`            | Odometer information              |
| `sensor`         | `sensor.aygo_fuel_tank`           | Fuel tank information             |
| `sensor`         | `sensor.aygo_starter_battery`     | Starter battery health            |
| `sensor`         | `sensor.aygo_current_week_stats`  | Statistics for current week       |
| `sensor`         | `sensor.aygo_current_month_stats` | Statistics for current month      |
| `sensor`         | `sensor.aygo_current_year_stats`  | Statistics for current year       |
| `device_tracker` | `device_tracker.aygo`             | Shows you last parked information |

### Notes about statistics sensors

Be aware that weeks start on Sundays and not Mondays. This is not possible to change due to limitation on Toyota's end.

When starting a new week, month or year, it will not show any information before your first trip. Even though a new month starts on the 1, you will need to wait for the 2 of the month before it is able to show you current month stats. This due to a limitation in Toyota API. This limitation also applies to weeks.
Due to this, this integration will list sensors as unavailable when no data is available.

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
   If you have non standard directory for configuration, use it instead.

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
- Follow the instruction on screen to complete the set up.
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
[workflow-shield]: https://img.shields.io/github/workflow/status/DurgNomis-drol/ha_toyota/Linting?style=for-the-badge
[workflow]: https://github.com/DurgNomis-drol/ha_toyota/actions
[installs-shield]: https://img.shields.io/endpoint?style=for-the-badge&url=https%3A%2F%2Ftoyota-installs-for-shield-io-b910bxm1lt58.runkit.sh%2F
[installs]: https://analytics.home-assistant.io/custom_integrations.json