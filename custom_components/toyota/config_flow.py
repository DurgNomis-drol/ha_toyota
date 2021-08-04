"""Config flow for Toyota Connected Services integration."""
import logging

from mytoyota.client import MyT
from mytoyota.exceptions import (
    ToyotaInvalidUsername,
    ToyotaLocaleNotValid,
    ToyotaLoginError,
    ToyotaRegionNotSupported,
)
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_REGION

from .const import CONF_LOCALE

# https://github.com/PyCQA/pylint/issues/3202
from .const import DOMAIN  # pylint: disable=unused-import

_LOGGER = logging.getLogger(__name__)

supported_regions = MyT.get_supported_regions()

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_LOCALE): str,
        vol.Required(CONF_REGION): vol.In(
            [region.capitalize() for region in supported_regions]
        ),
    }
)


class MazdaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Toyota Connected Services."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_EMAIL].lower())

            try:
                locale = user_input[CONF_LOCALE]
                region = user_input[CONF_REGION]

                client = MyT(
                    username=user_input[CONF_EMAIL],
                    password=user_input[CONF_PASSWORD],
                    locale=locale.lower(),
                    region=region.lower(),
                )

                await client.login()

            except ToyotaLoginError as ex:
                errors["base"] = "invalid_auth"
                _LOGGER.error(ex)
            except ToyotaLocaleNotValid as ex:
                errors["base"] = "invalid_locale"
                _LOGGER.error(ex)
            except ToyotaRegionNotSupported as ex:
                errors["base"] = "region_not_supported"
                _LOGGER.error("Region not supported - %s", ex)
            except ToyotaInvalidUsername as ex:
                errors["base"] = "invalid_username"
                _LOGGER.error(ex)
            except Exception as ex:  # pylint: disable=broad-except
                errors["base"] = "unknown"
                _LOGGER.error("An unknown error occurred during login request: %s", ex)
            else:
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
