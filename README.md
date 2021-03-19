<p align="center">
    <img src="https://logoeps.com/wp-content/uploads/2011/04/toyota-logo-vector.png" alt="logo" height="200">
</p>

<h2 align="center">Toyota community integration</h2>

<p align="center">
    This custom integration aims to provide plug-and-play integration for your Toyota vehicle.
</p>

**[!] Beta version alert.**
Please note this integration is in the early stage of its development.
See [Contribution](#contribution) section for more information on how to contribute.

## About

This is a custom component the retrieves' data from the
Toyota MyT API and makes them available in Home Assistant as sensors.
As there is no official API from Toyota, I will try my best to keep
it working but there are no promises.

## Features

This component will set up the following platforms:

| Platform         | Sample sensor           | Description                       |
| ---------------- | ----------------------- | --------------------------------- |
| `sensor`         | `sensor.aygo`           | Static data about your car        |
| `sensor`         | `sensor.aygo_fuel_tank` | Fuel tank information             |
| `sensor`         | `sensor.aygo_odometer`  | Odometer information              |
| `device_tracker` | `device_tracker.aygo`   | Shows you last parked information |

**Sensors displaying statistical information are coming soon...**

## Getting started

### Prerequisites

Use Home Assistant build 2021.3 or above.

If you can confirm that it is working as advertised on older version please open a PR.

**Note: It is _only_ tested against latest, but should work on older versions too.**

**Note: Future updates may change which version are required.**

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
