"""Family Power Access custom integration."""

from pathlib import Path

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import (
    StaticPathConfig,  # pyright: ignore[reportPrivateImportUsage]
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    NAME,
    PANEL_ELEMENT_NAME,
    PANEL_ICON,
    PANEL_MODULE_URL,
    PANEL_STATIC_PATH,
    PANEL_URL_PATH,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]
FRONTEND_PATH = Path(__file__).parent / "frontend"


async def async_setup(hass: HomeAssistant, config: dict[str, object]) -> bool:
    """Serve the packaged panel module once for this Home Assistant runtime."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get("static_path_registered"):
        return True

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=PANEL_STATIC_PATH,
                path=str(FRONTEND_PATH),
                cache_headers=False,
            )
        ]
    )
    domain_data["static_path_registered"] = True
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Family Power Access from a config entry."""
    if frontend.async_panel_exists(hass, PANEL_URL_PATH):
        raise HomeAssistantError(
            f"The Home Assistant panel path {PANEL_URL_PATH} is already registered"
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    try:
        await panel_custom.async_register_panel(
            hass=hass,
            frontend_url_path=PANEL_URL_PATH,
            webcomponent_name=PANEL_ELEMENT_NAME,
            sidebar_title=NAME,
            sidebar_icon=PANEL_ICON,
            module_url=PANEL_MODULE_URL,
            require_admin=False,
        )
    except ValueError as err:
        await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
        raise HomeAssistantError(
            f"The Home Assistant panel path {PANEL_URL_PATH} is already registered"
        ) from err

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Family Power Access config entry."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False

    frontend.async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)
    return True
