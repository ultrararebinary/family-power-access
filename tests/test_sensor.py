"""Tests for the Family Power Access Hello World sensor."""

from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import STATE_UNAVAILABLE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.family_power_access.const import (
    DOMAIN,
    HELLO_WORLD_UNIQUE_ID,
    NAME,
)

ENTITY_ID = "sensor.hello_world"


async def _setup_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Create and load the integration config entry."""
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


async def test_sensor_exposes_hello_world_value_and_unique_id(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
) -> None:
    """The integration creates the static Hello World sensor."""
    entry = await _setup_entry(hass)

    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.state == "Hello World"
    assert state.attributes["friendly_name"] == "Hello World"

    registry_entry = entity_registry.async_get(ENTITY_ID)
    assert registry_entry is not None
    assert registry_entry.config_entry_id == entry.entry_id
    assert registry_entry.domain == Platform.SENSOR
    assert registry_entry.platform == DOMAIN
    assert registry_entry.unique_id == HELLO_WORLD_UNIQUE_ID


async def test_sensor_unloads_with_config_entry(hass: HomeAssistant) -> None:
    """Unloading the config entry removes the active sensor state."""
    entry = await _setup_entry(hass)
    assert hass.states.get(ENTITY_ID) is not None

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.state == STATE_UNAVAILABLE
    assert state.attributes["restored"] is True


async def test_sensor_unique_id_survives_reload(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
) -> None:
    """Reloading the entry recreates the sensor with the same unique id."""
    entry = await _setup_entry(hass)
    first_registry_entry = entity_registry.async_get(ENTITY_ID)
    assert first_registry_entry is not None

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.state == "Hello World"

    second_registry_entry = entity_registry.async_get(ENTITY_ID)
    assert second_registry_entry is not None
    assert second_registry_entry.id == first_registry_entry.id
    assert second_registry_entry.unique_id == HELLO_WORLD_UNIQUE_ID


async def test_sensor_setup_does_not_contact_github(hass: HomeAssistant) -> None:
    """The Hello World sensor loads without making outbound HTTP calls."""
    with patch("aiohttp.ClientSession.request") as request:
        await _setup_entry(hass)

    request.assert_not_called()
