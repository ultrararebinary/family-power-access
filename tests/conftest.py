"""Shared Home Assistant fixtures for Family Power Access."""

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
def load_custom_integrations(enable_custom_integrations: None) -> None:
    """Permit Home Assistant to load this repository's custom integration."""


@pytest.fixture
async def frontend_panel_components(hass: HomeAssistant) -> HomeAssistant:
    """Load the Home Assistant frontend and panel components for panel tests."""
    assert await async_setup_component(hass, "frontend", {})
    assert await async_setup_component(hass, "panel_custom", {})
    await hass.async_block_till_done()
    return hass
