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

# Each spirit owns a named combat language.  The five tuple positions are the
# stable roles above; effects are interpreted by the role-specific executor in
# build_ability().  This keeps the ecology readable without creating 35 hot
# loops or relying on vanilla illager spell AI.
SKILLS = {
    1: [
        ("王冠护持", "傲慢为同柱披上王权", "resistance", "glowing", 0),
        ("罪痕标定", "锁定最近的见证者并令其失重", "levitation", "glowing", 2),
        ("晨星赐福", "以虚假的冠冕修复同柱", "resistance", "absorption", 0),
        ("失坠敕令", "压低周围凡人的力量与动作", "weakness", "mining_fatigue", 1),
        ("王座裁落", "在近身处落下傲慢的裁决", "levitation", "weakness", 7),
    ],
    2: [
        ("妒潮护幕", "嫉妒复制最坚固的鳞片", "absorption", "resistance", 0),
        ("寒潮猎印", "暗潮缠住最近的脚步", "slowness", "weakness", 2),
        ("回潮再生", "偷取生命的形状赐予同柱", "regeneration", "speed", 0),
        ("海渊重压", "倒影令众人迟滞而失明", "slowness", "darkness", 1),
        ("沉锚碾落", "深海之口咬住近身猎物", "slowness", "weakness", 7),
    ],
    3: [
        ("死寂护幕", "死亡为同柱封上一层墓石", "resistance", "absorption", 0),
        ("疫矢猎印", "骨哨令最近的活物腐败", "poison", "glowing", 3),
        ("灵魂归仓", "葬歌将残躯重新缝合", "regeneration", "resistance", 0),
        ("深渊低语", "坟土吞没声音与视野", "darkness", "slowness", 2),
        ("刈魂", "丧钟为近身者预告终点", "wither", "slowness", 8),
    ],
    4: [
        ("腐宴护壳", "饕宴残渣凝成带刺甲壳", "absorption", "resistance", 0),
        ("饥印", "腐蝇锁定最近且最鲜活的胃", "hunger", "glowing", 2),
        ("吞食反哺", "以腐宴喂养受伤的同柱", "regeneration", "absorption", 0),
        ("蝇幕蚀志", "腐败气息令众人饥饿作呕", "hunger", "nausea", 2),
        ("饥啮", "饥饿在近身处同时张口", "hunger", "weakness", 7),
    ],
    5: [
        ("怒血共鸣", "暴怒将伤口锻成力量", "strength", "resistance", 0),
        ("血猎标记", "猎手沿血光咬住最近目标", "glowing", "weakness", 3),
        ("狂血灌注", "战吼迫使同柱继续厮杀", "regeneration", "strength", 0),
        ("死亡低语", "怒火扰乱周围的判断", "nausea", "weakness", 2),
        ("怒斩", "最短的距离只容得下一次斩击", "weakness", "glowing", 9),
    ],
    6: [
        ("紫宴护幕", "静止本身成为同柱的护甲", "resistance", "absorption", 0),
        ("魅视缚足", "睡意攀上最近目标的四肢", "slowness", "mining_fatigue", 2),
        ("献身回流", "不愿行动的躯体拒绝死亡", "regeneration", "resistance", 0),
        ("感官倒悬", "沉重梦境封住周围的动作", "slowness", "darkness", 1),
        ("强制朝拜", "越想挣扎，镰刃便越沉重", "mining_fatigue", "weakness", 7),
    ],
    7: [
        ("金契护体", "财富替同柱承受第一道伤口", "absorption", "resistance", 0),
        ("债印", "金光记下最近目标的欠款", "glowing", "weakness", 2),
        ("复利回偿", "未来的代价修补现在的身体", "regeneration", "absorption", 0),
        ("重税", "无形债契拖慢所有偿还者", "mining_fatigue", "weakness", 1),
        ("一次结清", "金色刃口收走近身者的抵押", "weakness", "slowness", 8),
    ],
}

ROLE_SOUNDS = {
    1: "minecraft:item.shield.block",
    2: "minecraft:item.crossbow.shoot",
    3: "minecraft:block.enchantment_table.use",
    4: "minecraft:entity.evoker.cast_spell",
    5: "minecraft:entity.player.attack.strong",
}

OBJECTIVES = ("rpg_mn_lord", "rpg_mn_role", "rpg_mn_cd", "rpg_mn_tick", "rpg_mn_slot",
              "rpg_mn_owner", "rpg_mn_cast")


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
        "# 二阶段每次压力轮换一个职责；以 rpg_rite_id 精确隔离同法阵存活者。",
        "scoreboard players add @s rpg_mn_slot 1",
        "execute if score @s rpg_mn_slot matches 6.. run scoreboard players set @s rpg_mn_slot 1",
        "tag @e[tag=rpg.demon.minion] remove rpg.demon.minion.owned",
        "tag @s add rpg.rite.anchor.current",
        "execute as @e[tag=rpg.demon.minion] if score @s rpg_mn_owner = @e[type=minecraft:item_display,tag=rpg.rite.anchor.current,limit=1] rpg_rite_id run tag @s add rpg.demon.minion.owned",
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
                "scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0",
                "execute if entity @s[type=minecraft:item_display,tag=rpg.rite.anchor] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner = @s rpg_rite_id",
                "execute if entity @s[type=minecraft:item_display,tag=rpg.ch1.rite] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_ch1_id = @s rpg_ch1_id",
                "execute if entity @s[type=minecraft:item_display,tag=rpg.ch1.rite] run tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] add rpg.ch1.minion",
                # Deterministic first-cast staggering prevents seven cohorts
                # summoned together from producing a single particle/sound spike.
                "scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd %d" % (role["cd"] // 2 + (lord_index - 1) * 7 + role_index * 3),
                "scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0",
                "tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new",
                "particle %s ~ ~1 ~ 0.55 0.75 0.55 0.035 18" % lord["particle"],
                "particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10",
                "playsound %s hostile @a[distance=..28] ~ ~ ~ 0.55 0.9" % lord["sound"],
                tellraw_summon(lord, role, spirit),
            ]
            write(rel, "\n".join(lines))
            all_lines.append("function rpg:minion/summon/%s/%s" % (lord["slug"], spirit[0]))
            phase.append(
                "execute if score @s rpg_dm_lord matches %d if score @s rpg_mn_slot matches %d unless entity @e[tag=rpg.demon.minion,tag=rpg.demon.minion.owned,scores={rpg_mn_lord=%d,rpg_mn_role=%d},limit=1] run function rpg:minion/summon/%s/%s"
                % (lord_index, role_index, lord_index, role_index, lord["slug"], spirit[0])
            )
        write("minion/summon/%s/all.mcfunction" % lord["slug"], "\n".join(all_lines))
    phase += [
        "tag @s remove rpg.rite.anchor.current",
        "tag @e[tag=rpg.demon.minion.owned] remove rpg.demon.minion.owned",
    ]
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


def target_effect(effect, seconds, amplifier, radius):
    return "effect give @a[distance=..%d,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:%s %d %d true" % (radius, effect, seconds, amplifier)


def cast_notice(lord, role_index, role, spirit, skill, cue):
    component = [
        "",
        {"text": "[罪仆术式] ", "color": lord["base"], "bold": True, "italic": False},
        {"text": spirit[1] + " · ", "color": lord["light"], "bold": False, "italic": False},
        {"text": skill, "color": lord["light"], "bold": True, "italic": False},
        {"text": "｜" + role["name"], "color": "gray", "bold": False, "italic": False},
        {"text": "　" + cue, "color": "dark_gray", "bold": False, "italic": False},
    ]
    radius = {1: 12, 2: 10, 3: 14, 4: 8, 5: 4}[role_index]
    return "tellraw @a[distance=..%d,gamemode=!spectator] " % radius + json.dumps(component, ensure_ascii=False, separators=(",", ":"))


def ring(particle, radius):
    points = ((radius, 0), (-radius, 0), (0, radius), (0, -radius),
              (radius * 0.7, radius * 0.7), (-radius * 0.7, radius * 0.7),
              (radius * 0.7, -radius * 0.7), (-radius * 0.7, -radius * 0.7))
    return ["particle %s ~%g ~0.18 ~%g 0 0 0 0 1" % (particle, x, z) for x, z in points]


def telegraph_geometry(lord_index, role_index, lord):
    lines = [transition(lord_index, 4)]
    if role_index == 1:
        lines.append("particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8")
    elif role_index == 2:
        lines.append("execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8")
        lines.append(target_effect("glowing", 1, 0, 10))
    elif role_index == 3:
        target = "@e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=0.1..10,sort=nearest,limit=1]" % lord_index
        for step in (1, 2, 3, 4):
            lines.append("execute facing entity %s eyes run particle end_rod ^ ^1 ^%d 0.05 0.05 0.05 0.01 2" % (target, step))
    elif role_index == 4:
        lines += ring(lord["particle"], 8)
    else:
        lines += ring("crit", 4)
    return lines


def build_runtime_and_abilities():
    write("minion/tick.mcfunction", """# 35 种罪仆共用十刻节拍，场上无罪仆时不会进入本系统。
scoreboard players add #clock rpg_mn_tick 1
execute if score #clock rpg_mn_tick matches 10.. run function rpg:minion/beat
""")
    write("minion/beat.mcfunction", """scoreboard players set #clock rpg_mn_tick 0
scoreboard players set #casts rpg_mn_tick 0
execute as @e[tag=rpg.demon.minion] at @s run function rpg:minion/entity_tick
""")
    write("minion/entity_tick.mcfunction", """execute if entity @s[tag=rpg.demon.minion.casting,scores={rpg_mn_cast=1..}] run scoreboard players remove @s rpg_mn_cast 10
execute if entity @s[tag=rpg.demon.minion.casting,scores={rpg_mn_cast=..0}] run return run function rpg:minion/resolve_dispatch
execute if entity @s[tag=rpg.demon.minion.casting] run return 0
execute if entity @s[scores={rpg_mn_cd=1..}] run scoreboard players remove @s rpg_mn_cd 10
execute if entity @s[scores={rpg_mn_role=3}] unless entity @a[distance=..14,gamemode=!spectator,gamemode=!creative,limit=1] run return 0
execute unless entity @s[scores={rpg_mn_role=3}] unless entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run return 0
execute if score #casts rpg_mn_tick matches ..1 if entity @s[scores={rpg_mn_cd=..0}] run function rpg:minion/ability_dispatch
""")
    dispatch = ["# 柱位与职责共同决定独立能力。"]
    resolve = ["# 蓄势结束后按柱位与职责结算；随后清除施法态。"]
    for lord_index, lord in LORDS.items():
        for role_index, spirit in enumerate(lord["spirits"], 1):
            dispatch.append("execute if entity @s[scores={rpg_mn_lord=%d,rpg_mn_role=%d}] run return run function rpg:minion/ability/%s_%d" % (lord_index, role_index, lord["slug"], role_index))
            resolve.append("execute if entity @s[scores={rpg_mn_lord=%d,rpg_mn_role=%d}] run return run function rpg:minion/ability/resolve/%s_%d" % (lord_index, role_index, lord["slug"], role_index))
            build_ability(lord_index, role_index, lord, ROLES[role_index], spirit)
    write("minion/ability_dispatch.mcfunction", "\n".join(dispatch))
    write("minion/resolve_dispatch.mcfunction", "\n".join(resolve))


def build_ability(lord_index, role_index, lord, role, spirit):
    skill, cue, primary, secondary, damage = SKILLS[lord_index][role_index - 1]
    cooldown = role["cd"] + (lord_index - 1) * 4
    windup = 10 if role_index in (1, 5) else 20
    lines = [
        "# %s · %s（%s）：%s" % (spirit[1], role["name"], lord["lord"], skill),
        "scoreboard players add #casts rpg_mn_tick 1",
        "scoreboard players set @s rpg_mn_cd %d" % cooldown,
        "scoreboard players set @s rpg_mn_cast %d" % windup,
        "tag @s add rpg.demon.minion.casting",
        cast_notice(lord, role_index, role, spirit, skill, cue),
        "playsound %s hostile @a[distance=..20] ~ ~ ~ 0.35 1.12" % lord["sound"],
        "playsound %s hostile @a[distance=..14] ~ ~ ~ 0.28 0.92" % ROLE_SOUNDS[role_index],
    ] + telegraph_geometry(lord_index, role_index, lord)
    resolve = [
        "# %s：延迟结算；单次总粒子预算不超过 28。" % skill,
        "tag @s remove rpg.demon.minion.casting",
        "scoreboard players set @s rpg_mn_cast 0",
        "particle %s ~ ~1 ~ 0.38 0.55 0.38 0.025 2" % lord["particle"],
        "playsound %s hostile @a[distance=..14] ~ ~ ~ 0.32 1.05" % ROLE_SOUNDS[role_index],
    ]
    if role_index == 1:
        resolve += [
            "effect give @e[tag=rpg.advent,scores={rpg_dm_lord=%d},distance=..12,limit=1] minecraft:%s 4 0 true" % (lord_index, primary),
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..8] minecraft:%s 4 0 true" % (lord_index, primary),
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..8] minecraft:%s 3 0 true" % (lord_index, secondary),
            "particle enchant ~ ~1 ~ 0.8 0.7 0.8 0.04 10",
        ]
    elif role_index == 2:
        resolve += [
            "tag @s add rpg.demon.minion.caster",
            target_effect(primary, 4, 0, 10), target_effect(secondary, 3, 0, 10),
            "execute as @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run damage @s %d minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..12,sort=nearest,limit=1]" % damage,
            "execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.35 0.55 0.35 0.05 10",
            "tag @s remove rpg.demon.minion.caster",
        ]
    elif role_index == 3:
        resolve += [
            "effect give @e[tag=rpg.advent,scores={rpg_dm_lord=%d},distance=..14,limit=1] minecraft:instant_health 1 0 true" % lord_index,
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..10] minecraft:regeneration 4 0 true" % lord_index,
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..10] minecraft:%s 4 0 true" % (lord_index, primary),
            "effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=%d},distance=..10] minecraft:%s 3 0 true" % (lord_index, secondary),
            "particle heart ~ ~1.4 ~ 0.75 0.6 0.75 0.03 10",
        ]
    elif role_index == 4:
        resolve += [
            "tag @s add rpg.demon.minion.caster",
            player_effect(primary, 3, 0, 8), player_effect(secondary, 4, 0, 8),
            "execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run damage @s %d minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..10,sort=nearest,limit=1]" % damage,
            "tag @s remove rpg.demon.minion.caster",
            "particle reverse_portal ~ ~1 ~ 0.85 0.75 0.85 0.04 10",
        ]
    else:
        resolve += [
            "tag @s add rpg.demon.minion.caster",
            "execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s %d minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..8,limit=1]" % damage,
            player_effect(primary, 3, 0, 4), player_effect(secondary, 3, 0, 4),
            "effect give @s minecraft:regeneration 3 0 true",
            "tag @s remove rpg.demon.minion.caster",
            "particle sweep_attack ~ ~1 ~ 0.9 0.5 0.9 0.04 10",
        ]
    write("minion/ability/%s_%d.mcfunction" % (lord["slug"], role_index), "\n".join(lines))
    write("minion/ability/resolve/%s_%d.mcfunction" % (lord["slug"], role_index), "\n".join(resolve))


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
