#!/usr/bin/env python3
"""Resolve composed Spec Kit template content from the project template stack."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


SAFE_NAME = re.compile(r"[a-z0-9-]+\Z")
STRATEGIES = {"replace", "prepend", "append", "wrap"}
TEMPLATE_TYPES = {"template", "command", "script"}


class ResolutionError(Exception):
    """Raised when template layers cannot be resolved safely."""


def project_root(script_path: Path) -> Path:
    explicit = os.environ.get("SPECIFY_INIT_DIR")
    if explicit:
        root = Path(explicit)
        if not root.is_absolute():
            root = Path.cwd() / root
        try:
            root = root.resolve(strict=True)
        except OSError as exc:
            raise ResolutionError(
                f"SPECIFY_INIT_DIR does not point to an existing directory: {explicit}"
            ) from exc
        if not root.is_dir() or not (root / ".specify").is_dir():
            raise ResolutionError(
                f"SPECIFY_INIT_DIR is not a Spec Kit project (no .specify/ directory): {root}"
            )
        return root

    for start in (Path.cwd(), script_path.resolve().parent):
        for candidate in (start, *start.parents):
            if (candidate / ".specify").is_dir():
                return candidate
    raise ResolutionError("Could not find a Spec Kit project (.specify/ directory)")


def safe_priority(value: object) -> int:
    if isinstance(value, bool):
        return 10
    try:
        priority = int(value)
    except (TypeError, ValueError, OverflowError):
        return 10
    return priority if priority >= 1 else 10


def sorted_preset_ids(presets_dir: Path) -> list[str]:
    registry = presets_dir / ".registry"
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
            presets = data.get("presets", {})
            return [
                preset_id
                for preset_id, metadata in sorted(
                    presets.items(),
                    key=lambda item: (safe_priority(
                        item[1].get("priority") if isinstance(item[1], dict) else None
                    ), item[0]),
                )
                if isinstance(preset_id, str)
                and SAFE_NAME.fullmatch(preset_id)
                and isinstance(metadata, dict)
                and bool(metadata.get("enabled", True))
            ]
        except Exception:
            # Match the Spec Kit shell resolver: malformed preset registries
            # fall back to the installed preset directories.
            pass
    try:
        return sorted(
            path.name for path in presets_dir.iterdir()
            if path.is_dir() and SAFE_NAME.fullmatch(path.name)
        )
    except OSError:
        return []


def sorted_extension_ids(extensions_dir: Path) -> list[str]:
    registry = extensions_dir / ".registry"
    registered: dict[object, object] = {}
    if os.path.lexists(registry):
        if not registry.is_file():
            raise ResolutionError(f"Invalid extension registry {registry}: not a regular file")
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ResolutionError(f"Failed to parse extension registry {registry}: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("extensions", {}), dict):
            raise ResolutionError(f"Invalid extension registry {registry}: extensions must be a mapping")
        registered = data.get("extensions", {})

    ranked: list[tuple[int, str]] = []
    registered_ids = {key for key in registered if isinstance(key, str)}
    for extension_id, metadata in registered.items():
        if (
            isinstance(extension_id, str)
            and SAFE_NAME.fullmatch(extension_id)
            and isinstance(metadata, dict)
            and bool(metadata.get("enabled", True))
        ):
            ranked.append((safe_priority(metadata.get("priority")), extension_id))
    try:
        ranked.extend(
            (10, path.name)
            for path in extensions_dir.iterdir()
            if path.is_dir()
            and SAFE_NAME.fullmatch(path.name)
            and path.name not in registered_ids
        )
    except OSError:
        pass
    return [extension_id for _, extension_id in sorted(ranked)]


def conventional_template(directory: Path, name: str) -> Path | None:
    for candidate in (directory / "templates" / f"{name}.md", directory / f"{name}.md"):
        if candidate.is_file():
            return candidate
    return None


def preset_layer(preset_dir: Path, name: str) -> tuple[Path, str] | None:
    manifest_path = preset_dir / "preset.yml"
    conventional = conventional_template(preset_dir, name)
    manifest_declares_name = False
    strategy = "replace"
    candidate: Path | None = None

    if manifest_path.is_file():
        try:
            import yaml
        except ImportError as exc:
            raise ResolutionError(
                "PyYAML is required to resolve preset template composition"
            ) from exc
        try:
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(manifest, dict) or not isinstance(manifest.get("provides"), dict):
                raise ValueError("manifest must contain a provides mapping")
            templates = manifest["provides"].get("templates")
            if not isinstance(templates, list) or not templates:
                raise ValueError("manifest provides.templates must be a non-empty list")
            for entry in templates:
                if not isinstance(entry, dict) or not all(
                    isinstance(entry.get(key), str) for key in ("type", "name", "file")
                ):
                    raise ValueError("manifest template entries need string type, name, and file")
                if entry["type"] not in TEMPLATE_TYPES:
                    raise ValueError("invalid manifest template type")
                entry_strategy = entry.get("strategy", "replace")
                if not isinstance(entry_strategy, str) or entry_strategy.lower() not in STRATEGIES:
                    raise ValueError("invalid manifest template strategy")
                if entry["type"] == "script" and entry_strategy.lower() not in {"replace", "wrap"}:
                    raise ValueError("invalid manifest script strategy")
            for entry in templates:
                if entry.get("name") == name and entry.get("type", "template") == "template":
                    manifest_declares_name = True
                    strategy = entry.get("strategy", "replace").lower()
                    relative = Path(entry["file"])
                    if not relative.is_absolute() and ".." not in relative.parts:
                        declared = preset_dir / relative
                        if declared.is_file():
                            candidate = declared
                    break
        except Exception as exc:
            raise ResolutionError(f"Invalid preset manifest {manifest_path}: {exc}") from exc

    if candidate is None and not manifest_declares_name:
        candidate = conventional
    return (candidate, strategy) if candidate is not None else None


def collect_layers(name: str, root: Path) -> list[tuple[Path, str]]:
    base = root / ".specify" / "templates"
    override = base / "overrides" / f"{name}.md"
    if override.is_file():
        return [(override, "replace")]

    layers: list[tuple[Path, str]] = []
    effective_base_found = False
    presets_dir = root / ".specify" / "presets"
    if presets_dir.is_dir():
        for preset_id in sorted_preset_ids(presets_dir):
            layer = preset_layer(presets_dir / preset_id, name)
            if layer:
                layers.append(layer)
                if layer[1] == "replace":
                    effective_base_found = True
                    break

    extensions_dir = root / ".specify" / "extensions"
    if not effective_base_found and extensions_dir.is_dir():
        for extension_id in sorted_extension_ids(extensions_dir):
            candidate = conventional_template(extensions_dir / extension_id, name)
            if candidate:
                layers.append((candidate, "replace"))
                effective_base_found = True
                break

    core = base / f"{name}.md"
    if not effective_base_found and core.is_file():
        layers.append((core, "replace"))
    return layers


def resolve_template_content(name: str, root: Path) -> str | None:
    if not SAFE_NAME.fullmatch(name):
        return None
    layers = collect_layers(name, root)
    if not layers:
        return None
    try:
        content = layers[-1][0].read_text(encoding="utf-8")
        for path, strategy in reversed(layers[:-1]):
            layer_content = path.read_text(encoding="utf-8")
            if strategy == "replace":
                content = layer_content
            elif strategy == "prepend":
                content = f"{layer_content}\n\n{content}"
            elif strategy == "append":
                content = f"{content}\n\n{layer_content}"
            elif strategy == "wrap":
                if "{CORE_TEMPLATE}" not in layer_content:
                    raise ResolutionError(
                        f"Wrap template {path} is missing {{CORE_TEMPLATE}} placeholder"
                    )
                content = layer_content.replace("{CORE_TEMPLATE}", content)
        return content
    except OSError as exc:
        raise ResolutionError(f"Failed to read template layer: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("template_name")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        root = project_root(Path(__file__))
        content = resolve_template_content(args.template_name, root)
    except ResolutionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if content is None:
        print(
            f"ERROR: Could not resolve required {args.template_name} from the "
            f"template override stack for {root}",
            file=sys.stderr,
        )
        return 1

    if args.json:
        print(json.dumps(
            {"TEMPLATE_NAME": args.template_name, "TEMPLATE_CONTENT": content},
            ensure_ascii=False,
            separators=(",", ":"),
        ))
    else:
        sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
