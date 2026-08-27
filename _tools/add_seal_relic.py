# -*- coding: utf-8 -*-
"""Final ownership layer for sealed relic agitation, slots, abilities and HUD.

This generator deliberately runs after every existing gameplay/UI generator.
It keeps the seven authored escape<N> functions, but replaces their random
caller, rebuilds the active-slot index, and composes relic state into the
existing two-layer actionbar.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from rpg_ui_style import (CYAN, DARK_GRAY, GRAY, HOLY, HOLY_LIGHT, RED,
                          RITUAL, WHITE, comp, lore, row)


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
FUNC = DP / "data/rpg/function"

LORDS = (
    (1, "路西法 · 傲慢", "#00491C"),
    (2, "利维坦 · 嫉妒", "#1B4F72"),
    (3, "亚巴顿 · 怠惰", "#6A6A70"),
    (4, "别西卜 · 暴食", "#5A6B1E"),
    (5, "萨麦尔 · 暴怒", "#7B241C"),
    (6, "贝利尔 · 色欲", "#5B2C6F"),
    (7, "玛门 · 贪婪", "#B7950B"),
)

OBJECTIVES = (
    "rpg_agit", "rpg_rel_n", "rpg_rel_1", "rpg_rel_2", "rpg_rel_w",
    "rpg_rel_cd", "rpg_rel_hold", "rpg_rel_gap", "rpg_rel_rec",
    "rpg_rel_src", "rpg_rel_pulse", "rpg_rel_left",
)

SEALED = "minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b}]"
USE_COMPONENTS = (
    "minecraft:food={nutrition:0,saturation:0f,can_always_eat:1b},"
    "minecraft:consumable={consume_seconds:100160f,animation:\"block\","
    "sound:\"minecraft:block.respawn_anchor.ambient\","
    "has_consume_particles:false,on_consume_effects:[]},"
    "minecraft:max_stack_size=1,"
)
BOX_COMPONENTS = (
    '"minecraft:food":{nutrition:0,saturation:0f,can_always_eat:1b},'
    '"minecraft:consumable":{consume_seconds:100160f,animation:"block",'
    'sound:"minecraft:block.respawn_anchor.ambient",has_consume_particles:false,'
    'on_consume_effects:[]},"minecraft:max_stack_size":1,'
)


def read(rel: str) -> str:
    return (FUNC / rel).read_text(encoding="utf-8")


def write(rel: str, source: str) -> None:
    target = FUNC / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def write_json(rel: str, value: object) -> None:
    target = DP / "data" / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8", newline="\n")


def patch_once(rel: str, needle: str, replacement: str) -> None:
    source = read(rel)
    if source.count(needle) != 1:
        raise RuntimeError("seal-relic anchor changed in %s" % rel)
    write(rel, source.replace(needle, replacement, 1))


def score(objective: str, colour: str = WHITE) -> dict:
    return {"score": {"name": "@s", "objective": objective},
            "color": colour, "bold": False, "italic": False}


def tell(*parts: dict) -> str:
    return "tellraw @s " + row(*parts)


def add_objectives() -> None:
    rel = "command/soreboard.mcfunction"
    source = read(rel)
    source = source.replace("scoreboard objectives add rpg_seal_roll dummy\n", "")
    additions = []
    for objective in OBJECTIVES:
        line = "scoreboard objectives add %s dummy" % objective
        if line not in source:
            additions.append(line)
    if additions:
        source = source.rstrip() + "\n" + "\n".join(additions) + "\n"
    write(rel, source)


def patch_relic_items() -> None:
    """Make every generated relic holdable and replace the obsolete surprise lore."""
    old_lore = "长期携带可能挣脱封印并重新降临"
    new_lore = "躁动达到 100 才会逃逸；圣水净化，潜行长按压制"
    box_pattern = re.compile(
        r'id:"minecraft:echo_shard",count:1,components:\{'
        r'(?=(?:(?!\}\},\{slot:).)*rpg_sealed)')
    for path in FUNC.rglob("*.mcfunction"):
        source = path.read_text(encoding="utf-8")
        if "rpg_sealed" not in source:
            continue
        changed = source.replace(old_lore, new_lore)
        lines = []
        for line in changed.splitlines():
            if "rpg_sealed" in line and "minecraft:echo_shard[" in line and \
                    "minecraft:food=" not in line:
                line = line.replace("minecraft:echo_shard[",
                                    "minecraft:echo_shard[" + USE_COMPONENTS)
            if "rpg_sealed" in line and 'id:"minecraft:echo_shard"' in line and \
                    '"minecraft:food"' not in line:
                line = box_pattern.sub(
                    'id:"minecraft:echo_shard",count:1,components:{' + BOX_COMPONENTS,
                    line)
            lines.append(line)
        changed = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
        if changed != source:
            path.write_text(changed, encoding="utf-8", newline="\n")

    # The canonical reward functions get complete, shared-palette instructions.
    for number, name, colour in LORDS:
        ability = {
            1: "本轮尚未显现能力",
            2: "反制：记录领主或罪仆术式；长按返还伤害",
            3: "拖滞：每 10 秒令近敌与自己缓慢",
            4: "吞噬残魂：16 格内敌对生物死亡时回复生命",
            5: "本轮尚未显现能力",
            6: "本轮尚未显现能力",
            7: "本轮尚未显现能力",
        }[number]
        name_json = row(comp("[封印遗物] ", HOLY, True), comp(name, colour))
        lore_json = lore([
            [comp(ability, HOLY_LIGHT)],
            [comp("背包顺序前两件生效；其余休眠。", GRAY)],
            [comp("携带每 10 秒躁动 +1；能力生效时 +3。", RITUAL)],
            [comp("圣水云每秒 -3；潜行长按 -20。", CYAN)],
            [comp("压制代价：能力冷却 30 秒，缓慢 I 8 秒。", RED)],
            [comp("躁动 100 时，最低槽位的生效遗物逃逸。", RED)],
        ])
        item = ("minecraft:echo_shard[" + USE_COMPONENTS +
                "minecraft:custom_name=" + name_json + ",minecraft:lore=" + lore_json +
                ",minecraft:enchantment_glint_override=true,"
                "minecraft:custom_data={holy_weapon_tag:1b,rpg_sealed:1b,rpg_lord:%d}]" % number)
        write("inquest/give/relic%d.mcfunction" % number, "give @s " + item)


def build_slot_index() -> None:
    lines = [
        "# seal relic active slot limit: 2",
        "scoreboard players set @s rpg_seal_i 0",
        "scoreboard players set @s rpg_rel_n 0",
        "scoreboard players set @s rpg_rel_1 0",
        "scoreboard players set @s rpg_rel_2 0",
        "tag @s remove rpg.seal.carrier",
    ]
    for number, _name, _colour in LORDS:
        lines.append("tag @s remove rpg.seal.active%d" % number)
    # Player slot grammar has two numeric groups: hotbar.0..8 followed by
    # inventory.0..26.  This is also the order players see while arranging a
    # carried loadout, and avoids the invalid inventory.27..35 aliases.
    slots = (["hotbar.%d" % i for i in range(9)] +
             ["inventory.%d" % i for i in range(27)])
    for slot in slots:
        for number, _name, _colour in LORDS:
            item = ("minecraft:echo_shard[minecraft:custom_data~"
                    "{rpg_sealed:1b,rpg_lord:%d}]" % number)
            lines.append(
                "execute if score @s rpg_rel_n matches 0 if items entity @s %s %s "
                "run scoreboard players set @s rpg_rel_1 %d" % (slot, item, number))
            lines.append(
                "execute if score @s rpg_rel_n matches 1 if items entity @s %s %s "
                "run scoreboard players set @s rpg_rel_2 %d" % (slot, item, number))
        lines.append(
            "execute if score @s rpg_rel_n matches ..1 if items entity @s %s %s "
            "run scoreboard players add @s rpg_rel_n 1" % (slot, SEALED))
    lines += [
        "execute if score @s rpg_rel_n matches 1..2 run tag @s add rpg.seal.carrier",
    ]
    for number, _name, _colour in LORDS:
        lines += [
            "execute if score @s rpg_rel_1 matches %d run tag @s add rpg.seal.active%d" %
            (number, number),
            "execute if score @s rpg_rel_2 matches %d run tag @s add rpg.seal.active%d" %
            (number, number),
        ]
    lines += [
        "execute unless entity @s[tag=rpg.seal.carrier] run scoreboard players set @s rpg_seal_t 0",
        "execute unless entity @s[tag=rpg.seal.carrier] run scoreboard players set @s rpg_rel_pulse 0",
    ]
    write("inquest/seal/reindex.mcfunction", "\n".join(lines))


def build_runtime() -> None:
    old = "\n".join([
        "scoreboard players add @s rpg_seal_i 1",
        "execute if score @s rpg_seal_i matches 100.. run function rpg:inquest/seal/reindex",
        "execute if entity @s[tag=rpg.seal.carrier] run function rpg:inquest/seal/tick",
        "execute unless entity @s[tag=rpg.seal.carrier] run scoreboard players set @s rpg_seal_t 0",
    ])
    patch_once("inquest/player_tick.mcfunction", old,
               "function rpg:inquest/seal/player_tick")

    write("inquest/seal/player_tick.mcfunction", """\
scoreboard players add @s rpg_agit 0
scoreboard players add @s rpg_rel_cd 0
scoreboard players add @s rpg_rel_gap 0
scoreboard players add @s rpg_seal_i 1
execute if score @s rpg_rel_cd matches 1.. run scoreboard players remove @s rpg_rel_cd 1
execute if score @s rpg_rel_gap matches 1.. run scoreboard players remove @s rpg_rel_gap 1
execute if score @s rpg_rel_gap matches ..0 run scoreboard players set @s rpg_rel_hold 0
execute if score @s rpg_seal_i matches 100.. run function rpg:inquest/seal/reindex
execute if entity @s[tag=rpg.seal.carrier] run function rpg:inquest/seal/tick
""")

    write("inquest/seal/tick.mcfunction", """\
# Deterministic agitation curve. Escape has one trigger: rpg_agit reaching 100.
scoreboard players add @s rpg_seal_t 1
scoreboard players add @s rpg_rel_w 1
scoreboard players add @s rpg_rel_pulse 1
execute if score @s rpg_seal_t matches 200.. run scoreboard players add @s rpg_agit 1
execute if score @s rpg_seal_t matches 200.. run scoreboard players set @s rpg_seal_t 0
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
function rpg:inquest/seal/warning_tick
execute if score @s rpg_agit matches 100.. run return run function rpg:inquest/seal/escape_gate
execute if score @s rpg_rel_pulse matches 200.. run scoreboard players set @s rpg_rel_pulse 0
execute if score @s rpg_rel_pulse matches 0 if score @s rpg_rel_cd matches ..0 if entity @s[tag=rpg.seal.active3] run function rpg:inquest/seal/ability/abaddon_scan
""")

    write("inquest/seal/escape_gate.mcfunction", """\
execute unless score @s rpg_agit matches 100.. run return 0
function rpg:inquest/seal/reindex
execute unless entity @s[tag=rpg.seal.carrier] run return 0
scoreboard players set @s rpg_agit 0
function rpg:inquest/seal/escape
""")
    dispatch = []
    for number, _name, _colour in LORDS:
        dispatch.append(
            "execute if score @s rpg_rel_1 matches %d run return run function "
            "rpg:inquest/seal/escape%d" % (number, number))
    write("inquest/seal/escape.mcfunction", "\n".join(dispatch))


def build_warnings() -> None:
    write("inquest/seal/warning_tick.mcfunction", """\
execute if score @s rpg_agit matches ..39 run tag @s remove rpg.seal.warn40
execute if score @s rpg_agit matches ..69 run tag @s remove rpg.seal.warn70
execute if score @s rpg_agit matches ..89 run tag @s remove rpg.seal.warn90
execute if score @s rpg_agit matches 40..69 unless entity @s[tag=rpg.seal.warn40] run function rpg:inquest/seal/warn_agitated
execute if score @s rpg_agit matches 70..89 unless entity @s[tag=rpg.seal.warn70] run function rpg:inquest/seal/warn_danger
execute if score @s rpg_agit matches 70..89 if entity @s[tag=rpg.seal.warn70] if score @s rpg_rel_w matches 200.. run function rpg:inquest/seal/warn_danger
execute if score @s rpg_agit matches 90..99 unless entity @s[tag=rpg.seal.warn90] run function rpg:inquest/seal/warn_critical
execute if score @s rpg_agit matches 90..99 if entity @s[tag=rpg.seal.warn90] if score @s rpg_rel_w matches 60.. run function rpg:inquest/seal/warn_critical
""")
    write("inquest/seal/warn_agitated.mcfunction", "\n".join([
        "tag @s add rpg.seal.warn40",
        tell(comp("[遗物躁动] ", RITUAL, True),
             comp("能力已增强；每次能力生效会再增加 3 点躁动。", GRAY)),
    ]))
    write("inquest/seal/warn_danger.mcfunction", "\n".join([
        "tag @s add rpg.seal.warn70",
        "scoreboard players set @s rpg_rel_w 0",
        tell(comp("[遗物危险] ", HOLY, True),
             comp("圣水云每秒净化 3；潜行长按可压制 20，但会冷却 30 秒并缓慢 8 秒。", GRAY)),
    ]))
    write("inquest/seal/warn_critical.mcfunction", "\n".join([
        "tag @s add rpg.seal.warn90",
        "scoreboard players set @s rpg_rel_w 0",
        "scoreboard players set @s rpg_rel_left 100",
        "scoreboard players operation @s rpg_rel_left -= @s rpg_agit",
        "tellraw @s " + row(comp("[遗物临界] ", RED, True), comp("距逃逸还差 ", GRAY),
                            score("rpg_rel_left", RED), comp(" 点！立即净化或压制。", RED)),
    ]))


def build_use_and_abilities() -> None:
    write_json("rpg/advancement/inquest/seal_use.json", {
        "criteria": {"use": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"predicates": {
                "minecraft:custom_data": "{rpg_sealed:1b}",
            }}},
        }},
        "rewards": {"function": "rpg:inquest/seal/use"},
    })
    active_checks = []
    for number, _name, _colour in LORDS:
        held = ("minecraft:echo_shard[minecraft:custom_data~"
                "{rpg_sealed:1b,rpg_lord:%d}]" % number)
        active_checks += [
            "execute if score @s rpg_rel_1 matches %d if items entity @s weapon.mainhand %s run tag @s add rpg.seal.held_active" % (number, held),
            "execute if score @s rpg_rel_2 matches %d if items entity @s weapon.mainhand %s run tag @s add rpg.seal.held_active" % (number, held),
        ]
    use_lines = [
        "advancement revoke @s only rpg:inquest/seal_use",
        "function rpg:inquest/seal/reindex",
        "scoreboard players set @s rpg_rel_gap 3",
        "scoreboard players add @s rpg_rel_hold 1",
        "tag @s remove rpg.seal.held_active",
    ] + active_checks + [
        "execute if score @s rpg_rel_hold matches 30 unless entity @s[tag=rpg.seal.held_active] run tellraw @s " +
        row(comp("[遗物休眠] ", DARK_GRAY, True), comp("它不在背包顺序的前两个生效槽位。", GRAY)),
        "execute if score @s rpg_rel_hold matches 30 if entity @s[tag=rpg.seal.held_active] if predicate rpg:sneaking run return run function rpg:inquest/seal/suppress",
        "execute if score @s rpg_rel_hold matches 30 if entity @s[tag=rpg.seal.held_active] unless predicate rpg:sneaking if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:2}] run return run function rpg:inquest/seal/ability/leviathan",
    ]
    write("inquest/seal/use.mcfunction", "\n".join(use_lines))

    write("inquest/seal/suppress.mcfunction", """\
scoreboard players remove @s rpg_agit 20
execute if score @s rpg_agit matches ..-1 run scoreboard players set @s rpg_agit 0
scoreboard players set @s rpg_rel_cd 600
scoreboard players set @s rpg_rel_hold 31
effect give @s minecraft:slowness 8 0 true
tellraw @s ["",{"text":"[遗物压制] ","color":"#62D9E8","bold":true,"italic":false},{"text":"躁动 -20；代价：全部遗物能力冷却 30 秒，缓慢 I 持续 8 秒。","color":"gray","bold":false,"italic":false}]
playsound minecraft:block.respawn_anchor.deplete player @s ~ ~ ~ 0.8 1.4
""")

    write("inquest/seal/ability/leviathan.mcfunction", """\
scoreboard players set @s rpg_rel_hold 31
execute if score @s rpg_rel_cd matches 1.. run return run tellraw @s ["",{"text":"[遗物冷却] ","color":"#62D9E8","bold":true,"italic":false},{"text":"压制余波仍在，尚不能动用反制。","color":"gray","italic":false}]
execute unless score @s rpg_rel_rec matches 1 run return run tellraw @s ["",{"text":"[利维坦] ","color":"#1B4F72","bold":true,"italic":false},{"text":"尚无可反制的术式","color":"gray","italic":false}]
tag @s add rpg.seal.cast
execute if score @s rpg_rel_src matches 2 run function rpg:inquest/seal/ability/reflect_drown
execute unless score @s rpg_rel_src matches 2 run function rpg:inquest/seal/ability/reflect_magic
tag @s remove rpg.seal.cast
scoreboard players set @s rpg_rel_rec 0
scoreboard players set @s rpg_rel_src 0
scoreboard players add @s rpg_agit 3
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
tellraw @s ["",{"text":"[利维坦 · 反制] ","color":"#1B4F72","bold":true,"italic":false},{"text":"术式已同源返还；记录清空，躁动 +3。","color":"gray","italic":false}]
""")
    for source_name, damage_type in (("magic", "minecraft:magic"),
                                     ("drown", "minecraft:drown")):
        lines = []
        for amount, lo, hi in ((4, 0, 39), (6, 40, 69), (8, 70, 89), (12, 90, 99)):
            match = "%d..%d" % (lo, hi)
            lines += [
                "execute if score @a[tag=rpg.seal.cast,limit=1] rpg_agit matches %s as @e[type=#rpg:seal_hostile,type=!minecraft:player,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] run damage @s %d %s by @a[tag=rpg.seal.cast,limit=1]" % (match, amount, damage_type),
                "execute if score @a[tag=rpg.seal.cast,limit=1] rpg_agit matches %s as @e[tag=rpg.demon,distance=..8] run damage @s %d %s by @a[tag=rpg.seal.cast,limit=1]" % (match, amount, damage_type),
                "execute if score @a[tag=rpg.seal.cast,limit=1] rpg_agit matches %s as @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] run damage @s %d %s by @a[tag=rpg.seal.cast,limit=1]" % (match, amount, damage_type),
            ]
        write("inquest/seal/ability/reflect_%s.mcfunction" % source_name,
              "\n".join(lines))

    write("inquest/seal/ability/record_magic.mcfunction", """\
execute unless entity @s[type=minecraft:player,tag=rpg.seal.active2] run return 0
scoreboard players set @s rpg_rel_rec 1
scoreboard players set @s rpg_rel_src 1
""")
    write("inquest/seal/ability/record_drown.mcfunction", """\
execute unless entity @s[type=minecraft:player,tag=rpg.seal.active2] run return 0
scoreboard players set @s rpg_rel_rec 1
scoreboard players set @s rpg_rel_src 2
""")

    write("inquest/seal/ability/abaddon_scan.mcfunction", """\
tag @s remove rpg.seal.aura_target
execute at @s if entity @e[type=#rpg:seal_hostile,type=!minecraft:player,distance=..8] run tag @s add rpg.seal.aura_target
execute at @s if entity @e[tag=rpg.demon,distance=..8] run tag @s add rpg.seal.aura_target
execute at @s if entity @e[tag=rpg.demon.minion,distance=..8] run tag @s add rpg.seal.aura_target
execute if entity @s[tag=rpg.seal.aura_target] run function rpg:inquest/seal/ability/abaddon
tag @s remove rpg.seal.aura_target
""")
    abaddon = [
        "effect give @s minecraft:slowness 11 0 true",
    ]
    for amplifier, lo, hi in ((0, 0, 39), (1, 40, 69), (1, 70, 89), (2, 90, 99)):
        match = "%d..%d" % (lo, hi)
        for selector in (
            "@e[type=#rpg:seal_hostile,type=!minecraft:player,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8]",
            "@e[tag=rpg.demon,distance=..8]",
            "@e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8]",
        ):
            abaddon.append(
                "execute if score @s rpg_agit matches %s run effect give %s minecraft:slowness 11 %d true" %
                (match, selector, amplifier))
    abaddon += [
        "scoreboard players add @s rpg_agit 3",
        "execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100",
    ]
    write("inquest/seal/ability/abaddon.mcfunction", "\n".join(abaddon))

    # Standard hostile types; tagged lords/minions are included separately at runtime.
    write_json("rpg/tags/entity_type/seal_hostile.json", {"values": [
        "minecraft:blaze", "minecraft:bogged", "minecraft:breeze",
        "minecraft:cave_spider", "minecraft:creaking", "minecraft:creeper",
        "minecraft:drowned", "minecraft:elder_guardian", "minecraft:ender_dragon",
        "minecraft:endermite", "minecraft:evoker", "minecraft:ghast",
        "minecraft:guardian", "minecraft:hoglin", "minecraft:husk",
        "minecraft:illusioner", "minecraft:magma_cube", "minecraft:phantom",
        "minecraft:piglin_brute", "minecraft:pillager", "minecraft:ravager",
        "minecraft:shulker", "minecraft:silverfish", "minecraft:skeleton",
        "minecraft:slime", "minecraft:spider", "minecraft:stray", "minecraft:vex",
        "minecraft:vindicator", "minecraft:warden", "minecraft:witch",
        "minecraft:wither", "minecraft:wither_skeleton", "minecraft:zoglin",
        "minecraft:zombie", "minecraft:zombie_villager",
    ]})


def patch_hurt_and_skill_paths() -> None:
    # Reuse the already-batched rpg.hurt walk: no new every-tick world traversal.
    rel = "command/index.mcfunction"
    source = read(rel)
    needle = "execute as @a at @s run function rpg:command/damage_scan"
    hook = "\n" + "\n".join([
        "execute if entity @a[tag=rpg.seal.active4,limit=1] as @e[tag=rpg.hurt,type=#rpg:seal_hostile,tag=!rpg.demon,tag=!rpg.demon.minion,nbt={Health:0.0f}] at @s run function rpg:inquest/seal/ability/beelzebub_death",
        "execute if entity @a[tag=rpg.seal.active4,limit=1] as @e[tag=rpg.hurt,tag=rpg.demon,nbt={Health:0.0f}] at @s run function rpg:inquest/seal/ability/beelzebub_death",
        "execute if entity @a[tag=rpg.seal.active4,limit=1] as @e[tag=rpg.hurt,tag=rpg.demon.minion,tag=!rpg.demon,nbt={Health:0.0f}] at @s run function rpg:inquest/seal/ability/beelzebub_death",
    ])
    if hook.strip() not in source:
        if source.count(needle) != 1:
            raise RuntimeError("rpg.hurt hook anchor changed")
        write(rel, source.replace(needle, needle + hook, 1))
    write("inquest/seal/ability/beelzebub_death.mcfunction",
          "execute as @a[tag=rpg.seal.active4,scores={rpg_rel_cd=..0},distance=..16] run function rpg:inquest/seal/ability/beelzebub_heal")
    write("inquest/seal/ability/beelzebub_heal.mcfunction", """\
# 吞噬残魂：档位越高回得越多。
#
# 原本这里写的是 `regeneration 12t/18t/24t/36t 3`，算得很准 ——
# 再生 IV 每 6 刻跳一次，那四个时长正好回 2/3/4/6 点，严丝合缝对上
# 1x / 1.5x / 2x / 3x 的曲线。**但 `effect give` 的时长只收整数秒**，
# `t` 后缀是 `/time` 与 `schedule` 的语法。带 t 的那一版服务器会
# 拒绝加载整个函数，而 validate 抓不到（见 check_effect_duration.py）。
#
# 整秒粒度下精确的 2/3/4/6 表达不出来，所以改成调等级、保住"越躁动
# 回得越多"的形状：约 1 / 3 / 6 / 13 点。**这条待实机重新配平** ——
# 临界档 13 点偏高，但保持单调递增比凑准数字要紧。
execute if score @s rpg_agit matches 0..39 run effect give @s minecraft:regeneration 1 2 true
execute if score @s rpg_agit matches 40..69 run effect give @s minecraft:regeneration 1 3 true
execute if score @s rpg_agit matches 70..89 run effect give @s minecraft:regeneration 1 4 true
execute if score @s rpg_agit matches 90..99 run effect give @s minecraft:regeneration 2 4 true
scoreboard players add @s rpg_agit 3
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
""")

    patched_boss = patched_minion = 0
    roots = ((FUNC / "taint", "rpg.dm.cast", "boss"),
             (FUNC / "minion/ability/resolve", "rpg.demon.minion.caster", "minion"))
    for root, source_tag, kind in roots:
        for path in root.rglob("*.mcfunction"):
            lines = path.read_text(encoding="utf-8").splitlines()
            out = []
            changed = False
            for line in lines:
                if "damage @s " in line and source_tag in line:
                    damage_at = line.index("damage @s ")
                    prefix = line[:damage_at]
                    if prefix.endswith("run "):
                        prefix = prefix[:-4] + "run "
                    record = "rpg:inquest/seal/ability/record_" + (
                        "drown" if " minecraft:drown " in line else "magic")
                    record_line = prefix + "function " + record
                    if not out or out[-1] != record_line:
                        out.append(record_line)
                        changed = True
                        if kind == "boss":
                            patched_boss += 1
                        else:
                            patched_minion += 1
                out.append(line)
            if changed:
                path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    if patched_boss < 20 or patched_minion < 10:
        raise RuntimeError("skill damage hooks unexpectedly sparse: boss=%d minion=%d" %
                           (patched_boss, patched_minion))


def patch_holy_water() -> None:
    rel = "rite/pool_beat.mcfunction"
    source = read(rel)
    needle = "execute as @a[distance=..4] run scoreboard players remove @s rpg_taint 1"
    insert = "\n".join([
        needle,
        "execute as @a[distance=..4,scores={rpg_agit=1..}] run scoreboard players remove @s rpg_agit 3",
        "execute as @a[distance=..4,scores={rpg_agit=..-1}] run scoreboard players set @s rpg_agit 0",
    ])
    patch_once(rel, needle, insert)


def build_panel() -> None:
    rel = "panel/inquest.mcfunction"
    source = read(rel)
    if not source.startswith("function rpg:inquest/seal/reindex\n"):
        source = "function rpg:inquest/seal/reindex\n" + source
    anchor = tell(comp("携带圣器见证三种不同招式，即可确认真名。", GRAY))
    if anchor not in source:
        # The panel polish pass may have adjusted copy; the home button is stable.
        anchor = next(line for line in source.splitlines() if "rpg_panel set 8" in line)
    rows = [
        tell(comp("+-------- 封印遗物 --------+", RITUAL, True)),
        "tellraw @s " + row(comp("躁动：", GRAY), score("rpg_agit", RITUAL),
                           comp(" / 100　", DARK_GRAY), comp("前两件生效", HOLY_LIGHT, True)),
    ]
    for slot_obj, label in (("rpg_rel_1", "生效 I　"), ("rpg_rel_2", "生效 II ")):
        rows.append("execute if score @s %s matches 0 run tellraw @s %s" %
                    (slot_obj, row(comp(label, GRAY), comp("空", DARK_GRAY))))
        for number, name, colour in LORDS:
            rows.append("execute if score @s %s matches %d run tellraw @s %s" %
                        (slot_obj, number, row(comp(label, GRAY), comp(name, colour, True))))
    rows += [
        tell(comp("其余遗物休眠：无能力，也不推动躁动。", DARK_GRAY)),
        tell(comp("放任：", RITUAL, True), comp("躁动越高能力越强；能力生效再 +3。", GRAY)),
        tell(comp("净化：", CYAN, True), comp("站在驱魔圣水云中，每秒 -3（消耗圣水）。", GRAY)),
        tell(comp("压制：", HOLY, True), comp("潜行长按生效遗物 -20；代价为 30 秒能力冷却与 8 秒缓慢 I。", GRAY)),
    ]
    if "+-------- 封印遗物 --------+" not in source:
        source = source.replace(anchor, "\n".join(rows) + "\n" + anchor, 1)
    write(rel, source)


def build_hud() -> None:
    stage_specs = ((0, 39, "\uf300", DARK_GRAY), (40, 69, "\uf301", RITUAL),
                   (70, 89, "\uf302", HOLY), (90, 100, "\uf303", RED))
    lines = ["data modify storage rpg:hud r set value '{\"text\":\"\"}'"]
    for lo, hi, glyph, _colour in stage_specs:
        lines += [
            "execute if score @s rpg_agit matches %d..%d run data modify storage rpg:hud top set value '%s'" %
            (lo, hi, json.dumps({"text": glyph, "font": "rpg:combat_prompt",
                                 "color": "white", "italic": False}, ensure_ascii=True,
                                separators=(",", ":"))),
            "execute if score @s rpg_agit matches %d..%d run data modify storage rpg:hud back set value '%s'" %
            (lo, hi, json.dumps({"text": "\uf310", "font": "rpg:combat_prompt"},
                                ensure_ascii=True, separators=(",", ":"))),
        ]
    for filled in range(11):
        lo = filled * 10
        hi = 100 if filled == 10 else lo + 9
        colour = DARK_GRAY if hi < 40 else RITUAL if hi < 70 else HOLY if hi < 90 else RED
        stage_name = ("沉眠" if hi < 40 else "躁动" if hi < 70 else
                      "危险" if hi < 90 else "临界")
        parts = [comp(stage_name + " ", colour, True), comp("▰" * filled, colour),
                 comp("▱" * (10 - filled), DARK_GRAY), comp(" ", GRAY),
                 score("rpg_agit", colour), comp("/100　│　", DARK_GRAY)]
        payload = json.dumps([""] + parts, ensure_ascii=False, separators=(",", ":"))
        lines.append("execute if score @s rpg_agit matches %d..%d run data modify storage rpg:hud r set value '%s'" %
                     (lo, hi, payload.replace("'", "\\'")))
    write("inquest/seal/hud.mcfunction", "\n".join(lines))
    write("hud/seal/render.mcfunction",
          '$title @s actionbar ["",$(top),$(back),$(r),$(a),$(b),$(c),$(d)]')
    write("hud/seal/event.mcfunction", """\
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud a set from storage rpg:hud e
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud b set value '{"text":""}'
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud c set value '{"text":""}'
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud d set value '{"text":""}'
execute if entity @s[scores={rpg_hud_dmt=1..}] run return run function rpg:hud/demon/render with storage rpg:hud
$execute if entity @s[tag=rpg.seal.carrier] run return run title @s actionbar ["",$(top),$(back),$(r),$(e)]
$title @s actionbar $(e)
""")

    hud = read("hud/hud.mcfunction")
    # 锚点必须**整行**匹配。同样这段文本还作为面板关闭 HUD 那条分支的后缀
    # 出现（`...[tag=rpg.panel.hud_off] run scoreboard players add @s rpg_hud_mt 0`），
    # 只按子串数会得到 2，于是下面那道唯一性检查会误判成"锚点变了"而拒绝落地。
    line = "scoreboard players add @s rpg_hud_mt 0"
    init_anchor = "\n" + line + "\n"
    init = ("\n" + line + "\ndata modify storage rpg:hud r set value '{\"text\":\"\"}'\n"
            "execute if entity @s[tag=rpg.seal.carrier] run function rpg:inquest/seal/hud\n")
    if "function rpg:inquest/seal/hud" not in hud:
        if hud.count(init_anchor) != 1:
            raise RuntimeError("HUD init anchor changed")
        write("hud/hud.mcfunction", hud.replace(init_anchor, init, 1))

    status = read("hud/status.mcfunction")
    old_routes = "\n".join([
        "execute if entity @s[scores={rpg_hud_on=1,rpg_hud_dmt=1..}] run function rpg:hud/demon/render with storage rpg:hud",
        "execute if entity @s[scores={rpg_hud_on=1,rpg_hud_dmt=0}] run function rpg:hud/render with storage rpg:hud",
        "execute if entity @s[scores={rpg_hud_on=0,rpg_hud_dmt=1..}] run function rpg:hud/demon/solo",
    ])
    new_routes = "\n".join([
        "execute if entity @s[scores={rpg_hud_dmt=1..},tag=rpg.seal.carrier] run function rpg:hud/demon/render with storage rpg:hud",
        "execute if entity @s[scores={rpg_hud_on=1,rpg_hud_dmt=1..},tag=!rpg.seal.carrier] run function rpg:hud/demon/render with storage rpg:hud",
        "execute if entity @s[scores={rpg_hud_dmt=0},tag=rpg.seal.carrier] run function rpg:hud/seal/render with storage rpg:hud",
        "execute if entity @s[scores={rpg_hud_on=1,rpg_hud_dmt=0},tag=!rpg.seal.carrier] run function rpg:hud/render with storage rpg:hud",
        "execute if entity @s[scores={rpg_hud_on=0,rpg_hud_dmt=1..},tag=!rpg.seal.carrier] run function rpg:hud/demon/solo",
    ])
    patch_once("hud/status.mcfunction", old_routes, new_routes)

    # Demon casts own the upper row. Relic number/bar stays on the lower row.
    for path in (FUNC / "hud/demon").glob("r*.mcfunction"):
        source = path.read_text(encoding="utf-8")
        if "$(r)" not in source:
            source = source.replace("$(a),$(b),$(c),$(d)", "$(r),$(a),$(b),$(c),$(d)")
            path.write_text(source, encoding="utf-8", newline="\n")

    # Charging and one-shot rows retain lower-row priority, while demon cast
    # still beats the persistent relic stage on the globally unique upper row.
    event_files = [FUNC / "hud/msg.mcfunction"] + sorted((FUNC / "hud").glob("s*.mcfunction"))
    title_re = re.compile(r"^(?P<prefix>.*run )title @s actionbar (?P<body>\[.*\])$")
    for path in event_files:
        out = []
        changed = False
        for line in path.read_text(encoding="utf-8").splitlines():
            match = title_re.match(line)
            if not match:
                out.append(line)
                continue
            prefix, body = match.group("prefix"), match.group("body")
            out.append(prefix + "data modify storage rpg:hud e set value '" +
                       body.replace("'", "\\'") + "'")
            out.append(prefix + "function rpg:hud/seal/event with storage rpg:hud")
            changed = True
        if changed:
            path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    add_objectives()
    patch_relic_items()
    build_slot_index()
    build_runtime()
    build_warnings()
    build_use_and_abilities()
    patch_hurt_and_skill_paths()
    patch_holy_water()
    build_panel()
    build_hud()
    print("seal relics: deterministic agitation, 2 slots, 3 abilities and two-layer HUD wired")


if __name__ == "__main__":
    main()
