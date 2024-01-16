## Toyota Connected Services Europe

This custom integration aims to provide plug-and-play integration for your Toyota vehicle.

With Version 2.0.0 the toyota Custom Component only supports the new Toyota ctpa-oneapi API!
This means that this version is **no longer compatible** with your vehicle **if you are still using the old [MyT](https://play.google.com/store/apps/details?id=app.mytoyota.toyota.com.mytoyota) app**! Before updating, please make sure that you are already using the new [MyToyota](https://play.google.com/store/apps/details?id=com.toyota.oneapp.eu) app and that your vehicle has already been migrated to the new API.

**If you already have an installation of the custom component, make sure when updating to a version >= 2.0 to completely remove the previous installation from your Home Assistant devices and HACS!
You should then perform a reboot and can then reinstall the custom component via HACS again.**

### Features

**Only Europe is supported**
**Disclaimer: Features available depends on your car model and year.**

- Battery/fuel remaining sensors.
- Read your odometer to see how far your car haven driven totally.
- See your vin and other details about your car.
- Daily, weekly, monthly and yearly statistics.
- Door and door lock sensors, including hood and trunk sensor.
- And more...

See [features](https://github.com/DurgNomis-drol/ha_toyota#binary-sensors) section for more details

### Installations

Go to: Settings -> Integrations -> Add integration and search for Toyota Connected Services.

[Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=toyota)

### Help is need to

- Implement Lock and HVAC control.
- Add support for other regions.

#### [Docs (installation, config, and issues)](https://github.com/DurgNomis-drol/ha_toyota)
