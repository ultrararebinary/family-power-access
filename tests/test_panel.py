"""Tests for the Family Power Access Home Assistant panel."""

import pytest
from homeassistant.components import frontend
from homeassistant.components.frontend import DATA_PANELS
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.family_power_access import (
    async_setup,
    async_setup_entry,
)
from custom_components.family_power_access.const import (
    DOMAIN,
    HELLO_WORLD_UNIQUE_ID,
    NAME,
    PANEL_ELEMENT_NAME,
    PANEL_ICON,
    PANEL_MODULE_URL,
    PANEL_URL_PATH,
)


async def _setup_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Create and load one Family Power Access config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={},
        title=NAME,
        unique_id=HELLO_WORLD_UNIQUE_ID,
        version=1,
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_panel_is_registered_once_for_configured_entry(
    hass: HomeAssistant,
    frontend_panel_components: HomeAssistant,
) -> None:
    """The configured integration contributes one non-admin sidebar panel."""
    assert PANEL_URL_PATH not in hass.data.get(DATA_PANELS, {})

    entry = await _setup_entry(hass)

    panel = hass.data[DATA_PANELS][PANEL_URL_PATH]
    assert panel.sidebar_title == NAME
    assert panel.sidebar_icon == PANEL_ICON
    assert panel.frontend_url_path == PANEL_URL_PATH
    assert panel.require_admin is False
    assert panel.config["_panel_custom"] == {
        "name": PANEL_ELEMENT_NAME,
        "embed_iframe": False,
        "trust_external": False,
        "handle_safe_area": False,
        "module_url": PANEL_MODULE_URL,
    }
    assert entry.state is ConfigEntryState.LOADED


async def test_panel_is_removed_and_restored_on_reload(
    hass: HomeAssistant,
    frontend_panel_components: HomeAssistant,
) -> None:
    """Unloading removes the sidebar entry and reloading adds one panel again."""
    entry = await _setup_entry(hass)
    assert frontend.async_panel_exists(hass, PANEL_URL_PATH)

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert not frontend.async_panel_exists(hass, PANEL_URL_PATH)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert frontend.async_panel_exists(hass, PANEL_URL_PATH)
    assert list(hass.data[DATA_PANELS]).count(PANEL_URL_PATH) == 1


async def test_panel_setup_fails_without_overwriting_existing_panel(
    hass: HomeAssistant,
    frontend_panel_components: HomeAssistant,
) -> None:
    """A path collision fails visibly and leaves the other panel intact."""
    frontend.async_register_built_in_panel(
        hass,
        component_name="existing",
        sidebar_title="Existing panel",
        frontend_url_path=PANEL_URL_PATH,
    )
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={},
        title=NAME,
        unique_id=HELLO_WORLD_UNIQUE_ID,
        version=1,
    )

    await async_setup(hass, {})
    with pytest.raises((HomeAssistantError, ValueError), match="already registered"):
        await async_setup_entry(hass, entry)

    assert hass.data[DATA_PANELS][PANEL_URL_PATH].sidebar_title == "Existing panel"
