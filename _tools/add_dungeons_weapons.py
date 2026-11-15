# -*- coding: utf-8 -*-
"""《Minecraft Dungeons》原作武器：坟墓克星（Grave Bane）与竖琴弩（Harp Crossbow）。

两把都是 [传说]，也是圣殿大团长雅克手里的武器（Boss 那一侧另有会话负责，
这里只做玩家能拿到的物品）。

* 贴图：原作是像素贴图挤出厚度的网格，直接把贴图还原成物品贴图就贴原作。
  坟墓克星 34×34 去掉黑底和色板；竖琴弩 38×38 的四格各是一帧（见
  dungeons_weapons_ref/SOURCES.md），按原格 18×18 存，不缩放、不重画。
* 坟墓克星：下界合金剑，攻击距离更长，自带亡灵杀手 V。每第三下命中化作
  横扫，前方敌人受额外伤害、亡灵加倍；两下之间超过 2 秒重新计数，
  间隔太短（未蓄满的连点）不计。横扫用 rpg:grave_sweep 伤害类型，
  它在 #minecraft:bypasses_cooldown 里，第三下对主目标的加伤也落得满。
* 竖琴弩：弩，自带多重射击与快速装填 II。每次射击在多重射击的三支之外，
  再向两侧各补一支，一共五支（原作就是五支）。

获取：雅克的掉落表 rpg:dungeons_weapons/jacques（两把里随机一把，Boss 会话
接线），以及不祥宝库约 4% 一把；另有 give 与潜影盒。
"""
import io
import json
import os
import sys

import png_tool as P
import rpg_ui_style as ui

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "dungeons_weapons_ref")
RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
RPG_TEX = os.path.join(RP, "assets/rpg/textures/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
FUNC = os.path.join(DP, "data/rpg/function")
LOOT = os.path.join(DP, "data/rpg/loot_table")

GRAVE_CMD = 1110042
HARP_CMD = 1110043

COMBO_GAP = 40        # ticks: 两下之间超过这么久，连击重新计数
MIN_GAP = 12          # ticks: 比这更密的连点不算一下（攻速 1.2，蓄满约 17 刻）
SWEEP = 8             # 第三下横扫
SWEEP_UNDEAD = 14
SIDE_YAW = 22         # 竖琴弩补的两支偏出的角度（多重射击自己是 ±10°）
BOLT_SPEED = 3.15     # 与原版弩箭同速
VAULT_WEIGHT = 1      # 不祥宝库 3 抽、总权重七十多：每次开启约 4%

LEGEND = ui.tier_colour("legend")
GLINT = ui.dust_transition(ui.HOLY_LIGHT, ui.HOLY_DARK, 1.2)
GLINT_SMALL = ui.dust(ui.HOLY, 0.7)
LIVING = "type=!player,type=!#rpg:no_damage_track"

OBJECTIVES = [("rpg_gb_dmg", "minecraft.custom:minecraft.damage_dealt"),
              ("rpg_gb_combo", "dummy"), ("rpg_gb_last", "dummy"),
              ("rpg_gb_tmp", "dummy"), ("rpg_hc_tmp", "dummy")]


# ---------------------------------------------------------------------------
def write(path, text):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text.rstrip("\n") + "\n")


def wj(path, doc):
    write(path, json.dumps(doc, ensure_ascii=False, indent=2))


def wf(rel, text):
    write(os.path.join(FUNC, rel), text)


# ---------------------------------------------------------------------------
# 贴图
# ---------------------------------------------------------------------------
# 竖琴弩四帧在 38×38 里的位置（SM_HarpCrossbow1~4 的 UV 实测）：每格 19，
# 格内第 0 行是色板，武器像素在其下 18×18。四帧取同一个格内偏移，切换不跳像素。
HARP_FRAMES = {1: (0, 1), 2: (0, 20), 3: (19, 1), 4: (19, 20)}
HARP_SIZE = 18


def build_textures():
    w, h, rgba = P.read(os.path.join(REF, "T_Glaive_Unique1.png"))
    assert (w, h) == (34, 34)
    out = bytearray(rgba)
    for y in range(h):
        for x in range(w):
            i = (y * w + x) * 4
            # 黑底不在网格上；第 0 行左端是色板
            if rgba[i:i + 3] == b"\0\0\0" or (y == 0 and x < 9):
                out[i:i + 4] = b"\0\0\0\0"
    P.write(os.path.join(RPG_TEX, "grave_bane.png"), w, h, bytes(out))

    w, h, rgba = P.read(os.path.join(REF, "T_HarpCrossbow.png"))
    assert (w, h) == (38, 38)
    n = HARP_SIZE
    for k, (x0, y0) in HARP_FRAMES.items():
        frame = b"".join(rgba[((y0 + y) * w + x0) * 4:((y0 + y) * w + x0 + n) * 4]
                         for y in range(n))
        # 透明格清成全零，免得白底颜色留在透明像素里
        frame = b"".join(b"\0\0\0\0" if frame[i + 3] == 0 else frame[i:i + 4]
                         for i in range(0, len(frame), 4))
        P.write(os.path.join(RPG_TEX, "harp_crossbow_%d.png" % k), n, n, frame)


# ---------------------------------------------------------------------------
# 模型与物品定义
# ---------------------------------------------------------------------------
def model(ref):
    return {"type": "minecraft:model", "model": ref}


# 原版弩的状态 -> 帧：松弦、拉一半、拉满、上好箭
HARP_STATES = {"standby": 1, "pulling_0": 2, "pulling_1": 4, "pulling_2": 4, "arrow": 3}


def harp_variant():
    m = lambda s: model("rpg:item/harp_crossbow_" + s)
    return {
        "type": "minecraft:select",
        "property": "minecraft:charge_type",
        "cases": [{"when": "arrow", "model": m("arrow")},
                  {"when": "rocket", "model": m("arrow")}],
        "fallback": {
            "type": "minecraft:condition",
            "property": "minecraft:using_item",
            "on_false": m("standby"),
            "on_true": {
                "type": "minecraft:range_dispatch",
                "property": "minecraft:crossbow/pull",
                "fallback": m("pulling_0"),
                "entries": [{"threshold": 0.58, "model": m("pulling_1")},
                            {"threshold": 1.0, "model": m("pulling_2")}],
            },
        },
    }


def dispatch_entry(base, cmd, node_model):
    path = os.path.join(MC_ITEMS, base + ".json")
    if os.path.isfile(path):
        doc = json.load(io.open(path, encoding="utf-8"))
    else:
        import zipfile
        from mc_env import JAR
        with zipfile.ZipFile(JAR) as z:
            doc = json.loads(z.read("assets/minecraft/items/%s.json" % base).decode("utf-8"))
    node = doc["model"]
    if (node.get("type") or "").split(":")[-1] != "range_dispatch":
        node = {"type": "minecraft:range_dispatch",
                "property": "minecraft:custom_model_data",
                "fallback": node, "entries": []}
        doc["model"] = node
    entries = node.setdefault("entries", [])
    entries[:] = [e for e in entries if e["threshold"] != cmd]
    entries.append({"threshold": cmd, "model": node_model})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


def build_models():
    # 底材是重锤，手持照重锤上的其它长柄兵器（毒液长柄刀、狱卒镰刀）
    wj(os.path.join(RPG_MODELS, "grave_bane.json"),
       {"parent": "rpg:item/huge_sword_handheld", "textures": {"layer0": "rpg:item/grave_bane"}})
    for state, k in HARP_STATES.items():
        wj(os.path.join(RPG_MODELS, "harp_crossbow_%s.json" % state),
           {"parent": "item/crossbow", "textures": {"layer0": "rpg:item/harp_crossbow_%d" % k}})
    dispatch_entry("mace", GRAVE_CMD, model("rpg:item/grave_bane"))
    dispatch_entry("crossbow", HARP_CMD, harp_variant())


# ---------------------------------------------------------------------------
# 物品
# ---------------------------------------------------------------------------
def rule():
    return ui.row_value(ui.comp(ui.RULE_TEXT, ui.WHITE))


def line(*parts):
    """以「[」开头的片段用档次色加粗，其余白字。"""
    return ui.row_value(*[ui.comp(p, LEGEND, True) if p.startswith("[") else ui.comp(p, ui.WHITE)
                          for p in parts])


def muted(text):
    return ui.row_value(ui.comp(text, ui.MUTED))


def name(text):
    return ui.row_value(ui.comp(ui.tier_tag("legend"), LEGEND, True),
                        ui.comp(text, ui.WHITE, False))


GRAVE = dict(
    base="mace", key="grave_bane",
    comps={
        "custom_name": name("坟墓克星"),
        "lore": [
            rule(),
            line("来自黑暗年代的", "[遗物]"),
            line("刀上的魔力足以", "[驱散亡灵]"),
            rule(),
            ui.row_value(ui.comp("🗡被动技能", ui.WHITE), ui.comp("[三段连斩]", LEGEND, True)),
            line("每第三下化作横扫，前方敌人受%d点伤害" % SWEEP),
            line("亡灵受%d点；两下间隔超过%d秒重新计数" % (SWEEP_UNDEAD, COMBO_GAP // 20)),
            muted("原作：Minecraft Dungeons · Grave Bane"),
            rule(),
        ],
        "enchantments": {"minecraft:smite": 5, "minecraft:density": 3,
                         "minecraft:looting": 2, "minecraft:unbreaking": 3},
        "attribute_modifiers": [
            {"type": "minecraft:attack_damage", "amount": 9, "operation": "add_value",
             "slot": "mainhand", "id": "rpg:grave_bane/0"},
            {"type": "minecraft:attack_speed", "amount": -2.8, "operation": "add_value",
             "slot": "mainhand", "id": "rpg:grave_bane/1"},
            # 长柄：比剑远一格
            {"type": "minecraft:entity_interaction_range", "amount": 1, "operation": "add_value",
             "slot": "mainhand", "id": "rpg:grave_bane/2"}],
        "custom_model_data": {"floats": [float(GRAVE_CMD)]},
    },
    data="{grave_bane_tag:1b,sword_tag:1b}")

HARP = dict(
    base="crossbow", key="harp_crossbow",
    comps={
        "custom_name": name("竖琴弩"),
        "lore": [
            rule(),
            line("一半是", "[乐器]", "，一半是杀器"),
            line("有它在，派对才算", "[开场]"),
            rule(),
            ui.row_value(ui.comp("🏹被动技能", ui.WHITE), ui.comp("[齐奏]", LEGEND, True)),
            line("每次射出五支箭：多重射击之外"),
            line("再向两侧各补一支，扇面更宽"),
            muted("原作：Minecraft Dungeons · Harp Crossbow"),
            rule(),
        ],
        "enchantments": {"minecraft:multishot": 1, "minecraft:quick_charge": 2,
                         "minecraft:unbreaking": 3},
        "custom_model_data": {"floats": [float(HARP_CMD)]},
    },
    # 不带 bow_tag：那会让五支箭都翻倍提速并在落点爆炸
    data="{harp_crossbow_tag:1b}")

ITEMS = [GRAVE, HARP]


def snbt(value):
    # JSON 是 SNBT 的子集（带引号的键、true/false、数字），组件值直接写 JSON
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def give_line(it, target="@a"):
    body = ",".join("%s=%s" % (k, snbt(v)) for k, v in it["comps"].items())
    return "give %s %s[%s,custom_data=%s]" % (target, it["base"], body, it["data"])


def loot_entry(it):
    return {"type": "minecraft:item", "name": "minecraft:" + it["base"],
            "functions": [
                {"function": "minecraft:set_components",
                 "components": {"minecraft:" + k: v for k, v in it["comps"].items()}},
                {"function": "minecraft:set_custom_data", "tag": it["data"]}]}


def build_give():
    path = os.path.join(FUNC, "command/give/weapon.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    appended = "坟墓克星" not in s
    if appended:
        write(path, s.rstrip("\n") + "\n\n# Minecraft Dungeons 原作武器（add_dungeons_weapons.py）\n"
              + "\n".join(give_line(it) for it in ITEMS))
    wf("command/give/dungeons.mcfunction", "\n".join(
        ["# 坟墓克星与竖琴弩，发给执行者自己（由 add_dungeons_weapons.py 生成）",
         "# 组件与 give/weapon 逐字相同，潜影盒按组件去重只收一份"]
        + [give_line(it, "@s") for it in ITEMS]))
    return appended


# ---------------------------------------------------------------------------
# 坟墓克星［三段连斩］
# ---------------------------------------------------------------------------
GRAVE_GUARD = """\
# 坟墓克星：这一刻有人打出了近战伤害才往下走。
execute if entity @a[scores={{rpg_gb_dmg=1..}},limit=1] run function rpg:item/extra/grave_bane
"""

GRAVE_TICK = """\
# 坟墓克星［三段连斩］的每刻结算。由 rpg:item/extra/skills 守卫调用。
execute as @a[scores={{rpg_gb_dmg=1..}}] if items entity @s weapon.mainhand *[minecraft:custom_data~{{grave_bane_tag:1b}}] at @s run function rpg:item/extra/grave_bane_hit
scoreboard players reset * rpg_gb_dmg
"""

GRAVE_HIT = """\
# 握着坟墓克星打中了一下。连击按 gametime 量间隔，不依赖每刻倒数。
execute store result score #now rpg_gb_tmp run time query gametime
scoreboard players operation #gap rpg_gb_tmp = #now rpg_gb_tmp
scoreboard players operation #gap rpg_gb_tmp -= @s rpg_gb_last
# 没蓄满的连点不算一下
execute if score @s rpg_gb_combo matches 1.. if score #gap rpg_gb_tmp matches ..{MIN_GAP_1} run return 0
execute if score #gap rpg_gb_tmp matches {GAP_1}.. run scoreboard players set @s rpg_gb_combo 0
scoreboard players operation @s rpg_gb_last = #now rpg_gb_tmp
scoreboard players add @s rpg_gb_combo 1
execute if score @s rpg_gb_combo matches ..2 anchored eyes positioned ^ ^-0.4 ^1.6 run particle {GLINT_SMALL} ~ ~ ~ 0.3 0.2 0.3 0 4
execute if score @s rpg_gb_combo matches 3.. run function rpg:item/extra/grave_bane_sweep
execute if score @s rpg_gb_combo matches 3.. run scoreboard players set @s rpg_gb_combo 0
"""

GRAVE_SWEEP = """\
# 第三下：前方横扫。施放者带 rpg.gb.cast，伤害记在他名下。
tag @s add rpg.gb.cast
playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.7
playsound minecraft:block.bell.use player @a[distance=..16] ~ ~ ~ 0.5 1.7
execute anchored eyes positioned ^ ^-0.5 ^ run particle minecraft:sweep_attack ^-1 ^ ^1.6 0 0 0 0 1
execute anchored eyes positioned ^ ^-0.5 ^ run particle minecraft:sweep_attack ^ ^ ^2 0 0 0 0 1
execute anchored eyes positioned ^ ^-0.5 ^ run particle minecraft:sweep_attack ^1 ^ ^1.6 0 0 0 0 1
execute anchored eyes positioned ^ ^-0.5 ^ run particle {GLINT} ^ ^ ^1.8 1.2 0.15 1.2 0 14
execute positioned ^ ^ ^1.8 as @e[distance=..2.8,{LIVING}] at @s run function rpg:item/extra/grave_bane_sweep_hit
tag @s remove rpg.gb.cast
"""

GRAVE_SWEEP_HIT = """\
# 被横扫扫到的一个。亡灵受伤加倍左右。
particle {GLINT_SMALL} ~ ~1 ~ 0.25 0.35 0.25 0 5
execute if entity @s[type=#minecraft:undead] run return run damage @s {SWEEP_UNDEAD} rpg:grave_sweep by @a[tag=rpg.gb.cast,limit=1]
damage @s {SWEEP} rpg:grave_sweep by @a[tag=rpg.gb.cast,limit=1]
"""

# ---------------------------------------------------------------------------
# 竖琴弩［齐奏］
# ---------------------------------------------------------------------------
HARP_SHOT = """\
# 竖琴弩［齐奏］—— 由 rpg:advancement/item/harp_crossbow 在射击时触发。
# 多重射击已经射出三支（±10°），这里再向两侧各补一支。
advancement revoke @s only rpg:item/harp_crossbow
tag @s add rpg.hc.cast
execute anchored eyes positioned ^ ^ ^ rotated ~-{SIDE_YAW} ~ run function rpg:item/extra/harp_crossbow_bolt
execute anchored eyes positioned ^ ^ ^ rotated ~{SIDE_YAW} ~ run function rpg:item/extra/harp_crossbow_bolt
playsound minecraft:block.note_block.harp player @a[distance=..16] ~ ~ ~ 0.8 1.4
execute anchored eyes positioned ^ ^ ^1 run particle minecraft:note ~ ~0.2 ~ 0.4 0.2 0.4 1 3
tag @s remove rpg.hc.cast
"""

HARP_BOLT = """\
# 沿当前朝向补一支弩箭。方向取两个临时标记的坐标差，不用三角函数。
summon minecraft:marker ^ ^ ^ {{Tags:["rpg.hc.o"]}}
summon minecraft:marker ^ ^ ^1 {{Tags:["rpg.hc.d"]}}
summon minecraft:arrow ^ ^ ^0.6 {{Tags:["rpg.hc.bolt","rpg.hc.new"],pickup:2b,crit:1b}}
execute store result score #ox rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.o,limit=1] Pos[0] 1000
execute store result score #oy rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.o,limit=1] Pos[1] 1000
execute store result score #oz rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.o,limit=1] Pos[2] 1000
execute store result score #dx rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.d,limit=1] Pos[0] 1000
execute store result score #dy rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.d,limit=1] Pos[1] 1000
execute store result score #dz rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.d,limit=1] Pos[2] 1000
scoreboard players operation #dx rpg_hc_tmp -= #ox rpg_hc_tmp
scoreboard players operation #dy rpg_hc_tmp -= #oy rpg_hc_tmp
scoreboard players operation #dz rpg_hc_tmp -= #oz rpg_hc_tmp
execute as @e[type=arrow,tag=rpg.hc.new,limit=1] run function rpg:item/extra/harp_crossbow_aim
kill @e[type=marker,tag=rpg.hc.o]
kill @e[type=marker,tag=rpg.hc.d]
"""

HARP_AIM = """\
# 新补的这支箭：速度与原版弩箭相同，归属记在射手名下（击杀、掉落都算他的）
execute store result entity @s Motion[0] double {SCALE} run scoreboard players get #dx rpg_hc_tmp
execute store result entity @s Motion[1] double {SCALE} run scoreboard players get #dy rpg_hc_tmp
execute store result entity @s Motion[2] double {SCALE} run scoreboard players get #dz rpg_hc_tmp
data modify entity @s Owner set from entity @a[tag=rpg.hc.cast,limit=1] UUID
tag @s remove rpg.hc.new
"""

ARGS = dict(MIN_GAP_1=MIN_GAP - 1, GAP_1=COMBO_GAP + 1, GLINT=GLINT, GLINT_SMALL=GLINT_SMALL,
            LIVING=LIVING, SWEEP=SWEEP, SWEEP_UNDEAD=SWEEP_UNDEAD, SIDE_YAW=SIDE_YAW,
            SCALE="%.6f" % (BOLT_SPEED / 1000.0))


def build_functions():
    wf("item/extra/grave_bane_guard.mcfunction", GRAVE_GUARD.format(**ARGS))
    wf("item/extra/grave_bane.mcfunction", GRAVE_TICK.format(**ARGS))
    wf("item/extra/grave_bane_hit.mcfunction", GRAVE_HIT.format(**ARGS))
    wf("item/extra/grave_bane_sweep.mcfunction", GRAVE_SWEEP.format(**ARGS))
    wf("item/extra/grave_bane_sweep_hit.mcfunction", GRAVE_SWEEP_HIT.format(**ARGS))
    wf("item/extra/harp_crossbow_shot.mcfunction", HARP_SHOT.format(**ARGS))
    wf("item/extra/harp_crossbow_bolt.mcfunction", HARP_BOLT.format(**ARGS))
    wf("item/extra/harp_crossbow_aim.mcfunction", HARP_AIM.format(**ARGS))

    path = os.path.join(FUNC, "item/extra/skills.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "item/extra/grave_bane_guard" not in s:
        write(path, s.rstrip("\n") + "\nfunction rpg:item/extra/grave_bane_guard")

    adv = os.path.join(DP, "data/rpg/advancement/item/harp_crossbow.json")
    wj(adv, {
        "criteria": {"requirement": {
            "trigger": "minecraft:shot_crossbow",
            "conditions": {"item": {
                "items": "minecraft:crossbow",
                "predicates": {"minecraft:custom_data": "{harp_crossbow_tag:1b}"}}}}},
        "rewards": {"function": "rpg:item/extra/harp_crossbow_shot"},
    })

    # 横扫的伤害类型：记作玩家攻击，绕过受击冷却
    wj(os.path.join(DP, "data/rpg/damage_type/grave_sweep.json"),
       {"message_id": "player", "scaling": "when_caused_by_living_non_player",
        "exhaustion": 0.1})
    tag = os.path.join(DP, "data/minecraft/tags/damage_type/bypasses_cooldown.json")
    doc = json.load(io.open(tag, encoding="utf-8")) if os.path.isfile(tag) else \
        {"replace": False, "values": []}
    if "rpg:grave_sweep" not in doc["values"]:
        doc["values"].append("rpg:grave_sweep")
        wj(tag, doc)


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    block = ["scoreboard objectives add %s %s" % (o, c) for o, c in OBJECTIVES
             if ("scoreboard objectives add %s " % o) not in s]
    if block:
        write(path, s.rstrip("\n") + "\n\n##Dungeons 原作武器\n" + "\n".join(block))
    return block


# ---------------------------------------------------------------------------
# 获取
# ---------------------------------------------------------------------------
def build_loot():
    table = "rpg:dungeons_weapons/jacques"
    wj(os.path.join(LOOT, "dungeons_weapons/jacques.json"),
       {"pools": [{"rolls": 1, "entries": [loot_entry(it) for it in ITEMS]}]})
    path = os.path.join(LOOT, "trial/trial_ominous.json")
    doc = json.load(io.open(path, encoding="utf-8"))
    entries = doc["pools"][0]["entries"]
    if not any(e.get("value") == table for e in entries):
        entries.append({"type": "minecraft:loot_table", "value": table, "weight": VAULT_WEIGHT})
        wj(path, doc)
        return True
    return False


if __name__ == "__main__":
    build_textures()
    build_models()
    if os.path.isdir(FUNC):
        print("dungeons weapons: give appended: %s" % build_give())
        build_functions()
        print("dungeons weapons: objectives added: %s"
              % (", ".join(b.split()[3] for b in add_objectives()) or "(already present)"))
        print("dungeons weapons: ominous vault entry added: %s" % build_loot())
