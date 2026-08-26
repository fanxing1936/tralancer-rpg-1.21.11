#!/usr/bin/env python3
"""Typed loader and validation helpers for Chapter I configuration.

The campaign generator should import this module instead of reading JSON ad hoc.
Keeping validation here makes a bad debug coordinate or resource location fail at
build time, before it can create a partially generated datapack.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Iterator


DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "_campaign_beelzebub_config.json"
RESOURCE_LOCATION = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
LOCAL_COORD = re.compile(r"^\^(?:-?(?:\d+(?:\.\d+)?|\.\d+))?$")


class ConfigError(ValueError):
    """Raised when Chapter I configuration is unsafe or incomplete."""


def _expect(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _is_resource(value: Any) -> bool:
    return isinstance(value, str) and RESOURCE_LOCATION.fullmatch(value) is not None


def _is_local_position(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parts = value.split()
    return len(parts) == 3 and all(LOCAL_COORD.fullmatch(part) for part in parts)


def iter_items(config: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any]]]:
    """Yield ``(category, key, item)`` for every Chapter I item reference."""
    for category, entries in config["items"].items():
        for key, item in entries.items():
            yield category, key, item


def item_index(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {key: item for _, key, item in iter_items(config)}


def iter_actors(config: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any]]]:
    actors = config["actors"]
    yield "controller", "controller", actors["controller"]
    for key, actor in actors["npcs"].items():
        yield "npc", key, actor
    yield "boss", actors["boss"]["id"], actors["boss"]
    for key, actor in actors["minions"].items():
        yield "minion", key, actor


def iter_positions(config: dict[str, Any]) -> Iterator[tuple[str, str, str]]:
    """Yield every configurable local position, including scene labels."""
    for kind, key, actor in iter_actors(config):
        yield kind, key, actor["spawn"]
    for group, points in config["scene_points"].items():
        for key, point in points.items():
            yield f"scene.{group}", key, point["spawn"]


def palette_color(config: dict[str, Any], name_or_hex: str) -> str:
    """Resolve a palette alias while still permitting an explicit hex color."""
    if HEX_COLOR.fullmatch(name_or_hex):
        return name_or_hex.upper()
    try:
        return config["visual"]["palette"][name_or_hex]
    except KeyError as exc:
        raise ConfigError(f"unknown palette color: {name_or_hex}") from exc


def config_digest(config: dict[str, Any]) -> str:
    canonical = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def manifest(config: dict[str, Any]) -> dict[str, Any]:
    """Return a compact, data-pack-safe build manifest for regression checks."""
    return {
        "schema_version": config["schema_version"],
        "config_id": config["config_id"],
        "sha256": config_digest(config),
        "item_keys": sorted(item_index(config)),
        "actor_keys": sorted(key for _, key, _ in iter_actors(config)),
        "position_keys": sorted(f"{kind}.{key}" for kind, key, _ in iter_positions(config)),
        "debug_enabled": bool(config["debug"]["enabled"]),
    }


def validate(config: dict[str, Any], pack_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    _expect(config.get("schema_version") == 1, "schema_version must be 1", errors)
    _expect(config.get("config_id") == "beelzebub_chapter_1", "unexpected config_id", errors)

    required = ("runtime", "visual", "items", "actors", "scene_points", "cache_loadouts", "debug", "integration")
    for key in required:
        _expect(isinstance(config.get(key), dict), f"missing object: {key}", errors)
    if errors:
        return errors

    runtime = config["runtime"]
    _expect(_is_resource(runtime.get("dimension")), "runtime.dimension is not a resource location", errors)
    _expect(runtime.get("max_party_size") in range(1, 9), "runtime.max_party_size must be 1..8", errors)
    _expect(runtime.get("join_lock_stage") in range(0, 11), "runtime.join_lock_stage must be 0..10", errors)
    for key in ("active_radius", "scene_radius", "boss_claim_radius", "rite_bind_radius", "witness_radius", "investigate_radius"):
        _expect(isinstance(runtime.get(key), (int, float)) and runtime[key] > 0, f"runtime.{key} must be positive", errors)
    timing = runtime.get("observation_ticks", {})
    for key in ("anomaly", "trail", "hypothesis", "cache", "puzzle"):
        _expect(isinstance(timing.get(key), int) and timing[key] > 0,
                f"runtime.observation_ticks.{key} must be a positive integer", errors)
    _expect(isinstance(runtime.get("recap_hold_ticks"), int) and runtime["recap_hold_ticks"] >= 40,
            "runtime.recap_hold_ticks must be an integer of at least 40", errors)
    recovery = runtime.get("recovery", {})
    for key in ("party_wipe_ticks", "mira_capture_ticks", "mira_rescue_ticks",
                "mira_rescue_window_ticks", "boss_missing_ticks"):
        _expect(isinstance(recovery.get(key), int) and recovery[key] > 0,
                f"runtime.recovery.{key} must be a positive integer", errors)

    safe = runtime.get("safe_plane", {})
    _expect(isinstance(safe.get("headroom"), int), "runtime.safe_plane.headroom must be an integer", errors)
    _expect(safe.get("headroom", 0) >= 3, "safe plane needs at least three blocks of headroom", errors)
    for axis in ("ground_sample_x", "ground_sample_z", "tall_sample_x", "tall_sample_z"):
        _expect(isinstance(safe.get(axis), list) and safe[axis] and all(isinstance(v, int) for v in safe[axis]), f"invalid safe sample axis: {axis}", errors)
    forbidden = safe.get("forbidden_ground", [])
    _expect(isinstance(forbidden, list) and len(forbidden) == len(set(forbidden)), "forbidden_ground must be a unique list", errors)
    for block in forbidden:
        _expect(_is_resource(block), f"invalid forbidden block: {block}", errors)

    palette = config["visual"].get("palette", {})
    required_colors = {"chapter", "church", "beelzebub", "beelzebub_light", "ash", "danger", "witness", "seal", "pact",
                       "eliminate", "danger_ui", "panel", "next_hunt", "beelzebub_combat", "beelzebub_soft",
                       "beelzebub_glint", "white"}
    _expect(required_colors <= set(palette), "visual.palette is missing canonical colors", errors)
    for key, value in palette.items():
        _expect(isinstance(value, str) and HEX_COLOR.fullmatch(value) is not None, f"invalid palette color {key}: {value}", errors)

    items = list(iter_items(config))
    _expect(len(items) == 15, f"expected 15 Chapter I item references, got {len(items)}", errors)
    keys = [key for _, key, _ in items]
    _expect(len(keys) == len(set(keys)), "item keys must be globally unique", errors)
    for category, key, item in items:
        _expect(_is_resource(item.get("base_item")), f"invalid base item: {category}.{key}", errors)
        _expect(_is_resource(item.get("give_function")), f"invalid give function: {category}.{key}", errors)
        _expect(isinstance(item.get("match"), str) and item["match"], f"missing item match: {category}.{key}", errors)
        _expect(isinstance(item.get("generated", False), bool), f"invalid generated flag: {category}.{key}", errors)
        if item.get("generated", False):
            _expect(item["match"].startswith("minecraft:custom_data~{"),
                    f"generated item match must expose custom_data: {category}.{key}", errors)
        if "item_model" in item:
            _expect(_is_resource(item["item_model"]), f"invalid item model: {category}.{key}", errors)
    totem = config["items"]["investigation"].get("exorcism_totem", {})
    _expect(isinstance(totem.get("source"), str) and totem["source"].endswith(".mcfunction"),
            "exorcism_totem.source must identify a canonical function", errors)

    actors = config["actors"]
    boss = actors.get("boss", {})
    _expect(boss.get("id") == "beelzebub", "boss.id must remain beelzebub", errors)
    _expect(boss.get("lord_score") == 4, "Beelzebub must use rpg_dm_lord=4", errors)
    _expect(isinstance(boss.get("health"), int) and boss["health"] > 0,
            "Chapter I boss health must be a positive integer", errors)
    _expect(_is_resource(boss.get("summon_function")), "boss summon_function is invalid", errors)
    minions = actors.get("minions", {})
    _expect(set(minions) == {"zepar", "botis", "bathin", "sallos", "purson"}, "the five Beelzebub minions are incomplete", errors)
    _expect(sorted(m.get("role") for m in minions.values()) == [1, 2, 3, 4, 5], "minion roles must be exactly 1..5", errors)
    wave_values = [m.get("wave") for m in minions.values()]
    _expect(all(isinstance(wave, int) and wave > 0 for wave in wave_values), "minion waves must be positive integers", errors)
    if all(isinstance(wave, int) and wave > 0 for wave in wave_values):
        _expect(sorted(set(wave_values)) == list(range(1, max(wave_values) + 1)),
                "minion waves must be contiguous from 1", errors)
    for key, minion in minions.items():
        _expect(_is_resource(minion.get("entity_type")), f"invalid minion entity type: {key}", errors)
        _expect(_is_resource(minion.get("summon_function")), f"invalid minion summon function: {key}", errors)
        _expect(isinstance(minion.get("duty"), str) and minion["duty"], f"{key} duty must be non-empty", errors)
        health = minion.get("health_by_party", {})
        required_rosters = {str(size) for size in range(2, runtime["max_party_size"] + 1)}
        _expect(required_rosters <= set(health),
                f"{key} health_by_party must cover every configured party size 2..{runtime['max_party_size']}", errors)
        _expect(all(str(size) in {str(n) for n in range(2, 9)} for size in health),
                f"{key} health_by_party keys must be 2..8", errors)
        _expect(all(isinstance(v, int) and v > 0 for v in health.values()), f"{key} health values must be positive integers", errors)

    actor_ids: list[str] = []
    for kind, key, actor in iter_actors(config):
        actor_ids.append(f"{kind}.{key}")
        position_only = actor.get("position_only", False)
        _expect(isinstance(position_only, bool), f"invalid position_only flag: {kind}.{key}", errors)
        if not position_only:
            _expect(_is_resource(actor.get("entity_type")), f"invalid entity type: {kind}.{key}", errors)
        _expect(_is_local_position(actor.get("spawn")), f"invalid local spawn: {kind}.{key}={actor.get('spawn')}", errors)
    _expect(actors.get("controller", {}).get("entity_type") == "minecraft:marker",
            "controller.entity_type is an internal marker invariant", errors)
    _expect(len(actor_ids) == len(set(actor_ids)), "actor identifiers are not unique", errors)

    expected_points = {
        "anomaly": 3,
        "trail": 4,
        "hypothesis": 3,
        "cache": 3,
        "route_cipher": 3,
        "hypothesis_board": 3,
        "ritual_calibration": 3,
    }
    point_keys: list[str] = []
    for group, expected_count in expected_points.items():
        points = config["scene_points"].get(group, {})
        _expect(len(points) == expected_count, f"scene_points.{group} expected {expected_count} entries", errors)
        for key, point in points.items():
            point_keys.append(key)
            _expect(_is_local_position(point.get("spawn")), f"invalid scene spawn: {group}.{key}", errors)
            _expect(isinstance(point.get("label"), str) and point["label"], f"empty scene label: {group}.{key}", errors)
            try:
                palette_color(config, point.get("color", ""))
            except ConfigError as exc:
                errors.append(f"{group}.{key}: {exc}")
    _expect(len(point_keys) == len(set(point_keys)), "scene point keys must be globally unique", errors)

    known_items = set(keys)
    loadouts = config["cache_loadouts"]
    _expect(set(loadouts) == {"cache1", "cache2", "cache3"}, "cache_loadouts must define cache1..cache3", errors)
    distributed: list[str] = []
    for cache, loadout in loadouts.items():
        _expect(isinstance(loadout, list) and loadout, f"empty cache loadout: {cache}", errors)
        for key in loadout:
            distributed.append(key)
            _expect(key in known_items, f"unknown item in {cache}: {key}", errors)
    expected_kit = {"pending_name_page", "beelzebub_medium", "exorcism_totem", "strong_holy_water", "silver_nail", "confession_bell", "purification_censer", "ritual_chalk_defense", "demon_sealing_lamp"}
    _expect(set(distributed) == expected_kit, "cache loadouts do not exactly cover the Chapter I investigation kit", errors)
    _expect(len(distributed) == len(set(distributed)), "an item is distributed by more than one cache", errors)

    debug = config["debug"]
    _expect(isinstance(debug.get("enabled"), bool), "debug.enabled must be boolean", errors)
    _expect(debug.get("operator_only") is True, "debug commands must stay operator-only", errors)
    _expect(_is_resource(debug.get("function_namespace")), "debug.function_namespace is invalid", errors)
    entries = debug.get("entry_points", {})
    for key in ("menu", "start", "give_all_items", "spawn_boss", "spawn_all_minions", "list_positions"):
        _expect(_is_resource(entries.get(key)), f"missing debug entry point: {key}", errors)
    _expect(debug.get("stage_jump_targets") == list(range(11)), "debug stage jump targets must be 0..10", errors)

    integration = config["integration"]
    _expect(integration.get("loader_module") == "_tools/beelzebub_campaign_config.py", "loader_module path drifted", errors)
    _expect(_is_resource("rpg:" + integration.get("generated_manifest", "").replace("data/rpg/", "", 1).removesuffix(".json")), "generated_manifest path is invalid", errors)
    _expect(set(integration.get("required_consumers", [])) == {"runtime", "visual.palette", "items", "actors", "scene_points", "cache_loadouts", "debug"}, "integration.required_consumers is incomplete", errors)

    if pack_root is not None:
        function_root = pack_root / "data" / "rpg" / "function"
        for category, key, item in items:
            namespace, rel = item["give_function"].split(":", 1)
            if namespace == "rpg" and not item.get("generated", False):
                _expect((function_root / f"{rel}.mcfunction").is_file(), f"missing generated give function: {category}.{key} -> {item['give_function']}", errors)
        for key, actor in [("boss", boss), *minions.items()]:
            namespace, rel = actor["summon_function"].split(":", 1)
            if namespace == "rpg":
                _expect((function_root / f"{rel}.mcfunction").is_file(), f"missing generated summon function: {key} -> {actor['summon_function']}", errors)

    return errors


def load_config(path: Path | str = DEFAULT_CONFIG, pack_root: Path | None = None) -> dict[str, Any]:
    path = Path(path).resolve()
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot load Chapter I config {path}: {exc}") from exc
    errors = validate(config, pack_root)
    if errors:
        raise ConfigError("invalid Chapter I config:\n- " + "\n- ".join(errors))
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description="Load and inspect Chapter I configuration")
    parser.add_argument("config", nargs="?", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--pack-root", type=Path, help="also verify generated rpg:function references")
    parser.add_argument("--manifest", action="store_true", help="print the compact generated manifest")
    parser.add_argument("--positions", action="store_true", help="print every configurable spawn position")
    args = parser.parse_args()
    config = load_config(args.config, args.pack_root.resolve() if args.pack_root else None)
    if args.manifest:
        print(json.dumps(manifest(config), ensure_ascii=False, indent=2))
    elif args.positions:
        for kind, key, position in iter_positions(config):
            print(f"{kind}.{key} = {position}")
    else:
        print(
            f"Chapter I config OK: {len(list(iter_items(config)))} items, "
            f"{len(list(iter_actors(config)))} actors, {len(list(iter_positions(config)))} positions, "
            f"sha256={config_digest(config)[:12]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
