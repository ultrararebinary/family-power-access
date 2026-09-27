"""Distribution contract for the Home Assistant custom integration."""

import json
import struct
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "family_power_access"


def test_one_custom_integration_and_matching_versions() -> None:
    """HACS receives one integration with the same version as the project."""
    packages = [
        path
        for path in (ROOT / "custom_components").iterdir()
        if path.is_dir() and (path / "manifest.json").is_file()
    ]
    assert [path.name for path in packages] == ["family_power_access"]

    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert manifest["domain"] == "family_power_access"
    assert manifest["name"] == "Family Power Access"
    assert manifest["version"] == project["project"]["version"] == "0.1.1"
    assert manifest["config_flow"] is True
    assert manifest["single_config_entry"] is True
    assert manifest["requirements"] == []


def test_release_metadata_is_complete() -> None:
    """The repository exposes all metadata required for HACS distribution."""
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    hacs = json.loads((ROOT / "hacs.json").read_text())

    assert manifest["documentation"].startswith("https://github.com/")
    assert manifest["issue_tracker"] == manifest["documentation"] + "/issues"
    assert manifest["codeowners"]
    assert hacs == {"name": "Family Power Access", "hide_default_branch": True}
    assert (ROOT / "README.md").is_file()


def test_translations_and_brand_icon_are_packaged() -> None:
    """HACS and Home Assistant can show labels and the repository icon."""
    for path in (
        INTEGRATION / "strings.json",
        INTEGRATION / "translations" / "en.json",
        INTEGRATION / "translations" / "fr.json",
    ):
        assert json.loads(path.read_text())

    icon = (ROOT / "brand" / "icon.png").read_bytes()
    assert icon[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", icon[16:24]) == (256, 256)
