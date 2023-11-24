"""Tests changes to common module."""
import json

from pytest_homeassistant_custom_component.common import load_fixture


def test_load_fixture():
    data = json.loads(load_fixture("gather_all_information.json"))
    assert data[0]["vin"] == "JTXXXXXXXXXXXXXXX"
