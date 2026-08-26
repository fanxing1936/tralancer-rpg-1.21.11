#!/usr/bin/env python3
"""Acceptance gate for the configurable Chapter I build contract.

Before the main generator is wired, this checker verifies that the new config
exactly describes its current defaults.  Once wired, ``--require-wired`` also
requires a digest-bearing manifest and all debug entry functions in the build.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from beelzebub_campaign_config import (
    ConfigError,
    DEFAULT_CONFIG,
    config_digest,
    iter_items,
    iter_positions,
    load_config,
    manifest,
)


def generated_path(pack_root: Path, function_id: str) -> Path:
    namespace, rel = function_id.split(":", 1)
    return pack_root / "data" / namespace / "function" / f"{rel}.mcfunction"


def current_default_tokens(config: dict) -> list[tuple[str, str]]:
    """Map non-templated defaults to literals in the pre-integration generator.

    Values emitted through Python loops/f-strings are deliberately omitted here;
    their generated function references are already checked by ``load_config``.
    """
    tokens: list[tuple[str, str]] = []
    for name, value in config["visual"]["palette"].items():
        tokens.append((f"visual.palette.{name}", value))
    dynamic_positions = {"scene.trail.trail2", "scene.trail.trail3", "scene.trail.trail4"}
    for kind, key, position in iter_positions(config):
        if f"{kind}.{key}" not in dynamic_positions:
            tokens.append((f"position.{kind}.{key}", position))
    for category, key, item in iter_items(config):
        tokens.append((f"item.{category}.{key}.give_function", item["give_function"]))
        if category != "rewards":
            tokens.append((f"item.{category}.{key}.match", item["match"]))
    boss = config["actors"]["boss"]
    tokens.extend([
        ("actors.boss.summon_function", boss["summon_function"]),
        ("actors.boss.lord_score", f"rpg_dm_lord={boss['lord_score']}"),
    ])
    for key, minion in config["actors"]["minions"].items():
        tokens.append((f"actors.minions.{key}.id", f'"{key}"'))
    runtime = config["runtime"]
    tokens.extend([
        ("runtime.active_radius", f"distance=..{runtime['active_radius']}"),
        ("runtime.scene_radius", f"distance=..{runtime['scene_radius']}"),
        ("runtime.rite_bind_radius", f"distance=..{runtime['rite_bind_radius']}"),
        ("runtime.observation_ticks.anomaly", f"threshold = 80 if key.startswith(\"hyp\") else {runtime['observation_ticks']['anomaly']}"),
        ("runtime.observation_ticks.trail", f"else {runtime['observation_ticks']['trail']}"),
        ("runtime.recovery.mira_capture_ticks", f"rpg_ch1_guard matches {runtime['recovery']['mira_capture_ticks']}.."),
        ("runtime.recovery.mira_rescue_ticks", f"rpg_ch1_rescue matches {runtime['recovery']['mira_rescue_ticks']}.."),
    ])
    return tokens


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Chapter I configuration coverage and wiring")
    parser.add_argument("pack_root", nargs="?", type=Path, default=Path("../rpg"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--require-wired", action="store_true", help="fail unless generator consumption, manifest and debug functions exist")
    args = parser.parse_args()
    pack_root = args.pack_root.resolve()
    repo_root = Path(__file__).resolve().parent.parent
    generator_path = repo_root / "_tools" / "add_beelzebub_campaign.py"
    errors: list[str] = []

    try:
        config = load_config(args.config, pack_root)
    except ConfigError as exc:
        print(exc)
        return 1

    generator = generator_path.read_text(encoding="utf-8")
    wired = "beelzebub_campaign_config import" in generator and "load_config(" in generator

    if not wired:
        for path, token in current_default_tokens(config):
            if token not in generator:
                errors.append(f"unwired default drift: {path} -> {token!r}")

    integration = config["integration"]
    manifest_path = pack_root / integration["generated_manifest"]
    if wired:
        if not manifest_path.is_file():
            errors.append(f"wired generator did not emit manifest: {manifest_path}")
        else:
            try:
                actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid generated manifest: {exc}")
            else:
                expected_manifest = manifest(config)
                if actual_manifest != expected_manifest:
                    errors.append(
                        "generated manifest does not match config "
                        f"(expected sha256 {config_digest(config)}, got {actual_manifest.get('sha256')})"
                    )
        if config["debug"]["enabled"]:
            for key, function_id in config["debug"]["entry_points"].items():
                if not generated_path(pack_root, function_id).is_file():
                    errors.append(f"missing debug function: {key} -> {function_id}")
            for stage in config["debug"]["stage_jump_targets"]:
                jump = generated_path(pack_root, f"{config['debug']['function_namespace']}/stage/{stage}")
                if not jump.is_file():
                    errors.append(f"missing debug stage jump: {stage}")
                worker = generated_path(pack_root, f"{config['debug']['function_namespace']}/stage/{stage}_worker")
                if not worker.is_file():
                    errors.append(f"missing debug stage worker: {stage}")
                elif "tag @s add rpg.ch1.debug.no_commit" not in worker.read_text(encoding="utf-8"):
                    errors.append(f"debug stage {stage} is not protected from permanent progression")
            stage10_tick = generated_path(pack_root, "rpg:campaign/beelzebub/stage/10_tick")
            if stage10_tick.is_file():
                stage10_body = stage10_tick.read_text(encoding="utf-8")
                if "unless entity @s[tag=rpg.ch1.debug.no_commit]" not in stage10_body:
                    errors.append("Stage 10 does not gate permanent completion during debug preview")
        for category, key, item in iter_items(config):
            give_path = generated_path(pack_root, item["give_function"])
            if not give_path.is_file():
                errors.append(f"configured item give function is missing: {category}.{key} -> {item['give_function']}")

        join_path = generated_path(pack_root, "rpg:campaign/beelzebub/join")
        if join_path.is_file():
            join_body = join_path.read_text(encoding="utf-8")
            full_gate = f"scores={{rpg_ch1_roster={config['runtime']['max_party_size']}..}}"
            if full_gate not in join_body or join_body.find(full_gate) > join_body.find("tag @s add rpg.ch1.accepted"):
                errors.append("max_party_size is not enforced before accepting a new member")

        preflight_path = generated_path(pack_root, "rpg:campaign/beelzebub/scene/preflight")
        if preflight_path.is_file():
            preflight = preflight_path.read_text(encoding="utf-8")
            highest_air = f"if block ~ ~{config['runtime']['safe_plane']['headroom'] - 1} ~ minecraft:air"
            if highest_air not in preflight:
                errors.append("safe_plane.headroom does not drive generated air checks")

        for stage, recap_tag in ((1, "anomaly"), (3, "minions"), (4, "area"), (5, "hypothesis"), (6, "prep")):
            tick_path = generated_path(pack_root, f"rpg:campaign/beelzebub/stage/{stage}_tick")
            if tick_path.is_file():
                tick_body = tick_path.read_text(encoding="utf-8")
                hold = f"tag=rpg.ch1.recap.{recap_tag}] if score @s rpg_ch1_time matches {config['runtime']['recap_hold_ticks']}.."
                if hold not in tick_body:
                    errors.append(f"Stage {stage} recap does not hold for recap_hold_ticks")

        raw_palette = [value for value in config["visual"]["palette"].values() if value in generator]
        if raw_palette:
            errors.append("generator contains raw configurable palette colors: " + ", ".join(sorted(raw_palette)))
    elif args.require_wired:
        errors.append("add_beelzebub_campaign.py does not load the Chapter I config yet")

    if errors:
        print(f"Chapter I config check FAILED ({len(errors)})")
        for error in errors:
            print("- " + error)
        return 1

    state = "wired" if wired else "contract-ready / awaiting generator integration"
    print(
        f"Chapter I config check OK: {state}; 15 items, 11 actors, "
        f"{len(list(iter_positions(config)))} configurable positions; sha256={config_digest(config)[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
