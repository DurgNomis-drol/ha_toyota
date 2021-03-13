"""Config flow for Toyota Connected Services integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers import aiohttp_client

from .api import ToyotaApi
from .const import CONF_LOCALE, CONF_UUID

# https://github.com/PyCQA/pylint/issues/3202
from .const import DOMAIN  # pylint: disable=unused-import
from .toyota import ToyotaLocaleNotValid, ToyotaLoginError

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_LOCALE): str,
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
                session = aiohttp_client.async_get_clientsession(self.hass)
                client = ToyotaApi(
                    username=user_input[CONF_EMAIL],
                    password=user_input[CONF_PASSWORD],
                    locale=user_input[CONF_LOCALE],
                    session=session,
                )
                valid, token, uuid = await client.get_token_and_uuid()
                if valid:
                    data = user_input
                    data.update({CONF_API_TOKEN: token, CONF_UUID: uuid})

            except ToyotaLoginError as ex:
                errors["base"] = "invalid_auth"
                _LOGGER.error(ex)
            except ToyotaLocaleNotValid as ex:
                errors["base"] = "invalid_locale"
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
