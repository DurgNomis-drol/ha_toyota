import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.area_registry import AreaRegistry
from homeassistant.helpers.device_registry import DeviceRegistry
from homeassistant.helpers.entity_registry import EntityRegistry
from pytest_homeassistant_custom_component.common import (
    mock_area_registry,
    mock_device_registry,
    mock_registry,
)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: bool) -> None:
    yield


@pytest.fixture
def enable_custom_integrations(hass: HomeAssistant) -> None:
    """Enable custom integrations defined in the test dir."""
    # hass.data.pop(loader.DATA_CUSTOM_COMPONENTS)


@pytest.fixture
def area_reg(hass: HomeAssistant) -> AreaRegistry:
    """Return an empty, loaded, registry."""
    return mock_area_registry(hass)


@pytest.fixture
def device_reg(hass: HomeAssistant) -> DeviceRegistry:
    """Return an empty, loaded, registry."""
    return mock_device_registry(hass)


@pytest.fixture
def entity_reg(hass: HomeAssistant) -> EntityRegistry:
    """Return an empty, loaded, registry."""
    return mock_registry(hass)
