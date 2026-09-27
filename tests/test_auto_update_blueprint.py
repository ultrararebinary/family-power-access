"""Contract tests for the optional auto-update automation blueprint."""

from pathlib import Path
from typing import Any

import yaml
from homeassistant.components.trace.util import async_get_trace, async_list_traces
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.setup import async_setup_component

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "blueprints" / "automation" / "family_power_access_auto_update.yaml"
UPDATE_ENTITY = "update.family_power_access"


class BlueprintLoader(yaml.SafeLoader):
    """YAML loader that preserves Home Assistant blueprint input references."""


def _construct_input(loader: BlueprintLoader, node: yaml.Node) -> dict[str, str]:
    return {"!input": loader.construct_scalar(node)}


BlueprintLoader.add_constructor("!input", _construct_input)


def load_blueprint() -> dict[str, Any]:
    return yaml.load(BLUEPRINT.read_text(), Loader=BlueprintLoader)


def test_blueprint_is_optional_automation_with_update_target_and_time() -> None:
    """The repository ships an importable blueprint, not an enabled automation."""
    blueprint = load_blueprint()

    assert blueprint["blueprint"]["domain"] == "automation"
    assert "automation" not in blueprint

    inputs = blueprint["blueprint"]["input"]
    assert inputs["update_entity"]["selector"] == {"entity": {"domain": "update"}}
    assert inputs["install_time"]["default"] == "21:00:00"
    assert inputs["install_time"]["selector"] == {"time": {}}


def test_blueprint_installs_only_when_selected_update_is_available() -> None:
    """The selected HACS update entity controls both condition and action target."""
    blueprint = load_blueprint()

    assert blueprint["triggers"] == [
        {
            "trigger": "time",
            "at": {"!input": "install_time"},
        }
    ]
    assert blueprint["conditions"] == [
        {
            "condition": "state",
            "entity_id": {"!input": "update_entity"},
            "state": "on",
        }
    ]

    assert blueprint["actions"] == [
        {
            "action": "update.install",
            "target": {"entity_id": {"!input": "update_entity"}},
        }
    ]


def test_blueprint_has_no_explicit_version_restart_or_extra_target() -> None:
    """Failures remain visible in trace without restart or broad targeting."""
    blueprint_text = BLUEPRINT.read_text()
    blueprint = load_blueprint()
    action = blueprint["actions"][0]

    assert "version" not in action
    assert "backup" not in action
    assert "continue_on_error" not in action
    assert action["target"] == {"entity_id": {"!input": "update_entity"}}
    assert "homeassistant.restart" not in blueprint_text
    assert "button.press" not in blueprint_text


async def test_update_install_failure_is_recorded_in_home_assistant_trace(
    hass: HomeAssistant,
) -> None:
    """A failing update.install action is visible through Home Assistant traces."""

    async def fail_update_install(call: ServiceCall) -> None:
        assert call.data == {"entity_id": [UPDATE_ENTITY]}
        raise HomeAssistantError("simulated update.install failure")

    hass.services.async_register("update", "install", fail_update_install)
    hass.states.async_set(UPDATE_ENTITY, "on")

    automation_id = "family_power_access_auto_update_trace"
    assert await async_setup_component(
        hass,
        "automation",
        {
            "automation": [
                {
                    "id": automation_id,
                    "alias": "Family Power Access auto update trace",
                    "triggers": [{"trigger": "time", "at": "21:00:00"}],
                    "conditions": [
                        {
                            "condition": "state",
                            "entity_id": UPDATE_ENTITY,
                            "state": "on",
                        }
                    ],
                    "actions": [
                        {
                            "action": "update.install",
                            "target": {"entity_id": UPDATE_ENTITY},
                        }
                    ],
                }
            ]
        },
    )
    await hass.async_block_till_done()

    await hass.services.async_call(
        "automation",
        "trigger",
        {
            "entity_id": "automation.family_power_access_auto_update_trace",
            "skip_condition": False,
        },
        blocking=True,
    )
    await hass.async_block_till_done()

    traces = await async_list_traces(hass, "automation", f"automation.{automation_id}")
    await hass.services.async_call(
        "automation",
        "turn_off",
        {
            "entity_id": "automation.family_power_access_auto_update_trace",
            "stop_actions": True,
        },
        blocking=True,
    )
    await hass.async_block_till_done()

    assert len(traces) == 1
    assert traces[0]["error"] == "simulated update.install failure"

    trace = await async_get_trace(
        hass, f"automation.{automation_id}", traces[0]["run_id"]
    )
    assert trace["trace"]["action/0"][0]["error"] == (
        "simulated update.install failure"
    )
