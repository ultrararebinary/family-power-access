"""Tests for the Family Power Access config flow."""

from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.family_power_access.const import (
    DOMAIN,
    HELLO_WORLD_UNIQUE_ID,
    NAME,
)


async def test_user_step_shows_empty_form(hass: HomeAssistant) -> None:
    """The user flow starts with a confirmation form without fields."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}
    assert result["data_schema"] is not None
    assert list(result["data_schema"].schema) == []


async def test_user_step_creates_empty_entry(hass: HomeAssistant) -> None:
    """Submitting the empty form creates the single config entry."""
    form = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    result = await hass.config_entries.flow.async_configure(form["flow_id"], {})

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == NAME
    assert result["data"] == {}

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert entry.version == 1
    assert entry.unique_id == HELLO_WORLD_UNIQUE_ID


async def test_user_step_rejects_second_entry(hass: HomeAssistant) -> None:
    """The integration can only be configured once."""
    form = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )
    await hass.config_entries.flow.async_configure(form["flow_id"], {})

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
