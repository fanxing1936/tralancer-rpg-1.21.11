# -*- coding: utf-8 -*-
"""Build the persistent 35-member Goetic legion ecosystem.

The first thirty-five spirits in Goetic order are assigned five at a time to
the seven established sin lords.  Each cohort has a vanguard, hunter,
ritualist, hexer and executioner.  Manual summons are permanent and require no
boss; ritual phase two introduces one missing role per pressure cycle.
"""

import io
import json
import os
import shutil
import sys


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
LOOT = os.path.join(DP, "data/rpg/loot_table")
ADV = os.path.join(DP, "data/rpg/advancement")


LORDS = {
    1: {"slug": "lucifer", "lord": "路西法", "base": "#00491C", "light": "#72D99A", "particle": "end_rod", "sound": "minecraft:entity.evoker.prepare_attack", "loot": "minecraft:emerald",
        "spirits": [("bael", "巴力"), ("agares", "阿加雷斯"), ("vassago", "瓦沙克"), ("samigina", "萨米基纳"), ("marbas", "马尔巴士")]},
    2: {"slug": "leviathan", "lord": "利维坦", "base": "#1B4F72", "light": "#62D9E8", "particle": "nautilus", "sound": "minecraft:entity.guardian.attack", "loot": "minecraft:prismarine_crystals",
        "spirits": [("valefor", "华利弗"), ("amon", "亚蒙"), ("barbatos", "巴巴托斯"), ("paimon", "派蒙"), ("buer", "布耶尔")]},
    3: {"slug": "abaddon", "lord": "亚巴顿", "base": "#5B5B62", "light": "#C2C2CC", "particle": "sculk_soul", "sound": "minecraft:entity.warden.heartbeat", "loot": "minecraft:bone",
        "spirits": [("gusion", "古辛"), ("sitri", "西迪"), ("beleth", "贝雷特"), ("leraje", "列拉金"), ("eligos", "艾利欧格")]},
    4: {"slug": "beelzebub", "lord": "别西卜", "base": "#596B18", "light": "#B5D957", "particle": "spore_blossom_air", "sound": "minecraft:entity.spider.ambient", "loot": "minecraft:rotten_flesh",
        "spirits": [("zepar", "桀派"), ("botis", "布提斯"), ("bathin", "巴钦"), ("sallos", "塞列欧斯"), ("purson", "布松")]},
    5: {"slug": "samael", "lord": "萨麦尔", "base": "#7B241C", "light": "#FF665E", "particle": "soul_fire_flame", "sound": "minecraft:entity.ravager.roar", "loot": "minecraft:blaze_powder",
        "spirits": [("marax", "莫拉格斯"), ("ipos", "因波斯"), ("aim", "艾姆"), ("naberius", "纳贝流士"), ("glasya_labolas", "格拉夏·拉波拉斯")]},
    6: {"slug": "belial", "lord": "贝利尔", "base": "#57256B", "light": "#C28BE0", "particle": "witch", "sound": "minecraft:entity.illusioner.prepare_blindness", "loot": "minecraft:amethyst_shard",
        "spirits": [("bune", "布涅"), ("ronove", "罗诺比"), ("berith", "比利士"), ("astaroth", "亚斯塔禄"), ("forneus", "佛纽司")]},
    7: {"slug": "mammon", "lord": "玛门", "base": "#987B08", "light": "#FFD85A", "particle": "wax_on", "sound": "minecraft:block.amethyst_block.chime", "loot": "minecraft:gold_nugget",
        "spirits": [("foras", "佛拉斯"), ("asmoday", "阿斯摩太"), ("gaap", "盖布"), ("furfur", "佛尔佛尔"), ("marchosias", "马可西亚斯")]},
}

ROLES = {
    1: {"name": "先锋", "entity": "vindicator", "health": 92, "attack": 8, "armor": 10, "speed": 0.27, "weapon": "minecraft:iron_sword", "cd": 110, "material": "minecraft:iron_nugget"},
    2: {"name": "猎手", "entity": "pillager", "health": 66, "attack": 6, "armor": 5, "speed": 0.31, "weapon": "minecraft:crossbow", "cd": 85, "material": "minecraft:arrow"},
    3: {"name": "司祭", "entity": "evoker", "health": 76, "attack": 4, "armor": 7, "speed": 0.0, "weapon": "minecraft:book", "cd": 125, "material": "minecraft:glowstone_dust", "no_ai": True},
    4: {"name": "咒使", "entity": "illusioner", "health": 70, "attack": 6, "armor": 6, "speed": 0.29, "weapon": "minecraft:bow", "cd": 100, "material": "minecraft:spider_eye"},
    5: {"name": "处刑者", "entity": "vindicator", "health": 108, "attack": 11, "armor": 8, "speed": 0.33, "weapon": "minecraft:iron_axe", "cd": 75, "material": "minecraft:redstone"},
}

OBJECTIVES = ("rpg_mn_lord", "rpg_mn_role", "rpg_mn_cd", "rpg_mn_tick", "rpg_mn_slot")


def fpath(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(fpath(rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, content):
    target = fpath(rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content.rstrip("\n") + "\n")


def write_json(root, rel, value):
    target = os.path.join(root, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def reset_generated_trees():
    for target in (fpath("minion"), os.path.join(LOOT, "minion"), os.path.join(ADV, "minion")):
        if os.path.isdir(target):
            shutil.rmtree(target)


def patch_scoreboard_and_hooks():
    rel = "command/soreboard.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines() if "rpg_mn_life" not in line).rstrip()
    for objective in OBJECTIVES:
        line = "scoreboard objectives add %s dummy" % objective
        if line not in src:
            src += "\n" + line
    write(rel, src)

    rel = "exorcism.mcfunction"
    lines = [line for line in read(rel).splitlines() if "罪仆生态" not in line and "function rpg:minion/tick" not in line]
    lines += ["", "# 罪仆生态：仅场上确有罪仆时推进十刻节拍。", "execute if entity @e[tag=rpg.demon.minion,limit=1] run function rpg:minion/tick"]
    write(rel, "\n".join(lines))

    rel = "taint/cast.mcfunction"
    lines = [line for line in read(rel).splitlines() if "function rpg:minion/summon_try" not in line and "每轮第二次普通出手" not in line]
    write(rel, "\n".join(lines))

    rel = "inquest/phase2/pressure.mcfunction"
    lines = [line for line in read(rel).splitlines() if "function rpg:minion/phase2_summon" not in line]
    needle = "function rpg:inquest/phase2/pressure_core"
    if needle not in lines:
        raise RuntimeError("phase2 pressure hook point changed")
    lines.insert(lines.index(needle) + 1, "function rpg:minion/phase2_summon")
    write(rel, "\n".join(lines))


def name_json(lord, role, spirit):
    return json.dumps([
        "",
        {"text": "[罪仆·%s] " % role["name"], "color": lord["base"], "bold": True, "italic": False},
        {"text": spirit[1], "color": lord["light"], "bold": False, "italic": False},
    ], ensure_ascii=False, separators=(",", ":"))


def summon_snbt(index, role_index, lord, role, spirit):
    no_ai = ",NoAI:1b" if role.get("no_ai") else ""
    return (
        "{Tags:[\"rpg.demon.minion\",\"rpg.demon.minion.new\",\"rpg.demon.minion.lord%d\",\"rpg.demon.minion.role%d\"],"
        "CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b%s,CustomName:%s,Health:%sf,"
        "active_effects:[{id:\"minecraft:fire_resistance\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:[{id:\"minecraft:max_health\",base:%sf},{id:\"minecraft:attack_damage\",base:%sf},"
        "{id:\"minecraft:armor\",base:%sf},{id:\"minecraft:follow_range\",base:36f},"
        "{id:\"minecraft:movement_speed\",base:%sf},{id:\"minecraft:knockback_resistance\",base:0.35f}],"
        "equipment:{mainhand:{id:\"%s\",count:1}},drop_chances:{mainhand:0f},"
        "DeathLootTable:\"rpg:minion/%s/%s\"}"
    ) % (index, role_index, no_ai, name_json(lord, role, spirit), role["health"], role["health"], role["attack"], role["armor"], role["speed"], role["weapon"], lord["slug"], spirit[0])


def tellraw_summon(lord, role, spirit):
    component = [
        "",
        {"text": "[罪群] ", "color": lord["base"], "bold": True, "italic": False},
        {"text": lord["lord"] + " · ", "color": lord["base"], "bold": False, "italic": False},
        {"text": role["name"] + " ", "color": "gray", "bold": False, "italic": False},
        {"text": spirit[1], "color": lord["light"], "bold": False, "italic": False},
        {"text": "应召现身。", "color": "dark_gray", "bold": False, "italic": False},
    ]
    return "tellraw @a[distance=..24,gamemode=!spectator] " + json.dumps(component, ensure_ascii=False, separators=(",", ":"))


def build_summons():
    phase = [
        "# 二阶段每次压力轮换一个职责；存活的同柱同职不会重复出现。",
        "scoreboard players add @s rpg_mn_slot 1",
        "execute if score @s rpg_mn_slot matches 6.. run scoreboard players set @s rpg_mn_slot 1",
    ]
    for lord_index, lord in LORDS.items():
        all_lines = ["# %s麾下五职；手动调用时不检查 Boss 与人口上限。" % lord["lord"]]
        for role_index, spirit in enumerate(lord["spirits"], 1):
            role = ROLES[role_index]
            rel = "minion/summon/%s/%s.mcfunction" % (lord["slug"], spirit[0])
            lines = [
                "# %s麾下%s：%s。可独立、永久存活。" % (lord["lord"], role["name"], spirit[1]),
                "summon minecraft:%s ~ ~ ~ %s" % (role["entity"], summon_snbt(lord_index, role_index, lord, role, spirit)),
                "scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord %d" % lord_index,
                "scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role %d" % role_index,
                "scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd %d" % (role["cd"] // 2),
                "tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new",
                "particle %s ~ ~1 ~ 0.55 0.75 0.55 0.035 18" % lord["particle"],
                "particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10",
                "playsound %s hostile @a[distance=..28] ~ ~ ~ 0.55 0.9" % lord["sound"],
                tellraw_summon(lord, role, spirit),
            ]
            write(rel, "\n".join(lines))
            all_lines.append("function rpg:minion/summon/%s/%s" % (lord["slug"], spirit[0]))
            phase.append(
                "execute if score @s rpg_dm_lord matches %d if score @s rpg_mn_slot matches %d unless entity @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d,rpg_mn_role=%d},distance=..36,limit=1] run function rpg:minion/summon/%s/%s"
                % (lord_index, role_index, lord_index, role_index, lord["slug"], spirit[0])
            )
        write("minion/summon/%s/all.mcfunction" % lord["slug"], "\n".join(all_lines))
    write("minion/phase2_summon.mcfunction", "\n".join(phase))


def transition(lord, count=12):
    colors = {
        1: ("0.19,0.85,0.49", "0.0,0.18,0.07"), 2: ("0.25,0.78,0.93", "0.02,0.16,0.31"),
        3: ("0.76,0.76,0.82", "0.10,0.10,0.12"), 4: ("0.70,0.84,0.34", "0.18,0.23,0.05"),
        5: ("0.94,0.20,0.18", "0.25,0.01,0.01"), 6: ("0.76,0.47,0.88", "0.18,0.04,0.25"),
        7: ("1.0,0.79,0.20", "0.28,0.17,0.01"),
    }
    a, b = colors[lord]
    return "particle dust_color_transition{from_color:[%s],to_color:[%s],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 %d" % (a, b, count)


def player_effect(effect, seconds, amplifier, radius):
    return "effect give @a[distance=..%d,gamemode=!spectator,gamemode=!creative] minecraft:%s %d %d true" % (radius, effect, seconds, amplifier)


def build_runtime_and_abilities():
    write("minion/tick.mcfunction", """# 35 种罪仆共用十刻节拍，场上无罪仆时不会进入本系统。
scoreboard players add #clock rpg_mn_tick 1
execute if score #clock rpg_mn_tick matches 10.. run function rpg:minion/beat
""")
    write("minion/beat.mcfunction", """scoreboard players set #clock rpg_mn_tick 0
execute as @e[tag=rpg.demon.minion] at @s run function rpg:minion/entity_tick
""")
    write("minion/entity_tick.mcfunction", """execute if entity @s[scores={rpg_mn_cd=1..}] run scoreboard players remove @s rpg_mn_cd 10
execute unless entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run return 0
execute if entity @s[scores={rpg_mn_cd=..0}] run function rpg:minion/ability_dispatch
""")
    dispatch = ["# 柱位与职责共同决定独立能力。"]
    for lord_index, lord in LORDS.items():
        for role_index, spirit in enumerate(lord["spirits"], 1):
            dispatch.append("execute if entity @s[scores={rpg_mn_lord=%d,rpg_mn_role=%d}] run return run function rpg:minion/ability/%s_%d" % (lord_index, role_index, lord["slug"], role_index))
            build_ability(lord_index, role_index, lord, ROLES[role_index], spirit)
    write("minion/ability_dispatch.mcfunction", "\n".join(dispatch))


def build_ability(lord_index, role_index, lord, role, spirit):
    lines = [
        "# %s · %s（%s）" % (spirit[1], role["name"], lord["lord"]),
        "scoreboard players set @s rpg_mn_cd %d" % role["cd"],
        transition(lord_index),
        "particle %s ~ ~1 ~ 0.45 0.65 0.45 0.025 10" % lord["particle"],
        "playsound %s hostile @a[distance=..20] ~ ~ ~ 0.35 1.12" % lord["sound"],
    ]
    if role_index == 1:
        buff = ("resistance", "absorption", "resistance", "absorption", "strength", "resistance", "absorption")[lord_index - 1]
        lines += [
            "effect give @e[tag=rpg.advent,scores={rpg_dm_lord=%d},distance=..12,limit=1] minecraft:%s 4 0 true" % (lord_index, buff),
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..8] minecraft:%s 4 0 true" % (lord_index, buff),
            "particle enchant ~ ~1 ~ 0.8 0.7 0.8 0.04 12",
        ]
    elif role_index == 2:
        effect = ("glowing", "slowness", "poison", "hunger", "glowing", "slowness", "weakness")[lord_index - 1]
        lines += [player_effect(effect, 4, 0, 10), "particle crit ~ ~1 ~ 0.8 0.6 0.8 0.05 12"]
    elif role_index == 3:
        secondary = ("resistance", "speed", "regeneration", "absorption", "strength", "resistance", "absorption")[lord_index - 1]
        lines += [
            "effect give @e[tag=rpg.advent,scores={rpg_dm_lord=%d},distance=..14,limit=1] minecraft:instant_health 1 0 true" % lord_index,
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..10] minecraft:regeneration 4 0 true" % lord_index,
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..10] minecraft:%s 4 0 true" % (lord_index, secondary),
            "particle heart ~ ~1.4 ~ 0.75 0.6 0.75 0.03 9",
        ]
    elif role_index == 4:
        effects = (("levitation", "weakness"), ("slowness", "mining_fatigue"), ("poison", "darkness"), ("hunger", "weakness"), ("nausea", "weakness"), ("slowness", "weakness"), ("mining_fatigue", "weakness"))[lord_index - 1]
        lines += [player_effect(effects[0], 3, 0, 8), player_effect(effects[1], 4, 0, 8), "particle reverse_portal ~ ~1 ~ 0.85 0.75 0.85 0.04 15"]
    else:
        damage = (5, 5, 6, 5, 7, 5, 6)[lord_index - 1]
        rider = ("weakness", "slowness", "poison", "hunger", "glowing", "mining_fatigue", "weakness")[lord_index - 1]
        lines += [
            "tag @s add rpg.demon.minion.caster",
            "execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s %d minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..8,limit=1]" % damage,
            player_effect(rider, 3, 0, 4),
            "tag @s remove rpg.demon.minion.caster",
            "particle sweep_attack ~ ~1 ~ 0.9 0.5 0.9 0.04 10",
        ]
    write("minion/ability/%s_%d.mcfunction" % (lord["slug"], role_index), "\n".join(lines))


def build_rewards():
    advancement = {
        "criteria": {"requirement": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": '{Tags:[\"rpg.demon.minion\"]}'}}]}}},
        "rewards": {"function": "rpg:minion/reward"},
    }
    write_json(ADV, "minion/kill.json", advancement)
    write("minion/reward.mcfunction", """advancement revoke @s only rpg:minion/kill
scoreboard players add @s rpg_ex_xp 1
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.22 1.55
""")
    for lord_index, lord in LORDS.items():
        for role_index, spirit in enumerate(lord["spirits"], 1):
            role = ROLES[role_index]
            table = {
                "type": "minecraft:entity",
                "pools": [
                    {"rolls": 1, "conditions": [{"condition": "minecraft:killed_by_player"}, {"condition": "minecraft:random_chance", "chance": 0.22}], "entries": [{"type": "minecraft:item", "name": lord["loot"]}]},
                    {"rolls": 1, "conditions": [{"condition": "minecraft:killed_by_player"}, {"condition": "minecraft:random_chance", "chance": 0.16}], "entries": [{"type": "minecraft:item", "name": role["material"]}]},
                ],
            }
            write_json(LOOT, "minion/%s/%s.json" % (lord["slug"], spirit[0]), table)


def main():
    reset_generated_trees()
    patch_scoreboard_and_hooks()
    build_summons()
    build_runtime_and_abilities()
    build_rewards()
    print("goetic legions: 35 persistent minions / 5 roles / phase-two rotation / manual summons")


if __name__ == "__main__":
    main()
