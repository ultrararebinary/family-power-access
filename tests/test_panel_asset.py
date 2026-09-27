"""HTTP contract for the packaged Family Power Access panel module."""

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.family_power_access.const import (
    DOMAIN,
    HELLO_WORLD_UNIQUE_ID,
    NAME,
    PANEL_MODULE_URL,
)


async def test_panel_module_is_served_locally_without_external_scripts(
    hass: HomeAssistant,
    frontend_panel_components: HomeAssistant,
    hass_client,
) -> None:
    """HACS-packaged frontend code is served from the local integration folder."""
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

    client = await hass_client()
    response = await client.get(PANEL_MODULE_URL)

    assert response.status == 200
    module = await response.text()
    assert "Hello World" in module
    assert "customElements.define" in module
    assert "https://" not in module
