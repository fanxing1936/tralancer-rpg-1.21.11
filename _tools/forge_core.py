# -*- coding: utf-8 -*-
"""装备养成重置：工作台、登记与迁移、属性块渲染、经验与升级。

所有对装备的读写都在一个临时 item_display（工作台，WS）上做：
先把槽位里的物品复制进去，改完再复制回去。这样玩家、物品实体、
测试用的盔甲架都走同一套代码，NBT 路径也只有一种。
"""

import rpg_ui_style as ui
import forge_spec as S
from forge_common import WS, CD, EQ, J, c, NONE, LOCK, NA, name_comp

L_WHITE_B = dict(color=ui.WHITE, bold=True, italic=False)
SLOTS = {"main": "weapon.mainhand", "off": "weapon.offhand", "head": "armor.head",
         "chest": "armor.chest", "legs": "armor.legs", "feet": "armor.feet"}
OBJECTIVES = ["rpg_fg", "rpg_fg_lk", "rpg_fg_op", "rpg_fg_uid", "rpg_fg_arg", "rpg_fg_arg2",
              "rpg_fg_id", "rpg_fg_en", "rpg_fg_hit", "rpg_fg_idle", "rpg_fg_rw", "rpg_fg_rs",
              "rpg_fg_calm", "rpg_fg_lb", "rpg_fg_burn", "rpg_fg_bt", "rpg_fg_mark", "rpg_fg_mt",
              "rpg_fg_hv", "rpg_fg_hs", "rpg_fg_vid", "rpg_fg_ec", "rpg_fg_ea", "rpg_fg_eo",
              "rpg_fg_shd", "rpg_fg_bl", "rpg_fg_blh", "rpg_fg_tn", "rpg_fg_shot", "rpg_fg_crit",
              "rpg_fg_t", "rpg_fg_clk", "rpg_fg_mc", "rpg_fg_kx"]
BARS = ["▯▯▯▯▯", "▮▯▯▯▯", "▮▮▯▯▯", "▮▮▮▯▯", "▮▮▮▮▯", "▮▮▮▮▮"]
EXCLUDE_MAIN = ["offhand", "head", "chest", "legs", "feet", "armor", "body", "saddle"]
EXCLUDE_ARMOR = ["mainhand", "offhand", "hand"]
# 修饰值 ×1000 取整后四舍五入到 ×100：-2.2 存成 -2.2000000000000003，直接 ×100 取整会变成 -221。
# 计分板的除法是向下取整（floorDiv），所以正负数都是 +5 再除以 10。
ROUND_LINES = [
    "execute store result score #t rpg_fg run data get storage rpg:forge cur.amount 1000",
    "scoreboard players add #t rpg_fg 5",
    "scoreboard players operation #t rpg_fg /= #10 rpg_fg",
]


def lab(text):
    return dict(text=text, **L_WHITE_B)


def val(text, colour=ui.WHITE):
    return dict(text=text, color=colour, bold=False, italic=False)


# ---------------------------------------------------------------------------
# load：计分板、常数、名字表
# ---------------------------------------------------------------------------
def build_load(out):
    names = {"src": {"none": NONE}, "srcd": {"none": J(val(""))},
             "rune": {"none": NONE, "lock": LOCK}, "stone": {"none": NONE, "na": NA}}
    for s in S.SOURCES:
        names["src"][s["id"]] = name_comp("src", s["id"])
        names["srcd"][s["id"]] = name_comp("srcd", s["id"])
    for r in S.RUNES:
        names["rune"][r["id"]] = name_comp("rune", r["id"])
    for s in S.STONES:
        names["stone"][s["id"]] = name_comp("stone", s["id"])

    def snbt_strings(d):
        if isinstance(d, dict):
            return "{" + ",".join("%s:%s" % (k, snbt_strings(v)) for k, v in d.items()) + "}"
        return "'" + d + "'"

    lines = ["# 装备养成：计分板、常数与名字表（每次 /reload 重写）"]
    lines += ["scoreboard objectives add %s dummy" % o for o in OBJECTIVES]
    lines += [
        "scoreboard objectives add rpg_fg_do trigger",
        "scoreboard objectives add rpg_fg_dd minecraft.custom:minecraft.damage_dealt",
        "scoreboard objectives add rpg_fg_bow minecraft.used:minecraft.bow",
        "scoreboard objectives add rpg_fg_xbow minecraft.used:minecraft.crossbow",
    ]
    for k in (2, 3, 4, 5, 10, 15, 20, 25, 40, 60, 100, 150, 1000, 10000):
        lines.append("scoreboard players set #%d rpg_fg %d" % (k, k))
    lines += ["scoreboard players set #q0 rpg_fg -1000", "scoreboard players add #uid rpg_fg 0", "scoreboard players add #pid rpg_fg 0",
              "scoreboard players add #vid rpg_fg 0"]
    lines.append("data modify storage rpg:forge names set value " + snbt_strings(names))
    lines.append("data modify storage rpg:forge bars set value [%s]" % ",".join('"%s"' % b for b in BARS))
    lines.append("data modify storage rpg:forge prefixes set value [%s]" % ",".join('"%s"' % p for p in S.NAME_PREFIXES))
    out.fn("load", "\n".join(lines))


# ---------------------------------------------------------------------------
# 工作台
# ---------------------------------------------------------------------------
def build_workbench(out):
    out.fn("wb/new", "\n".join([
        "kill @e[type=minecraft:item_display,tag=rpg.fg.ws]",
        'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fg.ws"],view_range:0f}',
    ]))
    out.fn("wb/close", "kill @e[type=minecraft:item_display,tag=rpg.fg.ws]")
    for k, slot in SLOTS.items():
        out.fn("wb/load_" + k, "item replace entity %s contents from entity @s %s" % (WS, slot))
        out.fn("wb/save_" + k, "item replace entity @s %s from entity %s contents" % (slot, WS))
    out.fn("wb/load_item", "item replace entity %s contents from entity @s contents" % WS)
    out.fn("wb/save_item", "item replace entity @s contents from entity %s contents" % WS)


# ---------------------------------------------------------------------------
# 登记（第一次进入系统）与迁移
# ---------------------------------------------------------------------------
def build_restore(out, mig):
    rn = ["# 旧分支改名时把名字写成了对自身的 nbt 引用，原名丢了：按物品身份写回。"]
    for flag, name in mig["names"]:
        rn.append('execute if data entity %s %s.%s run data modify entity %s item.components."minecraft:custom_name" set value %s'
                  % (WS, CD, flag, WS, name))
    out.fn("mig/restore_name", "\n".join(rn))


def build_init(out, mig):
    """mig: add_forge 从 give 行算出的迁移表（原生圣器、名字、右键组件）。"""
    out.fn("init", "\n".join([
        "# 工作台里的装备进系统：判种类、迁移旧数据、算基础值、画属性块。",
        "# 返回 1 = 已登记；0 = 不是装备。",
        "execute if data entity %s %s run return 1" % (WS, EQ),
        "scoreboard players set #k rpg_fg 0",
        "execute if items entity %s contents #rpg:forge/armor run scoreboard players set #k rpg_fg 3" % WS,
        "execute if score #k rpg_fg matches 0 if items entity %s contents #rpg:forge/ranged run scoreboard players set #k rpg_fg 2" % WS,
        "execute if score #k rpg_fg matches 0 if items entity %s contents #rpg:forge/melee run scoreboard players set #k rpg_fg 1" % WS,
        "execute if score #k rpg_fg matches 0 if items entity %s contents *[minecraft:custom_data~{chestplate_tag:1b}] run scoreboard players set #k rpg_fg 3" % WS,
        "execute if score #k rpg_fg matches 0 if items entity %s contents *[minecraft:custom_data~{bow_tag:1b}] run scoreboard players set #k rpg_fg 2" % WS,
        "execute if score #k rpg_fg matches 0 if items entity %s contents *[minecraft:custom_data~{sword_tag:1b}] run scoreboard players set #k rpg_fg 1" % WS,
        "execute if score #k rpg_fg matches 0 run return 0",
        "function rpg:forge/mig/item",
        "data modify entity %s %s set value {v:1,q:0,lv:1,xp:0,gild:0b,gk:\"\",gl:0,src:\"none\",stone:\"none\",ln:0,base:0,spd:0,tough:0}" % (WS, EQ),
        'execute if score #k rpg_fg matches 1 run data modify entity %s %s merge value {kind:"melee",runes:["none","none"]}' % (WS, EQ),
        'execute if score #k rpg_fg matches 2 run data modify entity %s %s merge value {kind:"ranged",runes:["none","none"],base:100}' % (WS, EQ),
        'execute if score #k rpg_fg matches 3 run data modify entity %s %s merge value {kind:"armor",runes:["none"]}' % (WS, EQ),
        "scoreboard players add #uid rpg_fg 1",
        "execute store result entity %s %s.uid int 1 run scoreboard players get #uid rpg_fg" % (WS, EQ),
        "execute store result entity %s %s.lv int 1 run scoreboard players get #mlv rpg_fg" % (WS, EQ),
        'execute if score #mgild rpg_fg matches 1 run data modify entity %s %s merge value {gild:1b,gk:"legacy"}' % (WS, EQ),
        "execute if score #k rpg_fg matches 2..3 if data storage rpg:forge mig.src run data remove storage rpg:forge mig.src",
        "execute if data storage rpg:forge mig.src run data modify entity %s %s.src set from storage rpg:forge mig.src" % (WS, EQ),
        "execute if score #k rpg_fg matches 1 run function rpg:forge/base/melee",
        "execute if score #k rpg_fg matches 3 run function rpg:forge/base/armor",
        "execute if score #q0 rpg_fg matches -100.. store result entity %s %s.q int 1 run scoreboard players get #q0 rpg_fg" % (WS, EQ),
        "scoreboard players set #q0 rpg_fg -1000",
        "function rpg:forge/render",
        "return 1",
    ]))

    # ---- 基础值 ----
    def skip(excl):
        return " ".join('unless data storage rpg:forge cur{slot:"%s"}' % s for s in excl)

    out.fn("base/melee", "\n".join([
        "execute unless data entity %s item.components.\"minecraft:attribute_modifiers\" run item modify entity %s contents "
        "{function:\"minecraft:set_attributes\",replace:false,modifiers:[{attribute:\"minecraft:attack_damage\",id:\"rpg:forge/bonus\",amount:0,operation:\"add_value\",slot:\"mainhand\"}]}" % (WS, WS),
        "scoreboard players set #b rpg_fg 100",
        "scoreboard players set #s rpg_fg 400",
        "data modify storage rpg:forge it set from entity %s item.components.\"minecraft:attribute_modifiers\"" % WS,
        "function rpg:forge/base/melee_loop",
        "execute store result entity %s %s.base int 1 run scoreboard players get #b rpg_fg" % (WS, EQ),
        "execute store result entity %s %s.spd int 1 run scoreboard players get #s rpg_fg" % (WS, EQ),
    ]))
    out.fn("base/melee_loop", "\n".join([
        "execute unless data storage rpg:forge it[0] run return 0",
        "data modify storage rpg:forge cur set from storage rpg:forge it[0]",
        'execute if data storage rpg:forge cur{type:"minecraft:attack_damage",operation:"add_value"} unless data storage rpg:forge cur{id:"rpg:forge/bonus"} %s run function rpg:forge/base/add_b' % skip(EXCLUDE_MAIN),
        'execute if data storage rpg:forge cur{type:"minecraft:attack_speed",operation:"add_value"} %s run function rpg:forge/base/add_s' % skip(EXCLUDE_MAIN),
        "data remove storage rpg:forge it[0]",
        "function rpg:forge/base/melee_loop",
    ]))
    out.fn("base/add_b", "\n".join(ROUND_LINES + ["scoreboard players operation #b rpg_fg += #t rpg_fg"]))
    out.fn("base/add_s", "\n".join(ROUND_LINES + ["scoreboard players operation #s rpg_fg += #t rpg_fg"]))
    out.fn("base/armor", "\n".join([
        "execute unless data entity %s item.components.\"minecraft:attribute_modifiers\" run item modify entity %s contents "
        "{function:\"minecraft:set_attributes\",replace:false,modifiers:[{attribute:\"minecraft:armor\",id:\"rpg:forge/bonus\",amount:0,operation:\"add_value\",slot:\"armor\"}]}" % (WS, WS),
        "scoreboard players set #b rpg_fg 0",
        "scoreboard players set #s rpg_fg 0",
        "data modify storage rpg:forge it set from entity %s item.components.\"minecraft:attribute_modifiers\"" % WS,
        "function rpg:forge/base/armor_loop",
        "execute store result entity %s %s.base int 1 run scoreboard players get #b rpg_fg" % (WS, EQ),
        "execute store result entity %s %s.tough int 1 run scoreboard players get #s rpg_fg" % (WS, EQ),
    ]))
    out.fn("base/armor_loop", "\n".join([
        "execute unless data storage rpg:forge it[0] run return 0",
        "data modify storage rpg:forge cur set from storage rpg:forge it[0]",
        'execute if data storage rpg:forge cur{type:"minecraft:armor",operation:"add_value"} unless data storage rpg:forge cur{id:"rpg:forge/bonus"} %s run function rpg:forge/base/add_b' % skip(EXCLUDE_ARMOR),
        'execute if data storage rpg:forge cur{type:"minecraft:armor_toughness",operation:"add_value"} %s run function rpg:forge/base/add_s' % skip(EXCLUDE_ARMOR),
        "data remove storage rpg:forge it[0]",
        "function rpg:forge/base/armor_loop",
    ]))

    # ---- 迁移 ----
    m = [
        "# 旧系统留下的东西：12 行旧属性块、等级、镀金、旧符文符石、旧分支烙印。",
        "scoreboard players set #mlv rpg_fg 1",
        "scoreboard players set #mgild rpg_fg 0",
        "scoreboard players set #mstrip rpg_fg 0",
        "scoreboard players set #mrestore rpg_fg 0",
        "scoreboard players set #mname rpg_fg 0",
        "data remove storage rpg:forge mig",
        "data modify storage rpg:forge mig.refund set value []",
        "data remove storage rpg:forge t",
        'data modify storage rpg:forge t.a set from entity %s item.components."minecraft:lore"[0]' % WS,
        'data modify storage rpg:forge t.b set from entity %s item.components."minecraft:lore"[5]' % WS,
        'execute if data storage rpg:forge t{b:{extra:[{text:"[已镀金]"}]}} run scoreboard players set #mgild rpg_fg 1',
        'execute if data storage rpg:forge t{a:{extra:[{text:"+------装备属性------+"}]}} run function rpg:forge/mig/old_block',
        "execute if data entity %s %s.level store result score #mlv rpg_fg run data get entity %s %s.level" % (WS, CD, WS, CD),
        "execute if score #mlv rpg_fg matches 11.. run scoreboard players set #mlv rpg_fg 10",
        "execute if score #mlv rpg_fg matches ..0 run scoreboard players set #mlv rpg_fg 1",
    ]
    for key in ("weapon_tag", "level", "exp", "exp_max", "xilian", "add_weapon_tag"):
        m.append("data remove entity %s %s.%s" % (WS, CD, key))
    for flag, new in sorted(S.OLD_RUNE_TO_NEW.items()):
        m.append("execute if data entity %s %s.%s run function rpg:forge/mig/r_%s" % (WS, CD, flag, flag))
        out.fn("mig/r_" + flag, "\n".join([
            "data remove entity %s %s.%s" % (WS, CD, flag),
            "scoreboard players add #mstrip rpg_fg 3",
            'data modify storage rpg:forge mig.refund append value {k:"rune_%s"}' % new]))
    for flag, new in sorted(S.OLD_STONE_TO_NEW.items()):
        m.append("execute if data entity %s %s.%s run function rpg:forge/mig/s_%s" % (WS, CD, flag, flag))
        out.fn("mig/s_" + flag, "\n".join([
            "data remove entity %s %s.%s" % (WS, CD, flag),
            "scoreboard players add #mstrip rpg_fg 3",
            "scoreboard players set #mrestore rpg_fg 1",
            'data modify storage rpg:forge mig.refund append value {k:"stone_%s"}' % new]))
    m += [
        "function rpg:forge/mig/strip",
        "execute if score #mrestore rpg_fg matches 1 run function rpg:forge/mig/restore_use",
        # 旧分支烙印
        "scoreboard players set #nat rpg_fg 0",
    ]
    for flag in mig["native_holy"]:
        m.append("execute if data entity %s %s.%s run scoreboard players set #nat rpg_fg 1" % (WS, CD, flag))
    m += [
        'execute if data entity %s %s{armor_set:"holy"} run scoreboard players set #nat rpg_fg 1' % (WS, CD),
        "execute if data entity %s %s{holy_weapon_tag:2b} run function rpg:forge/mig/brand {src:\"hope\",key:\"holy_weapon_tag\"}" % (WS, CD),
        "execute if data entity %s %s{holy_weapon_tag:3b} run function rpg:forge/mig/brand {src:\"resolve\",key:\"holy_weapon_tag\"}" % (WS, CD),
        "execute if score #nat rpg_fg matches 0 if data entity %s %s{holy_weapon_tag:1b} run function rpg:forge/mig/brand {src:\"faith\",key:\"holy_weapon_tag\"}" % (WS, CD),
        "execute if data entity %s %s{devil_weapon_tag:1b} run function rpg:forge/mig/brand {src:\"malice\",key:\"devil_weapon_tag\"}" % (WS, CD),
        "execute if data entity %s %s{devil_weapon_tag:2b} run function rpg:forge/mig/brand {src:\"hatred\",key:\"devil_weapon_tag\"}" % (WS, CD),
        "execute if data entity %s %s{devil_weapon_tag:3b} run function rpg:forge/mig/brand {src:\"pride\",key:\"devil_weapon_tag\"}" % (WS, CD),
        "execute if score #mname rpg_fg matches 1 run function rpg:forge/mig/restore_name",
    ]
    out.fn("mig/item", "\n".join(m))
    out.fn("mig/old_block", "\n".join(
        ['data remove entity %s item.components."minecraft:lore"[0]' % WS] * 12))
    out.fn("mig/strip", "\n".join([
        "execute if score #mstrip rpg_fg matches ..0 run return 0",
        'data remove entity %s item.components."minecraft:lore"[-1]' % WS,
        "scoreboard players remove #mstrip rpg_fg 1",
        "function rpg:forge/mig/strip",
    ]))
    out.fn("mig/brand", "\n".join([
        "$data remove entity %s %s.$(key)" % (WS, CD),
        '$data modify storage rpg:forge mig.src set value "$(src)"',
        "scoreboard players set #mname rpg_fg 1",
    ]))
    rn = ["# 旧分支改名时把名字写成了对自身的 nbt 引用，原名丢了：按物品身份写回。"]
    for flag, name in mig["names"]:
        rn.append('execute if data entity %s %s.%s run data modify entity %s item.components."minecraft:custom_name" set value %s'
                  % (WS, CD, flag, WS, name))
    out.fn("mig/restore_name", "\n".join(rn))
    ru = ["# 旧符石把自己的右键组件盖在武器上：按物品身份还原，查不到就去掉。",
          "scoreboard players set #ru rpg_fg 0"]
    for flag, comps in mig["uses"]:
        ru.append("execute if score #ru rpg_fg matches 0 if data entity %s %s.%s run function rpg:forge/mig/use_%s"
                  % (WS, CD, flag, flag))
        body = ["scoreboard players set #ru rpg_fg 1"]
        for comp, value in comps:
            body.append('data modify entity %s item.components."minecraft:%s" set value %s' % (WS, comp, value))
        out.fn("mig/use_" + flag, "\n".join(body))
    ru += ['execute if score #ru rpg_fg matches 0 run data remove entity %s item.components."minecraft:consumable"' % WS,
           'execute if score #ru rpg_fg matches 0 run data remove entity %s item.components."minecraft:food"' % WS]
    out.fn("mig/restore_use", "\n".join(ru))
    out.fn("mig/refund", "\n".join([
        "# 迁移时剥下来的旧符文符石，换成新的退回背包。",
        "execute unless data storage rpg:forge mig.refund[0] run return 0",
        "data modify storage rpg:forge g.k set from storage rpg:forge mig.refund[0].k",
        "function rpg:forge/give/one",
        "data remove storage rpg:forge mig.refund[0]",
        "function rpg:forge/mig/refund",
    ]))
    keys = list(S.MATERIALS) + ["source_" + s["id"] for s in S.SOURCES] + ["rune_" + r["id"] for r in S.RUNES]         + ["stone_" + s["id"] for s in S.STONES]
    out.fn("give/one", chr(10).join(
        ['execute if data storage rpg:forge g{k:"%s"} run loot give @s loot rpg:forge/item/%s' % (k, k) for k in keys]))


# ---------------------------------------------------------------------------
# 数字格式与属性块
# ---------------------------------------------------------------------------
def build_render(out):
    out.fn("fmt", "\n".join([
        "# #v rpg_fg（×100 的整数）-> storage rpg:forge ui.<f.key>，两位小数，补零。",
        "scoreboard players operation #fi rpg_fg = #v rpg_fg",
        "scoreboard players operation #fi rpg_fg /= #100 rpg_fg",
        "scoreboard players operation #ff rpg_fg = #v rpg_fg",
        "scoreboard players operation #ff rpg_fg %= #100 rpg_fg",
        "execute store result storage rpg:forge f.i int 1 run scoreboard players get #fi rpg_fg",
        "execute store result storage rpg:forge f.d int 1 run scoreboard players get #ff rpg_fg",
        'data modify storage rpg:forge f.z set value ""',
        'execute if score #ff rpg_fg matches ..9 run data modify storage rpg:forge f.z set value "0"',
        "function rpg:forge/fmt_set with storage rpg:forge f",
    ]))
    out.fn("fmt_set", '$data modify storage rpg:forge ui.$(key) set value "$(i).$(z)$(d)"')

    r = [
        "# 按 rpg_eq 重算加成修饰、隐藏原版属性行、重画属性块（lore 最后 ln 行）。",
        "data modify storage rpg:forge ui set value {}",
        "data modify storage rpg:forge e set from entity %s %s" % (WS, EQ),
        "execute store result score #b rpg_fg run data get storage rpg:forge e.base",
        "execute store result score #q rpg_fg run data get storage rpg:forge e.q",
        "execute store result score #lv rpg_fg run data get storage rpg:forge e.lv",
        "execute store result score #xp rpg_fg run data get storage rpg:forge e.xp",
        "# 系数 ×10000 = (100+q)(98+2lv)",
        "scoreboard players operation #f rpg_fg = #q rpg_fg",
        "scoreboard players operation #f rpg_fg += #100 rpg_fg",
        "scoreboard players operation #g rpg_fg = #lv rpg_fg",
        "scoreboard players operation #g rpg_fg *= #2 rpg_fg",
        "scoreboard players add #g rpg_fg 98",
        "scoreboard players operation #f rpg_fg *= #g rpg_fg",
        "scoreboard players operation #bn rpg_fg = #f rpg_fg",
        "scoreboard players operation #bn rpg_fg -= #10000 rpg_fg",
        "scoreboard players operation #bn rpg_fg *= #b rpg_fg",
        "scoreboard players operation #bn rpg_fg /= #10000 rpg_fg",
        'execute if data storage rpg:forge e{kind:"melee"} run function rpg:forge/render/mod_melee',
        'execute if data storage rpg:forge e{kind:"armor"} run function rpg:forge/render/mod_armor',
        "# 品质",
        "execute store result storage rpg:forge ui.q int 1 run scoreboard players get #q rpg_fg",
        'data modify storage rpg:forge ui.qs set value ""',
        'execute if score #q rpg_fg matches 0.. run data modify storage rpg:forge ui.qs set value "+"',
    ]
    lo = -100
    for hi, name, colour in S.QUALITY:
        r.append('execute if score #q rpg_fg matches %d..%d run data modify storage rpg:forge ui merge value {qn:"%s",qc:"%s"}'
                 % (lo, hi, name, ui.hex_of(colour)))
        lo = hi + 1
    r += [
        "function rpg:forge/render/qp with storage rpg:forge ui",
        "# 等级",
        "execute store result storage rpg:forge ui.lv int 1 run scoreboard players get #lv rpg_fg",
        "execute store result storage rpg:forge ui.xp int 1 run scoreboard players get #xp rpg_fg",
        "scoreboard players operation #need rpg_fg = #lv rpg_fg",
        "scoreboard players operation #need rpg_fg *= #20 rpg_fg",
        "execute store result storage rpg:forge ui.need int 1 run scoreboard players get #need rpg_fg",
        "scoreboard players operation #n rpg_fg = #xp rpg_fg",
        "scoreboard players operation #n rpg_fg *= #5 rpg_fg",
        "scoreboard players operation #n rpg_fg /= #need rpg_fg",
    ]
    for i in range(6):
        r.append("execute if score #n rpg_fg matches %d run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[%d]" % (i, i))
    r += [
        "execute if score #lv rpg_fg matches ..%d run function rpg:forge/render/lv with storage rpg:forge ui" % (S.LV_MAX - 1),
        "execute if score #lv rpg_fg matches %d.. run function rpg:forge/render/lv_max" % S.LV_MAX,
        "# 镀金",
        "data modify storage rpg:forge ui.gp set value '%s'" % NONE,
        "execute if data storage rpg:forge e{gild:1b} run function rpg:forge/render/gp with storage rpg:forge e",
        'execute if data storage rpg:forge e{gild:1b,gk:"legacy"} run data modify storage rpg:forge ui.gp set value \'%s\'' % J(val("已镀金", S.C_GILD)),
        "# 源、符石、符文的名字",
        'data modify storage rpg:forge e.r1 set value "none"',
        'data modify storage rpg:forge e.r2 set value "none"',
        "data modify storage rpg:forge e.r1 set from storage rpg:forge e.runes[0]",
        "execute if data storage rpg:forge e.runes[1] run data modify storage rpg:forge e.r2 set from storage rpg:forge e.runes[1]",
        "function rpg:forge/render/names with storage rpg:forge e",
        "# 神圣之源、且装备 Lv.%d 以上：算圣器（index_player 读这个标记）" % S.HOLY_SOURCE_LV,
        "data remove entity %s %s.holy" % (WS, EQ),
    ] + ['execute if score #lv rpg_fg matches %d.. if data storage rpg:forge e{src:"%s"} run data modify entity %s %s.holy set value 1b'
         % (S.HOLY_SOURCE_LV, s["id"], WS, EQ) for s in S.SOURCES if s["side"] == "holy"] + [
        'execute if score #lv rpg_fg matches ..4 if data storage rpg:forge e{r2:"none"} run data modify storage rpg:forge ui.r2 set value \'%s\'' % LOCK,
        'execute if items entity %s contents *[minecraft:custom_data~{jachin_tag:1b}] run data modify storage rpg:forge ui.tc set value \'%s\'' % (WS, NA),
        'execute if items entity %s contents *[minecraft:custom_data~{boaz_tag:1b}] run data modify storage rpg:forge ui.tc set value \'%s\'' % (WS, NA),
        "# 数值",
        "scoreboard players operation #v rpg_fg = #b rpg_fg",
        "scoreboard players operation #v rpg_fg += #bn rpg_fg",
        'data modify storage rpg:forge f.key set value "dmg"',
        "function rpg:forge/fmt",
        "execute store result score #v rpg_fg run data get storage rpg:forge e.spd",
        'data modify storage rpg:forge f.key set value "spd"',
        "function rpg:forge/fmt",
        "execute store result score #v rpg_fg run data get storage rpg:forge e.tough",
        'data modify storage rpg:forge f.key set value "tough"',
        "function rpg:forge/fmt",
        "scoreboard players operation #v rpg_fg = #f rpg_fg",
        "scoreboard players operation #v rpg_fg /= #100 rpg_fg",
        'data modify storage rpg:forge f.key set value "fac"',
        "function rpg:forge/fmt",
        "execute store result entity %s %s.fac int 1 run scoreboard players get #v rpg_fg" % (WS, EQ),
        "# 画",
        'execute if data storage rpg:forge e{kind:"melee"} run function rpg:forge/render/lines_melee with storage rpg:forge ui',
        'execute if data storage rpg:forge e{kind:"ranged"} run function rpg:forge/render/lines_ranged with storage rpg:forge ui',
        'execute if data storage rpg:forge e{kind:"armor"} run function rpg:forge/render/lines_armor with storage rpg:forge ui',
        "execute store result score #ln rpg_fg run data get storage rpg:forge e.ln",
        "function rpg:forge/render/cut",
        'execute unless data entity %s item.components."minecraft:lore" run data modify entity %s item.components."minecraft:lore" set value []' % (WS, WS),
        'data modify entity %s item.components."minecraft:lore" append from storage rpg:forge L[]' % WS,
        "execute store result entity %s %s.ln int 1 run data get storage rpg:forge L" % (WS, EQ),
    ]
    out.fn("render", "\n".join(r))

    for kind, attr, slot in (("melee", "attack_damage", "mainhand"), ("armor", "armor", "armor")):
        out.fn("render/mod_" + kind, "\n".join([
            'data remove entity %s item.components."minecraft:attribute_modifiers"[{id:"rpg:forge/bonus"}]' % WS,
            'data modify entity %s item.components."minecraft:attribute_modifiers" append value '
            '{type:"minecraft:%s",id:"rpg:forge/bonus",amount:0.0d,operation:"add_value",slot:"%s"}' % (WS, attr, slot),
            'execute store result entity %s item.components."minecraft:attribute_modifiers"[-1].amount double 0.01 run scoreboard players get #bn rpg_fg' % WS,
            '# 原版的「在主手时」属性行和我们的属性块重复，藏起来',
            'execute unless data entity %s item.components."minecraft:tooltip_display" run data modify entity %s item.components."minecraft:tooltip_display" set value {hidden_components:[]}' % (WS, WS),
            'execute unless data entity %s item.components."minecraft:tooltip_display".hidden_components run data modify entity %s item.components."minecraft:tooltip_display".hidden_components set value []' % (WS, WS),
            'execute unless data entity %s item.components."minecraft:tooltip_display"{hidden_components:["minecraft:attribute_modifiers"]} run data modify entity %s item.components."minecraft:tooltip_display".hidden_components append value "minecraft:attribute_modifiers"' % (WS, WS),
        ]))
    out.fn("render/cut", "\n".join([
        "execute if score #ln rpg_fg matches ..0 run return 0",
        'data remove entity %s item.components."minecraft:lore"[-1]' % WS,
        "scoreboard players remove #ln rpg_fg 1",
        "function rpg:forge/render/cut",
    ]))
    out.fn("render/qp", "$data modify storage rpg:forge ui.qp set value '%s'" % J(
        {"text": "$(qn) $(qs)$(q)%", "color": "$(qc)", "bold": False, "italic": False}))
    out.fn("render/lv", "$data modify storage rpg:forge ui.lvp set value '%s'" % J(
        {"text": "", "extra": [lab("✦Lv.$(lv) "), val("$(bar)", S.C_LV_MAX), val(" $(xp)/$(need)", ui.MUTED)]}))
    out.fn("render/lv_max", "data modify storage rpg:forge ui.lvp set value '%s'" % J(
        {"text": "", "extra": [dict(text="✦Lv.%d " % S.LV_MAX, color=S.C_LV_MAX, bold=True, italic=False),
                               val("满级", S.C_LV_MAX)]}))
    out.fn("render/gp", "$data modify storage rpg:forge ui.gp set value '%s'" % J(
        {"text": "", "color": S.C_GILD, "bold": False, "italic": False,
         "extra": [{"translate": "$(gk)"}, {"text": " "}, {"translate": "enchantment.level.$(gl)"}]}))
    out.fn("render/names", "\n".join([
        "$data modify storage rpg:forge ui.sc set from storage rpg:forge names.src.$(src)",
        "$data modify storage rpg:forge ui.sd set from storage rpg:forge names.srcd.$(src)",
        "$data modify storage rpg:forge ui.tc set from storage rpg:forge names.stone.$(stone)",
        "$data modify storage rpg:forge ui.r1 set from storage rpg:forge names.rune.$(r1)",
        "$data modify storage rpg:forge ui.r2 set from storage rpg:forge names.rune.$(r2)",
    ]))
    RULE_ROW = J(["", val(ui.RULE_TEXT)])
    HEAD_ROW = J(["", val("◇ 装备属性", ui.MUTED)])
    line_q = '["",%s,$(qp),%s,$(gp)]' % (J(lab("🧪品质 ")), J(lab("　✧镀金 ")))
    line_lv = '["",$(lvp)]'
    line_src = '["",%s,$(sc),$(sd)]' % J(lab("◈源 "))
    line_st = '["",%s,$(tc)]' % J(lab("🔱符石 "))
    line_r2 = '["",%s,$(r1),%s,$(r2)]' % (J(lab("🪓符文 ")), J(val(" ")))
    line_r1 = '["",%s,$(r1)]' % J(lab("🪓符文 "))
    melee1 = J(["", lab("⚔伤害 "), val("$(dmg)"), lab("　⏱攻速 "), val("$(spd)")])
    ranged1 = J(["", lab("🏹箭伤 "), val("×$(fac)")])
    armor1 = J(["", lab("🛡护甲 "), val("$(dmg)"), lab("　◆韧性 "), val("$(tough)")])
    for kind, first, rest in (("melee", melee1, [line_lv, line_q, line_src, line_st, line_r2]),
                              ("ranged", ranged1, [line_lv, line_q, line_src, line_st, line_r2]),
                              ("armor", armor1, [line_lv, line_q, line_r1])):
        out.fn("render/lines_" + kind, "$data modify storage rpg:forge L set value [%s]"
               % ",".join([HEAD_ROW, first] + rest + [RULE_ROW]))


# ---------------------------------------------------------------------------
# 经验
# ---------------------------------------------------------------------------
def build_xp(out):
    out.fn("xp/add", "\n".join([
        "# 工作台里的装备加 #xa 点经验；升了几级记在 #up。",
        "scoreboard players set #up rpg_fg 0",
        "execute store result score #lv rpg_fg run data get entity %s %s.lv" % (WS, EQ),
        "execute if score #lv rpg_fg matches %d.. run return 0" % S.LV_MAX,
        "execute store result score #xp rpg_fg run data get entity %s %s.xp" % (WS, EQ),
        "scoreboard players operation #xp rpg_fg += #xa rpg_fg",
        "function rpg:forge/xp/loop",
        "execute store result entity %s %s.lv int 1 run scoreboard players get #lv rpg_fg" % (WS, EQ),
        "execute store result entity %s %s.xp int 1 run scoreboard players get #xp rpg_fg" % (WS, EQ),
        "function rpg:forge/render",
    ]))
    out.fn("xp/loop", "\n".join([
        "execute if score #lv rpg_fg matches %d.. run scoreboard players set #xp rpg_fg 0" % S.LV_MAX,
        "execute if score #lv rpg_fg matches %d.. run return 0" % S.LV_MAX,
        "scoreboard players operation #need rpg_fg = #lv rpg_fg",
        "scoreboard players operation #need rpg_fg *= #20 rpg_fg",
        "execute if score #xp rpg_fg < #need rpg_fg run return 0",
        "scoreboard players operation #xp rpg_fg -= #need rpg_fg",
        "scoreboard players add #lv rpg_fg 1",
        "scoreboard players add #up rpg_fg 1",
        "function rpg:forge/xp/loop",
    ]))
    for k in ("main", "head", "chest", "legs", "feet"):
        out.fn("xp/" + k, "\n".join([
            "function rpg:forge/wb/new",
            "function rpg:forge/wb/load_" + k,
            "function rpg:forge/xp/add",
            "function rpg:forge/wb/save_" + k,
            "function rpg:forge/wb/close",
            "execute if score #up rpg_fg matches 1.. run function rpg:forge/xp/up",
        ]))
    out.fn("xp/up", "\n".join([
        "playsound minecraft:block.trial_spawner.eject_item player @s ~ ~ ~ 0.8 1.4",
        "particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.3 24",
        'tellraw @s ["",{"text":"[锻造]","color":"%s","bold":true,"italic":false},{"text":"　装备升到了 ","color":"gray","italic":false},'
        '{"text":"Lv.","color":"#FFFFFF","bold":true,"italic":false},{"score":{"name":"#lv","objective":"rpg_fg"},"color":"#FFFFFF","bold":true,"italic":false}]'
        % ui.hex_of(S.C_FORGE),
    ]))
