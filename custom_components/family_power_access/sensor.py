"""Sensor platform for Family Power Access."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import HELLO_WORLD_UNIQUE_ID


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Family Power Access sensors from a config entry."""
    async_add_entities([HelloWorldSensor()])


class HelloWorldSensor(SensorEntity):
    """Static Hello World sensor used to validate the custom integration."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = False
    _attr_name = "Hello World"
    _attr_should_poll = False
    _attr_translation_key = "hello_world"
    _attr_unique_id = HELLO_WORLD_UNIQUE_ID

    @property
    def native_value(self) -> StateType:
        """Return the sensor value."""
        return "Hello World"
