"""Test the Simple Integration config flow."""
import pytest
import voluptuous as vol
from homeassistant import config_entries, setup
from homeassistant.helpers.selector import SelectSelector

from custom_components.toyota.const import DOMAIN


@pytest.mark.asyncio
async def test_config_form(hass):
    # When
    await setup.async_setup_component(hass, "persistent_notification", {})
    setup_result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Then
    assert setup_result["type"] == "form"
    assert setup_result["handler"] == DOMAIN
    assert setup_result["errors"] == {}

    data_schema: vol.Schema = setup_result["data_schema"]
    region_select: SelectSelector = data_schema.schema["region"]
    region = region_select.__dict__
    assert region["container"] == ["Europe"]

    await hass.async_block_till_done()
