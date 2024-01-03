"""Config flow for Toyota Connected Services integration."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from mytoyota.client import MyT
from mytoyota.exceptions import ToyotaInvalidUsernameError, ToyotaLoginError

# https://github.com/PyCQA/pylint/issues/3202
from .const import CONF_METRIC_VALUES, DOMAIN  # pylint: disable=unused-import

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class ToyotaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Toyota Connected Services."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_EMAIL].lower())

            try:
                client = MyT(
                    username=user_input[CONF_EMAIL],
                    password=user_input[CONF_PASSWORD],
                )

                await client.login()

            except ToyotaLoginError as ex:
                errors["base"] = "invalid_auth"
                _LOGGER.error(ex)
            except ToyotaInvalidUsernameError as ex:
                errors["base"] = "invalid_username"
                _LOGGER.error(ex)
            except Exception as ex:  # pylint: disable=broad-except
                errors["base"] = "unknown"
                _LOGGER.error("An unknown error occurred during login request: %s", ex)
            else:
                return self.async_create_entry(title=user_input[CONF_EMAIL], data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get async options flow."""
        return ToyotaOptionsFlowHandler(config_entry)


class ToyotaOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for Toyota Connected Services."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(title=self.config_entry.data.get(CONF_EMAIL), data=self.options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_METRIC_VALUES,
                        default=self.config_entry.options.get(CONF_METRIC_VALUES, True),
                    ): bool,
                }
            ),
        )
