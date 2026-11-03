# -*- coding: utf-8 -*-
"""米迦勒脊骨 / 米迦勒肋骨 -- the archangel's two relics, a paired [神圣] set.

第一次神陨之战，米迦勒呼喊"谁似神"（Mi-ka-El 的本义）击败路西法。
脊骨与肋骨是他留在人间的圣骸，两件都算圣器（holy_weapon_tag）。

  米迦勒脊骨  netherite_spear  active  -- 谁似神: hold the spear's own charge
                                         for a second and bone spikes break the
                                         ground for 10 blocks ahead
  米迦勒肋骨  netherite_sword  passive -- 圣焰: hits stack holy fire on the
                                         target; the third stack kindles it
  dual wield                   synergy -- 骨中之骨 (Gen 2:23): spine in one hand,
                                         rib in the other -- the spikes reach 16
                                         blocks and lay a stack each, the fire
                                         kindles on the second stack, and burns
                                         路西法 twice as hard

The split mirrors 雅斤 / 波阿斯: only the spine has a use action.  The rib is a
plain sword, so with the rib in the main hand right-click falls through to the
spear in the off hand and its charge still fires the skill.

Two timing details shape the code:

* `using_item` repeats every tick while the charge is held.  Charge and
  cooldown are both measured against `time query gametime`, so neither needs a
  per-tick countdown that would freeze while nobody holds the weapon.
* A kindled target has just been struck, and `damage` inside the victim's
  invulnerability window only lands the excess.  So kindling lights an 11-tick
  fuse first; the burst lands once the window has closed.
"""

import io
import json
import os
import shutil
import sys

import png_tool as P
import rpg_ui_style as ui
import rpg_vfx as vfx

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
RPG_TEX = os.path.join(RP, "assets/rpg/textures/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")

# 用户提供的原画：1024 px，正好是 32 网格的 32 倍放大，已无损还原成 32×32
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "michael_art")

SPINE_CMD = 1110040
RIB_CMD = 1110041

CHARGE = 20          # ticks of held charge before the spikes break ground
COOLDOWN = 160       # ticks
REACH = 10           # blocks of spikes
PAIR_REACH = 16      # with 骨中之骨
FUSE = 11            # ticks: outlasts the victim's invulnerability window
EMBER = 100          # ticks an unkindled stack lasts

MAINHAND = ["michael_spine_tag", "michael_rib_tag"]
OFFHAND = ["michael_spine_tag", "michael_rib_tag"]
OBJECTIVES = [("rpg_mi_dmg", "minecraft.custom:minecraft.damage_dealt"),
              ("rpg_mi_flame", "dummy"), ("rpg_mi_ttl", "dummy"),
              ("rpg_mi_fuse", "dummy"), ("rpg_mi_hold", "dummy"),
              ("rpg_mi_last", "dummy"), ("rpg_mi_cd", "dummy"),
              ("rpg_mi_tmp", "dummy")]

HOLY = ui.tier_colour("holy")             # 受难红 #FF3300
EMBER_DARK = ui.shade(ui.PASSION, 0.7)    # 受难红沉向黑，贴近刻印渐变的暗端
FIRE = ui.dust_transition(ui.PASSION, EMBER_DARK, 1.4)
FIRE_BIG = ui.dust_transition(ui.PASSION, EMBER_DARK, 1.6)
FIRE_SMALL = ui.dust(ui.PASSION, 0.8)
BONE = 'block{block_state:{Name:"minecraft:bone_block"}}'
FLASH = vfx.flash(ui.PASSION)
# 恶魔：七魔王与无名者带 rpg.demon，罪仆只带 rpg.demon.minion
LIVING = "type=!player,type=!#rpg:no_damage_track"


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def wf(rel, text):
    path = os.path.join(FUNC, rel)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


# ---------------------------------------------------------------------------
# resource pack
# ---------------------------------------------------------------------------
def mirror(w, h, rgba):
    out = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            s = (y * w + x) * 4
            d = (y * w + (w - 1 - x)) * 4
            out[d:d + 4] = rgba[s:s + 4]
    return bytes(out)


def build_textures():
    # 用户原画原样使用，不描边（试过描边，用户选回原图）
    if not os.path.isdir(RPG_TEX):
        os.makedirs(RPG_TEX)
    for name in ("michael_spine", "michael_rib"):
        src = os.path.join(ART, name + ".png")
        w, h, rgba = P.read(src)
        assert (w, h) == (32, 32), "%s 不是 32 网格" % name
        # 物品栏图标：只保留有像素的部分，透明边直接裁掉，不缩放（用户要求）。
        # 于是画布是包围盒的尺寸（27×27、26×23），客户端把它撑满物品格 ——
        # 这是 ART-STYLE §4「16/32 网格、主体 80%–94%」的登记例外
        x0, y0, x1, y1 = P.bbox(w, h, rgba)
        cw, ch = x1 - x0 + 1, y1 - y0 + 1
        crop = b"".join(rgba[((y0 + y) * w + x0) * 4:((y0 + y) * w + x1 + 1) * 4]
                        for y in range(ch))
        P.write(os.path.join(RPG_TEX, name + "_icon.png"), cw, ch, crop)
        # 手持：原图原尺寸，手里的大小不变
        if name == "michael_spine":
            # 长枪的手持模型沿用原版 spear_in_hand，它要的是左右镜像过的贴图；
            # 不镜像的那张没有模型引用，旧构建留下的就删掉
            P.write(os.path.join(RPG_TEX, name + "_in_hand.png"), w, h,
                    mirror(w, h, rgba))
            stale = os.path.join(RPG_TEX, name + ".png")
            if os.path.isfile(stale):
                os.remove(stale)
        else:
            shutil.copyfile(src, os.path.join(RPG_TEX, name + ".png"))


def dispatch_entry(path, base, cmd, model):
    if os.path.isfile(path):
        doc = json.load(io.open(path, encoding="utf-8"))
    else:
        import zipfile
        from mc_env import JAR
        with zipfile.ZipFile(JAR) as z:
            doc = json.loads(
                z.read("assets/minecraft/items/%s.json" % base).decode("utf-8"))
    node = doc["model"]
    if (node.get("type") or "").split(":")[-1] != "range_dispatch":
        node = {"type": "minecraft:range_dispatch",
                "property": "minecraft:custom_model_data",
                "fallback": node, "entries": []}
        doc["model"] = node
    entries = node.setdefault("entries", [])
    entries[:] = [e for e in entries if e["threshold"] != cmd]
    entries.append({"threshold": cmd, "model": model})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


def build_models():
    wj(os.path.join(RPG_MODELS, "michael_spine.json"),
       {"parent": "item/generated",
        "textures": {"layer0": "rpg:item/michael_spine_icon"}})
    wj(os.path.join(RPG_MODELS, "michael_rib_icon.json"),
       {"parent": "item/generated",
        "textures": {"layer0": "rpg:item/michael_rib_icon"}})
    wj(os.path.join(RPG_MODELS, "michael_spine_in_hand.json"),
       {"parent": "minecraft:item/spear_in_hand",
        "textures": {"layer0": "rpg:item/michael_spine_in_hand"}})
    # 肋骨挂雅斤／波阿斯的双持手持变换：副手是正手，不是反握
    wj(os.path.join(RPG_MODELS, "michael_rib.json"),
       {"parent": "rpg:item/twin_handheld",
        "textures": {"layer0": "rpg:item/michael_rib"}})

    dispatch_entry(os.path.join(MC_ITEMS, "netherite_spear.json"),
                   "netherite_spear", SPINE_CMD,
                   {"type": "minecraft:select",
                    "property": "minecraft:display_context",
                    "cases": [{"when": ["gui", "ground", "fixed", "on_shelf"],
                               "model": {"type": "minecraft:model",
                                         "model": "rpg:item/michael_spine"}}],
                    "fallback": {"type": "minecraft:model",
                                 "model": "rpg:item/michael_spine_in_hand"}})
    # 肋骨同样分两套：物品栏里是铺满的图标，手里是原尺寸
    dispatch_entry(os.path.join(MC_ITEMS, "netherite_sword.json"),
                   "netherite_sword", RIB_CMD,
                   {"type": "minecraft:select",
                    "property": "minecraft:display_context",
                    "cases": [{"when": ["gui", "ground", "fixed", "on_shelf"],
                               "model": {"type": "minecraft:model",
                                         "model": "rpg:item/michael_rib_icon"}}],
                    "fallback": {"type": "minecraft:model",
                                 "model": "rpg:item/michael_rib"}})


# ---------------------------------------------------------------------------
# the two items
# ---------------------------------------------------------------------------
RULE = '["",{"text":"%s","italic":false,"color":"white"}]' % ui.RULE_TEXT


def seg(text, colour=ui.GRAY, bold=False):
    return ('{"text":"%s","italic":false,"color":"%s"%s}'
            % (text, colour, ',"bold":true' if bold else ""))


def row(*segs):
    return '["",%s]' % ",".join(segs)


def name(text):
    return row(seg(ui.tier_tag("holy"), HOLY, True),
               '{"text":"%s","italic":false,"color":"%s","bold":false}'
               % (text, ui.WHITE))


SPINE = ("give @a netherite_spear["
         "custom_name=" + name("米迦勒脊骨") + ","
         "lore=[" + ",".join([
             RULE,
             row(seg("天使长呼喊"), seg("[谁似神]", HOLY, True)),
             row(seg("三分之一的"), seg("[星辰]", HOLY, True), seg("应声坠落")),
             RULE,
             row(seg("🗡主动技能", ui.WHITE), seg("[谁似神]", HOLY, True)),
             row(seg("蓄力1秒，前方%d格骨刺破土，挑飞并重创" % REACH)),
             row(seg("恶魔受到的伤害提高50%%并被点燃", ui.MUTED)),
             row(seg("与"), seg("[米迦勒肋骨]", HOLY, True),
                 seg("双持时骨刺延至%d格并叠上圣焰" % PAIR_REACH)),
             RULE]) + "],"
         # spears sit in #enchantable/melee_weapon and #enchantable/lunge but
         # not #enchantable/sweeping, hence no sweeping_edge here
         "enchantments={sharpness:5,fire_aspect:2,lunge:2,looting:2,unbreaking:3},"
         "attribute_modifiers=["
         '{type:"attack_damage",amount:12,operation:add_value,slot:mainhand,id:"rpg:michael/spine/0"},'
         '{type:"attack_speed",amount:-3.1,operation:add_value,slot:mainhand,id:"rpg:michael/spine/1"},'
         '{type:"entity_interaction_range",amount:1,operation:add_value,slot:mainhand,id:"rpg:michael/spine/2"},'
         # 副手的脊骨是一根不弯的脊梁
         '{type:"armor",amount:4,operation:add_value,slot:offhand,id:"rpg:michael/spine/3"},'
         '{type:"knockback_resistance",amount:0.3,operation:add_value,slot:offhand,id:"rpg:michael/spine/4"}],'
         "unbreakable={},"
         'tooltip_display={hidden_components:["minecraft:unbreakable"]},'
         "custom_model_data={floats:[%d.0f]}," % SPINE_CMD +
         "custom_data={michael_spine_tag:1b,holy_weapon_tag:1b,sword_tag:1b}]")

RIB = ("give @a netherite_sword["
       "custom_name=" + name("米迦勒肋骨") + ","
       "lore=[" + ",".join([
           RULE,
           row(seg("取自天使长"), seg("[肋旁]", HOLY, True), seg("的一根骨")),
           row(seg("火在其中，从未"), seg("[熄灭]", HOLY, True)),
           RULE,
           row(seg("🪓被动技能", ui.WHITE), seg("[圣焰]", HOLY, True)),
           row(seg("命中叠加圣焰，第3层引燃并灼烧")),
           row(seg("恶魔额外受创并显形", ui.MUTED)),
           row(seg("与"), seg("[米迦勒脊骨]", HOLY, True),
               seg("双持时每2层引燃，对路西法加倍")),
           RULE]) + "],"
       "enchantments={sharpness:5,sweeping_edge:3,fire_aspect:2,looting:3,unbreaking:3},"
       "attribute_modifiers=["
       '{type:"attack_damage",amount:9,operation:add_value,slot:mainhand,id:"rpg:michael/rib/0"},'
       '{type:"attack_speed",amount:-2.2,operation:add_value,slot:mainhand,id:"rpg:michael/rib/1"},'
       '{type:"attack_damage",amount:4,operation:add_value,slot:offhand,id:"rpg:michael/rib/2"}],'
       "unbreakable={},"
       'tooltip_display={hidden_components:["minecraft:unbreakable"]},'
       "custom_model_data={floats:[%d.0f]}," % RIB_CMD +
       "custom_data={michael_rib_tag:1b,holy_weapon_tag:1b,sword_tag:1b}]")


def build_give():
    path = os.path.join(FUNC, "command/give/weapon.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "米迦勒脊骨" in s:
        return False
    body = [s.rstrip("\n"), "",
            "# 米迦勒圣骸：脊骨（长枪·主动）与肋骨（剑·被动），左右手双持触发骨中之骨",
            SPINE, RIB, ""]
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(body))
    return True


def build_give_self():
    """单独入口：只把这一对发给执行者自己。组件与 give/weapon 里的两行逐字相同，
    make_boxes 按组件去重，所以潜影盒里仍然只收一份。"""
    self_give = lambda line: line.replace("give @a ", "give @s ", 1)
    wf("command/give/michael.mcfunction", "\n".join([
        "# 米迦勒圣骸：只发脊骨与肋骨，发给执行者自己（由 add_michael.py 生成）",
        "# 主手一把、副手一把即触发［骨中之骨］",
        self_give(SPINE), self_give(RIB)]))


def build_advancement():
    # 长枪的蓄力是真正的使用动作，using_item 直接响；custom_data 谓词
    # 让普通下界合金长枪不会触发任何东西
    wj(os.path.join(ADV, "michael_spine.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "items": "minecraft:netherite_spear",
                "predicates": {"minecraft:custom_data": "{michael_spine_tag:1b}"},
            }}}},
        "rewards": {"function": "rpg:item/extra/michael_trigger"},
    })


# ---------------------------------------------------------------------------
# 谁似神 -- the spine's skill
# ---------------------------------------------------------------------------
TRIGGER = """\
# 米迦勒脊骨［谁似神］—— 由 rpg:advancement/item/michael_spine 在蓄力时触发。
# using_item 在按住期间每刻都响：断了两刻以上就算重新起手，蓄满 {CHARGE} 刻出手。
# 蓄力与冷却都对着 gametime 量，不依赖每刻倒数。
advancement revoke @s only rpg:item/michael_spine
execute store result score #now rpg_mi_tmp run time query gametime
scoreboard players operation #gap rpg_mi_tmp = #now rpg_mi_tmp
scoreboard players operation #gap rpg_mi_tmp -= @s rpg_mi_last
execute unless score @s rpg_mi_last = @s rpg_mi_last run scoreboard players set #gap rpg_mi_tmp 99
execute if score #gap rpg_mi_tmp matches 3.. run scoreboard players set @s rpg_mi_hold 0
scoreboard players operation @s rpg_mi_last = #now rpg_mi_tmp

# 冷却中：起手那一下提示一次，之后按住也不再响
execute if score @s rpg_mi_cd > #now rpg_mi_tmp if score @s rpg_mi_hold matches 0 run playsound minecraft:entity.villager.no player @s
execute if score @s rpg_mi_cd > #now rpg_mi_tmp run return run scoreboard players set @s rpg_mi_hold -1
execute if score @s rpg_mi_hold matches ..-1 run return 0

scoreboard players add @s rpg_mi_hold 1
execute if score @s rpg_mi_hold matches ..{CHARGE_1} run function rpg:item/extra/michael_charge
execute if score @s rpg_mi_hold matches {CHARGE} run function rpg:item/extra/michael_cast
"""

CHARGE_FX = """\
# 蓄势：脊髓里的圣火往上涌
particle {FIRE} ~ ~1 ~ 0.35 0.45 0.35 0 2
execute if score @s rpg_mi_hold matches 1 run playsound minecraft:block.bone_block.place player @a[distance=..16] ~ ~ ~ 0.8 0.6
execute if score @s rpg_mi_hold matches 10 run playsound minecraft:block.respawn_anchor.charge player @a[distance=..16] ~ ~ ~ 0.6 1.6
"""

CAST = """\
# 谁似神：天使长的呼喊。前方 {REACH} 格骨刺破土，双持骨中之骨时延到 {PAIR_REACH} 格。
scoreboard players operation @s rpg_mi_cd = #now rpg_mi_tmp
scoreboard players add @s rpg_mi_cd {COOLDOWN}
tag @s add rpg.mi.cast
particle {FLASH} ~ ~0.2 ~ 0 0 0 0 1
particle {FIRE} ~ ~0.4 ~ 0.6 0.2 0.6 0.02 20
playsound minecraft:block.bone_block.break player @a[distance=..24] ~ ~ ~ 1 0.5
playsound minecraft:entity.blaze.shoot player @a[distance=..24] ~ ~ ~ 0.8 0.6
playsound minecraft:item.totem.use player @a[distance=..24] ~ ~ ~ 0.35 1.8

execute rotated ~ 0 run function rpg:item/extra/michael_spikes
execute if entity @s[tag=rpg.mi.pair] rotated ~ 0 run function rpg:item/extra/michael_spikes_far
execute as @e[tag=rpg.mi.spiked] at @s run function rpg:item/extra/michael_spike_hit

tag @s remove rpg.mi.cast
# 骨刺自己的伤害不算肋骨命中：清掉这一刻记下的输出
scoreboard players reset @s rpg_mi_dmg
"""

# one unrolled step: `positioned ^ ^ ^N` walks the flattened look vector
STEP = """\
execute positioned ^ ^ ^{N} run particle {BONE} ~ ~0.5 ~ 0.15 0.45 0.15 0 5
execute positioned ^ ^ ^{N} run particle {FIRE} ~ ~0.7 ~ 0.12 0.5 0.12 0 4
execute positioned ^ ^ ^{N} as @e[{LIVING},distance=..1.6] run tag @s add rpg.mi.spiked"""

SPIKE_HIT = """\
# 被骨刺挑中的一个。恶魔伤害提高一半并被点燃。
tag @s remove rpg.mi.spiked
execute if entity @s[tag=rpg.demon] run tag @s add rpg.mi.foe
execute if entity @s[tag=rpg.demon.minion] run tag @s add rpg.mi.foe
execute if entity @s[tag=!rpg.mi.foe] run damage @s 8 minecraft:magic by @a[tag=rpg.mi.cast,limit=1]
execute if entity @s[tag=rpg.mi.foe] run damage @s 12 minecraft:magic by @a[tag=rpg.mi.cast,limit=1]
execute if entity @s[tag=rpg.mi.foe] run data modify entity @s Fire set value 80s
data modify entity @s Motion[1] set value 0.55d
particle {BONE} ~ ~0.8 ~ 0.3 0.4 0.3 0 8
particle {FIRE} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
# 骨中之骨：骨刺挑中的直接叠上一层圣焰
execute if entity @a[tag=rpg.mi.cast,tag=rpg.mi.pair] run tag @a[tag=rpg.mi.cast] add rpg.mi.owner
execute if entity @a[tag=rpg.mi.owner] run function rpg:item/extra/michael_mark
tag @a[tag=rpg.mi.owner] remove rpg.mi.owner
tag @s remove rpg.mi.foe
"""

# ---------------------------------------------------------------------------
# 圣焰 -- the rib's passive, and 骨中之骨
# ---------------------------------------------------------------------------
TICK = """\
# 米迦勒圣骸的每刻结算。由 rpg:item/extra/michael_guard 守卫调用。

# 骨中之骨：一手脊骨、一手肋骨，左右不论
tag @a remove rpg.mi.pair
tag @a[tag=rpg.h.michael_spine_tag1,tag=rpg.o.michael_rib_tag1] add rpg.mi.pair
tag @a[tag=rpg.h.michael_rib_tag1,tag=rpg.o.michael_spine_tag1] add rpg.mi.pair

# 圣焰：握着肋骨（主手或副手）且这一刻打出了伤害
tag @a[tag=rpg.h.michael_rib_tag1,scores={{rpg_mi_dmg=1..}}] add rpg.mi.src
tag @a[tag=rpg.o.michael_rib_tag1,scores={{rpg_mi_dmg=1..}}] add rpg.mi.src
execute if entity @a[tag=rpg.mi.src] as @e[tag=rpg.hurt,{LIVING}] at @s if function rpg:item/extra/michael_by_rib run function rpg:item/extra/michael_rib_hit
tag @a[tag=rpg.mi.src] remove rpg.mi.src
scoreboard players reset * rpg_mi_dmg

# 圣焰的存续：引信、余烬与熄灭
execute as @e[tag=rpg.mi.fuse] at @s run function rpg:item/extra/michael_fuse
execute as @e[tag=rpg.mi.marked] at @s run function rpg:item/extra/michael_ember
scoreboard players set #mi_live rpg_mi_tmp 0
execute if entity @e[tag=rpg.mi.marked,limit=1] run scoreboard players set #mi_live rpg_mi_tmp 1
execute if entity @e[tag=rpg.mi.fuse,limit=1] run scoreboard players set #mi_live rpg_mi_tmp 1
"""

GUARD = """\
# 没人拿着圣骸、场上也没有未熄的圣焰时整段跳过。
execute if entity @a[tag=rpg.h.michael_rib_tag1] run return run function rpg:item/extra/michael
execute if entity @a[tag=rpg.o.michael_rib_tag1] run return run function rpg:item/extra/michael
execute if entity @a[tag=rpg.h.michael_spine_tag1] run return run function rpg:item/extra/michael
execute if entity @a[tag=rpg.o.michael_spine_tag1] run return run function rpg:item/extra/michael
execute if score #mi_live rpg_mi_tmp matches 1.. run function rpg:item/extra/michael
"""

BY_RIB = """\
# 这一下是不是握着肋骨的人打的
execute on attacker if entity @s[tag=rpg.mi.src] run return 1
return fail
"""

RIB_HIT = """\
execute on attacker run tag @s add rpg.mi.owner
function rpg:item/extra/michael_mark
tag @a[tag=rpg.mi.owner] remove rpg.mi.owner
"""

MARK = """\
# 叠一层圣焰。施加者带 rpg.mi.owner；它若双持骨中之骨，第二层就引燃。
execute if entity @s[tag=rpg.mi.fuse] run return 0
# 有圣焰在烧，守卫就得继续放行 —— 施加者换下圣骸，引信和余烬也照常走完
scoreboard players set #mi_live rpg_mi_tmp 1
scoreboard players add @s rpg_mi_flame 1
scoreboard players set @s rpg_mi_ttl {EMBER}
tag @s add rpg.mi.marked
scoreboard players set #need rpg_mi_tmp 3
execute if entity @a[tag=rpg.mi.owner,tag=rpg.mi.pair] run scoreboard players set #need rpg_mi_tmp 2
particle {FIRE} ~ ~1.1 ~ 0.25 0.35 0.25 0.02 6
execute if score @s rpg_mi_flame >= #need rpg_mi_tmp run function rpg:item/extra/michael_kindle
"""

KINDLE = """\
# 引燃：先点上引信，等目标的受击无敌过去再炸开，伤害才落得满
scoreboard players reset @s rpg_mi_flame
tag @s remove rpg.mi.marked
tag @s add rpg.mi.fuse
scoreboard players set @s rpg_mi_fuse {FUSE}
execute if entity @a[tag=rpg.mi.owner,tag=rpg.mi.pair] run tag @s add rpg.mi.pairfuse
playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.8 0.7
"""

FUSE_TICK = """\
scoreboard players remove @s rpg_mi_fuse 1
particle {FIRE} ~ ~1 ~ 0.3 0.4 0.3 0.01 2
execute if score @s rpg_mi_fuse matches ..0 run function rpg:item/extra/michael_ignite_hit
"""

IGNITE = """\
# 圣焰炸开。恶魔额外受创并显形；骨中之骨引燃的，对路西法加倍 ——
# 第一次神陨之战的败者，认得这团火。
tag @s remove rpg.mi.fuse
execute if entity @s[tag=rpg.demon] run tag @s add rpg.mi.foe
execute if entity @s[tag=rpg.demon.minion] run tag @s add rpg.mi.foe
execute if entity @s[tag=rpg.mi.pairfuse,tag=rpg.advent,scores={{rpg_dm_lord=1}}] run tag @s add rpg.mi.morningstar
execute if entity @s[tag=!rpg.mi.foe] run damage @s 6 minecraft:magic
execute if entity @s[tag=rpg.mi.foe,tag=!rpg.mi.morningstar] run damage @s 10 minecraft:magic
execute if entity @s[tag=rpg.mi.morningstar] run damage @s 20 minecraft:magic
data modify entity @s Fire set value 60s
execute if entity @s[tag=rpg.mi.foe] run effect give @s minecraft:glowing 5 0 true
particle {FLASH} ~ ~1.1 ~ 0 0 0 0 1
particle {FIRE_BIG} ~ ~1 ~ 0.4 0.5 0.4 0.05 20
playsound minecraft:entity.blaze.hurt player @a[distance=..16] ~ ~ ~ 0.8 0.6
execute if entity @s[tag=rpg.mi.morningstar] run playsound minecraft:item.trident.thunder player @a[distance=..24] ~ ~ ~ 0.6 1.4
tag @s remove rpg.mi.foe
tag @s remove rpg.mi.pairfuse
tag @s remove rpg.mi.morningstar
"""

EMBER_TICK = """\
# 未引燃的圣焰 {EMBER} 刻后熄灭
scoreboard players remove @s rpg_mi_ttl 1
particle {FIRE_SMALL} ~ ~1.2 ~ 0.25 0.35 0.25 0 1
execute if score @s rpg_mi_ttl matches ..0 run scoreboard players reset @s rpg_mi_flame
execute if score @s rpg_mi_ttl matches ..0 run tag @s remove rpg.mi.marked
"""

ARGS = dict(CHARGE=CHARGE, CHARGE_1=CHARGE - 1, COOLDOWN=COOLDOWN,
            REACH=REACH, PAIR_REACH=PAIR_REACH, FUSE=FUSE, EMBER=EMBER,
            FIRE=FIRE, FIRE_BIG=FIRE_BIG, FIRE_SMALL=FIRE_SMALL, BONE=BONE,
            FLASH=FLASH, LIVING=LIVING)


def build_functions():
    wf("item/extra/michael_trigger.mcfunction", TRIGGER.format(**ARGS))
    wf("item/extra/michael_charge.mcfunction", CHARGE_FX.format(**ARGS))
    wf("item/extra/michael_cast.mcfunction", CAST.format(**ARGS))
    near = ["# 骨刺的前 %d 格。`positioned ^ ^ ^N` 沿放平的视线取点，整条线不需要递归。"
            % REACH]
    near += [STEP.format(N=n, **ARGS) for n in range(1, REACH + 1)]
    wf("item/extra/michael_spikes.mcfunction", "\n".join(near))
    far = ["# 骨中之骨：骨刺再往前 %d 格。" % (PAIR_REACH - REACH)]
    far += [STEP.format(N=n, **ARGS) for n in range(REACH + 1, PAIR_REACH + 1)]
    wf("item/extra/michael_spikes_far.mcfunction", "\n".join(far))
    wf("item/extra/michael_spike_hit.mcfunction", SPIKE_HIT.format(**ARGS))

    wf("item/extra/michael.mcfunction", TICK.format(**ARGS))
    wf("item/extra/michael_guard.mcfunction", GUARD)
    wf("item/extra/michael_by_rib.mcfunction", BY_RIB)
    wf("item/extra/michael_rib_hit.mcfunction", RIB_HIT)
    wf("item/extra/michael_mark.mcfunction", MARK.format(**ARGS))
    wf("item/extra/michael_kindle.mcfunction", KINDLE.format(**ARGS))
    wf("item/extra/michael_fuse.mcfunction", FUSE_TICK.format(**ARGS))
    wf("item/extra/michael_ignite_hit.mcfunction", IGNITE.format(**ARGS))
    wf("item/extra/michael_ember.mcfunction", EMBER_TICK.format(**ARGS))

    path = os.path.join(FUNC, "item/extra/skills.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "item/extra/michael_guard" not in s:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\nfunction rpg:item/extra/michael_guard\n")


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    block = ["scoreboard objectives add %s %s" % (o, c)
             for o, c in OBJECTIVES
             if ("scoreboard objectives add %s " % o) not in s]
    if block:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n\n##米迦勒圣骸\n" + "\n".join(block) + "\n")
    return [b.split()[3] for b in block]


def register_index():
    """Main- and off-hand flags join the blocks add_twins.py already laid down,
    right after its 波阿斯 lines."""
    path = os.path.join(FUNC, "command/index.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "michael_spine_tag" in s:
        return 0
    anchors = [
        ("tag @a remove rpg.h.boaz_tag1",
         ["tag @a remove rpg.h.%s1" % t for t in MAINHAND]),
        ("execute as @a if items entity @s weapon.mainhand "
         "*[minecraft:custom_data~{boaz_tag:1b}] run tag @s add rpg.h.boaz_tag1",
         ["execute as @a if items entity @s weapon.mainhand "
          "*[minecraft:custom_data~{%s:1b}] run tag @s add rpg.h.%s1" % (t, t)
          for t in MAINHAND]),
        ("tag @a remove rpg.o.boaz_tag1",
         ["tag @a remove rpg.o.%s1" % t for t in OFFHAND]),
        ("execute as @a if items entity @s weapon.offhand "
         "*[minecraft:custom_data~{boaz_tag:1b}] run tag @s add rpg.o.boaz_tag1",
         ["execute as @a if items entity @s weapon.offhand "
          "*[minecraft:custom_data~{%s:1b}] run tag @s add rpg.o.%s1" % (t, t)
          for t in OFFHAND]),
    ]
    lines = s.split("\n")
    added = 0
    for anchor, new in anchors:
        assert anchor in lines, "index 里没有 add_twins 的锚点：" + anchor
        i = lines.index(anchor) + 1
        lines[i:i] = new
        added += len(new)
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    return added


if __name__ == "__main__":
    build_textures()
    build_models()
    build_functions()
    build_advancement()
    print("michael: give appended: %s" % build_give())
    build_give_self()
    print("michael: objectives added: %s"
          % (", ".join(add_objectives()) or "(already present)"))
    print("michael: index flags added: %d" % register_index())
