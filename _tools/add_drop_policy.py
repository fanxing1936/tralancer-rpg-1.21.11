#!/usr/bin/env python3
"""Generate the 1.21.11 mob-death drop policy.

This deliberately does not touch block/container/fishing loot, player death,
armor stands, mannequins, or existing RPG-authored entity loot tables.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


VANILLA_1_21_11_ENTITIES = """
allay armadillo armor_stand axolotl bat bee blaze bogged breeze camel camel_husk
cat cave_spider chicken cod copper_golem cow creaking creeper dolphin donkey
drowned elder_guardian ender_dragon enderman endermite evoker fox frog ghast giant
glow_squid goat guardian happy_ghast hoglin horse husk illusioner iron_golem llama
magma_cube mannequin mooshroom mule nautilus ocelot panda parched parrot phantom pig
piglin piglin_brute pillager player polar_bear pufferfish rabbit ravager salmon sheep
sheep/black sheep/blue sheep/brown sheep/cyan sheep/gray sheep/green sheep/light_blue
sheep/light_gray sheep/lime sheep/magenta sheep/orange sheep/pink sheep/purple sheep/red
sheep/white sheep/yellow shulker silverfish skeleton skeleton_horse slime sniffer
snow_golem spider squid stray strider tadpole trader_llama tropical_fish turtle vex
villager vindicator wandering_trader warden witch wither wither_skeleton wolf zoglin
zombie zombie_horse zombie_nautilus zombie_villager zombified_piglin
""".split()

# These seven are authored RPG tables in the minecraft namespace.  Preserving
# their files preserves their currency, equipment, and material pools verbatim.
CUSTOM_ENTITY_TABLES = {
    "creeper",
    "husk",
    "skeleton",
    "skeleton_horse",
    "zombie",
    "zombie_horse",
    "zombie_villager",
}

# Player/prop inventory is explicitly outside the user's mob-death policy.
EXCLUDED_ENTITY_TABLES = {"player", "armor_stand", "mannequin"}

CHARGED_CREEPER_TABLES = {
    "root",
    "piglin",
    "creeper",
    "skeleton",
    "wither_skeleton",
    "zombie",
}

EMPTY_ENTITY_TABLE = {"type": "minecraft:entity", "pools": []}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def jar_entity_tables(source_jar: Path) -> set[str]:
    prefix = "data/minecraft/loot_table/entities/"
    with zipfile.ZipFile(source_jar) as jar:
        return {
            name[len(prefix) : -5]
            for name in jar.namelist()
            if name.startswith(prefix) and name.endswith(".json")
        }


def verify_source_jar(source_jar: Path | None) -> None:
    if source_jar is None:
        return
    actual = jar_entity_tables(source_jar)
    expected = set(VANILLA_1_21_11_ENTITIES)
    if actual != expected:
        missing = sorted(actual - expected)
        stale = sorted(expected - actual)
        raise SystemExit(
            "source jar entity-table set differs from the embedded 1.21.11 set; "
            f"new={missing}, missing={stale}"
        )


def require_custom_tables(dp: Path) -> None:
    base = dp / "data/minecraft/loot_table/entities"
    missing = sorted(name for name in CUSTOM_ENTITY_TABLES if not (base / f"{name}.json").is_file())
    if missing:
        raise SystemExit(f"refusing to generate: missing authored entity loot tables: {missing}")


def generate(dp: Path, source_jar: Path | None) -> None:
    verify_source_jar(source_jar)
    require_custom_tables(dp)

    vanilla_root = dp / "data/minecraft/loot_table"
    suppressed = set(VANILLA_1_21_11_ENTITIES) - CUSTOM_ENTITY_TABLES - EXCLUDED_ENTITY_TABLES
    for name in sorted(suppressed):
        write_json(vanilla_root / "entities" / f"{name}.json", EMPTY_ENTITY_TABLE)
    for name in sorted(CHARGED_CREEPER_TABLES):
        write_json(vanilla_root / "charged_creeper" / f"{name}.json", EMPTY_ENTITY_TABLE)

    # Top-level entity tables correspond to entity type ids; sheep colour
    # sub-tables are selected by the main sheep table and are not entity ids.
    guarded_types = sorted(
        name
        for name in VANILLA_1_21_11_ENTITIES
        if "/" not in name and name not in EXCLUDED_ENTITY_TABLES
    )
    write_json(
        dp / "data/rpg/tags/entity_type/drop_policy_mobs.json",
        {"replace": False, "values": [f"minecraft:{name}" for name in guarded_types]},
    )

    write_json(
        dp / "data/rpg/loot_table/squad/equipment_return.json",
        {
            "type": "minecraft:entity",
            "pools": [
                {
                    "rolls": 1,
                    "entries": [
                        {
                            "type": "minecraft:slots",
                            "slot_source": {
                                "type": "minecraft:slot_range",
                                "source": "this",
                                "slots": "weapon.mainhand",
                            },
                        }
                    ],
                }
            ],
        },
    )

    fn = dp / "data/rpg/function/drop_policy"
    # Run before combat code so existing/newly loaded mobs receive the guard
    # before this pack's tick can apply damage. No scoreboard reset on reload.
    tick_path = dp / "data/rpg/function/command/tick.mcfunction"
    tick_lines = tick_path.read_text(encoding="utf-8").splitlines()
    hook = "function rpg:drop_policy/tick"
    write_text(tick_path, "\n".join([hook] + [line for line in tick_lines if line != hook]))
    write_text(
        fn / "tick.mcfunction",
        "# Only newly seen mobs are mutated; normal item entities are never scanned or removed.\n"
        "execute as @e[type=#rpg:drop_policy_mobs,tag=!rpg.drop_policy.v1] run function rpg:drop_policy/prepare",
    )
    write_text(
        fn / "prepare.mcfunction",
        "# RPG mercenaries return the player's entrusted main-hand item through an authored loot table.\n"
        'execute if entity @s[tag=rpg.merc] run data modify entity @s DeathLootTable set value "rpg:squad/equipment_return"\n'
        "# 0f is checked before Looting adjustment in Minecraft 1.21.11 Mob.dropCustomDeathLoot.\n"
        "data merge entity @s {CanPickUpLoot:0b,drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f,body:0f,saddle:0f}}\n"
        "tag @s add rpg.drop_policy.v1",
    )

    manifest = {
        "schema": 1,
        "minecraft_version": "1.21.11",
        "suppressed_entity_tables": sorted(suppressed),
        "preserved_custom_entity_tables": sorted(CUSTOM_ENTITY_TABLES),
        "excluded_non_mob_inventory_tables": sorted(EXCLUDED_ENTITY_TABLES),
        "suppressed_charged_creeper_tables": sorted(CHARGED_CREEPER_TABLES),
        "hardcoded_boundaries": [
            "WitherBoss directly spawns the nether star after normal loot processing.",
            "Horse-family inventory and chested-horse chest items are dropped by dropEquipment outside loot tables.",
            "Allay and piglin inventory, allay entrusted hand items, and copper-golem preserved items have dedicated return paths.",
            "Enderman carried blocks are generated from block loot, which this policy intentionally does not override.",
            "Equipment guarding runs on the first global tick that sees a mob; same-tick summon-and-kill command chains are outside this guarantee.",
        ],
    }
    write_json(dp / "data/rpg/drop_policy_manifest.json", manifest)

    print(
        f"drop policy generated: {len(suppressed)} vanilla entity tables suppressed, "
        f"{len(CUSTOM_ENTITY_TABLES)} authored tables preserved, "
        f"{len(guarded_types)} entity types equipment-guarded"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("datapack", nargs="?", default="rpg")
    parser.add_argument("--source-jar", type=Path)
    args = parser.parse_args()
    generate(Path(args.datapack), args.source_jar)


if __name__ == "__main__":
    main()
