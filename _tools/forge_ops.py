# -*- coding: utf-8 -*-
"""装备养成重置：右键入口、对话框、工坊六种操作、魂火冶炼。

流程：材料带 consumable，主手右键触发 using_item 进度 -> rpg:forge/use。
副手装备先进工作台登记，再按材料弹对话框；按钮走 trigger rpg_fg_do，
确认时重新核对副手装备（uid）和主手材料，核对通过才扣材料、改装备。
"""

import rpg_ui_style as ui
import forge_spec as S
from forge_common import WS, CD, EQ, J

T_HOLY = ui.BROADCAST_HOLY
T_NAME = ui.BROADCAST_NAME
T_BODY = ui.BROADCAST_BODY
T_WARN = ui.BROADCAST_WARN
T_MUTED = ui.MUTED

ELIGIBLE = ("unless items entity @s weapon.offhand #rpg:forge/any "
            "unless items entity @s weapon.offhand *[minecraft:custom_data~{sword_tag:1b}] "
            "unless items entity @s weapon.offhand *[minecraft:custom_data~{bow_tag:1b}] "
            "unless items entity @s weapon.offhand *[minecraft:custom_data~{chestplate_tag:1b}]")
CONSUME = 'item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}'


def t(text, colour=T_BODY, bold=False):
    return {"text": text, "color": ui.hex_of(colour) if not text.startswith("$") else colour,
            "bold": bold, "italic": False}


def tt(text, colour=T_BODY, bold=False):
    return {"text": text, "color": ui.hex_of(colour), "bold": bold, "italic": False}


NL = tt("\n")


def dialog(title, body, actions, exit_label="取消"):
    """body: 组件列表；actions: [(文字, 颜色, trigger 值)]。"""
    doc = {
        "type": "minecraft:multi_action",
        "title": ["", tt("[锻造]", T_HOLY, True), tt(" " + title, T_NAME)],
        "body": {"type": "minecraft:plain_message", "width": 300, "contents": [""] + body},
        "actions": [{"label": tt(label, colour, True),
                     "action": {"type": "minecraft:run_command", "command": "/trigger rpg_fg_do set %d" % v}}
                    for label, colour, v in actions],
        "columns": 2 if len(actions) != 1 else 1,
        "exit_action": {"label": tt(exit_label, T_MUTED)},
        "can_close_with_escape": True,
        "pause": False,
        "after_action": "close",
    }
    return "dialog show @s " + J(doc)


def say(text, colour=T_BODY):
    return "tellraw @s " + J(["", tt("[锻造]", S.C_FORGE, True), tt("　" + text, colour)])


def build_use(out):
    out.js("data/rpg/advancement/forge/use.json", {
        "criteria": {"use": {"trigger": "minecraft:using_item", "conditions": {
            "item": {"predicates": {"minecraft:custom_data": "{rpg_fm:1b}"}}}}},
        "rewards": {"function": "rpg:forge/use"}})
    dispatch = []
    for key in ("forge_stone", "wash_gem", "gild_leaf"):
        op = {"forge_stone": "xp", "wash_gem": "wash", "gild_leaf": "gild"}[key]
        dispatch.append('execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"%s"}] run function rpg:forge/op/%s/open' % (key, op))
    for s in S.SOURCES:
        dispatch.append('execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"%s"}] run function rpg:forge/op/src/open_%s' % (s["id"], s["id"]))
    for r in S.RUNES:
        dispatch.append('execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"%s"}] run function rpg:forge/op/rune/open_%s' % (r["id"], r["id"]))
    for s in S.STONES:
        dispatch.append('execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"%s"}] run function rpg:forge/op/stone/open_%s' % (s["id"], s["id"]))
    out.fn("use", "\n".join([
        "# 主手材料右键。长按期间进度每刻都会触发，用锁挡住重复弹窗。",
        "advancement revoke @s only rpg:forge/use",
        "scoreboard players set @s rpg_fg_lk 4",
        "execute if entity @s[tag=rpg.fg.ui] run return 0",
        "tag @s add rpg.fg.ui",
        "scoreboard players enable @s rpg_fg_do",
        "scoreboard players set @s rpg_fg_op 0",
        'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run function rpg:forge/smelt/open',
        "execute %s run return run %s" % (ELIGIBLE, say("副手拿着要养成的装备，主手拿材料再右键", T_WARN)),
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "execute store result score #ok rpg_fg run function rpg:forge/init",
        "execute if score #ok rpg_fg matches 0 run function rpg:forge/wb/close",
        "execute if score #ok rpg_fg matches 0 run return run %s" % say("这件东西不能养成", T_WARN),
        "function rpg:forge/wb/save_off",
        "function rpg:forge/mig/refund",
        "execute store result score @s rpg_fg_uid run data get entity %s %s.uid" % (WS, EQ),
        "data modify storage rpg:forge e set from entity %s %s" % (WS, EQ),
    ] + dispatch + ["function rpg:forge/wb/close"]))
    out.fn("ui/lock", "\n".join([
        "scoreboard players remove @s rpg_fg_lk 1",
        "execute if score @s rpg_fg_lk matches ..0 run tag @s remove rpg.fg.ui",
    ]))

    # 确认时核对主手材料
    chk = ["scoreboard players set #mm rpg_fg 0"]
    for key, op in (("forge_stone", 1), ("gild_leaf", 3)):
        chk.append('execute if score @s rpg_fg_op matches %d if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"%s"}] run scoreboard players set #mm rpg_fg 1' % (op, key))
    chk.append("execute if score @s rpg_fg_op matches 2 run scoreboard players set #mm rpg_fg 1")
    for op, key, lst in ((4, "rpg_src", S.SOURCES), (5, "rpg_rune", S.RUNES), (6, "rpg_stone", S.STONES)):
        for i, x in enumerate(lst):
            chk.append('execute if score @s rpg_fg_op matches %d if score @s rpg_fg_arg matches %d if items entity @s weapon.mainhand *[minecraft:custom_data~{%s:"%s"}] run scoreboard players set #mm rpg_fg 1'
                       % (op, i, key, x["id"]))
    out.fn("ui/check_mat", "\n".join(chk))

    do = [
        "# 对话框按钮。先核对，再执行。",
        "scoreboard players operation #do rpg_fg = @s rpg_fg_do",
        "scoreboard players set @s rpg_fg_do 0",
        "scoreboard players enable @s rpg_fg_do",
        "execute if score @s rpg_fg_op matches 10 run return run function rpg:forge/smelt/do",
        "execute if score @s rpg_fg_op matches 0 run return 0",
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "scoreboard players set #u rpg_fg -1",
        "execute store result score #u rpg_fg run data get entity %s %s.uid" % (WS, EQ),
        "function rpg:forge/ui/check_mat",
        "execute unless score #u rpg_fg = @s rpg_fg_uid run scoreboard players set #mm rpg_fg 0",
        "execute if score #mm rpg_fg matches 0 run function rpg:forge/wb/close",
        "execute if score #mm rpg_fg matches 0 run scoreboard players set @s rpg_fg_op 0",
        "execute if score #mm rpg_fg matches 0 run return run %s" % say("装备或材料换过了，这次操作作废，什么也没消耗", T_WARN),
        "data modify storage rpg:forge e set from entity %s %s" % (WS, EQ),
        "execute if score @s rpg_fg_op matches 1 if score #do rpg_fg matches 1 run function rpg:forge/op/xp/do",
        "execute if score @s rpg_fg_op matches 2 if score #do rpg_fg matches 3..4 run function rpg:forge/op/wash/do",
        "execute if score @s rpg_fg_op matches 3 if score #do rpg_fg matches 1 run function rpg:forge/op/gild/do",
    ]
    for i, s in enumerate(S.SOURCES):
        do.append("execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches %d if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_%s" % (i, s["id"]))
    for i, r in enumerate(S.RUNES):
        do.append("execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches %d if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_%s" % (i, r["id"]))
    for i, s in enumerate(S.STONES):
        do.append("execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches %d if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_%s" % (i, s["id"]))
    do += ["function rpg:forge/wb/save_off", "function rpg:forge/wb/close", "scoreboard players set @s rpg_fg_op 0"]
    out.fn("ui/do", "\n".join(do))
    out.fn("ui/done", "\n".join([
        "playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 0.9 1.1",
        "particle minecraft:wax_on ~ ~1 ~ 0.4 0.5 0.4 0.4 16",
    ]))


def cur_line(label, macro):
    return [tt(label, T_BODY), {"text": macro, "color": ui.hex_of(T_NAME), "bold": True, "italic": False}]


def build_xp(out):
    out.fn("op/xp/open", "\n".join([
        "execute if data storage rpg:forge e{lv:%d} run return run %s" % (S.LV_MAX, say("这件装备已经满级，铸造之石用不上")),
        "scoreboard players set @s rpg_fg_op 1",
        "execute store result score #lv rpg_fg run data get storage rpg:forge e.lv",
        "execute store result score #xp rpg_fg run data get storage rpg:forge e.xp",
        "execute store result storage rpg:forge d.lv0 int 1 run scoreboard players get #lv rpg_fg",
        "execute store result storage rpg:forge d.xp0 int 1 run scoreboard players get #xp rpg_fg",
        "scoreboard players add #xp rpg_fg %d" % S.XP_STONE,
        "scoreboard players set #up rpg_fg 0",
        "function rpg:forge/xp/loop",
        "scoreboard players operation #need rpg_fg = #lv rpg_fg",
        "scoreboard players operation #need rpg_fg *= #20 rpg_fg",
        "execute store result storage rpg:forge d.lv1 int 1 run scoreboard players get #lv rpg_fg",
        "execute store result storage rpg:forge d.xp1 int 1 run scoreboard players get #xp rpg_fg",
        "execute store result storage rpg:forge d.need int 1 run scoreboard players get #need rpg_fg",
        "function rpg:forge/op/xp/show with storage rpg:forge d",
    ]))
    out.fn("op/xp/show", "$" + dialog("铸造之石", [
        tt("装备经验 +%d" % S.XP_STONE, T_BODY), NL, NL,
        tt("当前　", T_MUTED), tt("Lv.$(lv0)　$(xp0)", T_NAME, True), NL,
        tt("之后　", T_MUTED), tt("Lv.$(lv1)　$(xp1)/$(need)", T_HOLY, True)],
        [("确认", T_HOLY, 1)]))
    out.fn("op/xp/do", "\n".join([
        "scoreboard players set #xa rpg_fg %d" % S.XP_STONE,
        "function rpg:forge/xp/add",
        CONSUME,
        "function rpg:forge/ui/done",
        "execute if score #up rpg_fg matches 1.. run function rpg:forge/xp/up",
    ]))


def grade_lines(score, prefix):
    out = ['data modify storage rpg:forge d.%ss set value ""' % prefix,
           'execute if score %s rpg_fg matches 0.. run data modify storage rpg:forge d.%ss set value "+"' % (score, prefix),
           "execute store result storage rpg:forge d.%s int 1 run scoreboard players get %s rpg_fg" % (prefix, score)]
    lo = -100
    for hi, name, _c in S.QUALITY:
        out.append('execute if score %s rpg_fg matches %d..%d run data modify storage rpg:forge d.%sn set value "%s"'
                   % (score, lo, hi, prefix, name))
        lo = hi + 1
    return out


def build_wash(out):
    out.fn("op/wash/open", "\n".join([
        "scoreboard players set @s rpg_fg_op 2",
        "execute store result score #q rpg_fg run data get storage rpg:forge e.q",
        "execute if data storage rpg:forge e.pq store result score #pq rpg_fg run data get storage rpg:forge e.pq",
        "execute unless data storage rpg:forge e.pq run function rpg:forge/op/wash/roll",
    ] + grade_lines("#q", "a") + grade_lines("#pq", "b") + [
        "function rpg:forge/op/wash/show with storage rpg:forge d",
    ]))
    out.fn("op/wash/roll", "\n".join([
        "# 洗炼钻在抽的时候就消耗；结果先挂在装备上，等你二选一。",
        "execute store result score #pq rpg_fg run random value %d..%d" % (S.Q_MIN, S.Q_MAX),
        "execute store result entity %s %s.pq int 1 run scoreboard players get #pq rpg_fg" % (WS, EQ),
        "function rpg:forge/wb/save_off",
        CONSUME,
        "playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2",
    ]))
    out.fn("op/wash/show", "$" + dialog("洗炼", [
        tt("洗炼钻已消耗。选择要保留的品质：", T_BODY), NL, NL,
        tt("原结果　", T_MUTED), tt("$(an) $(as)$(a)%", T_NAME, True), NL,
        tt("新结果　", T_MUTED), tt("$(bn) $(bs)$(b)%", T_HOLY, True), NL, NL,
        tt("关掉对话框不会丢掉新结果，下次再右键洗炼钻时接着选。", T_MUTED)],
        [("保留新结果", T_HOLY, 3), ("保留原结果", T_BODY, 4)], "稍后再选"))
    out.fn("op/wash/do", "\n".join([
        "execute unless data entity %s %s.pq run return 0" % (WS, EQ),
        "execute if score #do rpg_fg matches 3 run data modify entity %s %s.q set from entity %s %s.pq" % (WS, EQ, WS, EQ),
        "data remove entity %s %s.pq" % (WS, EQ),
        "function rpg:forge/render",
        "function rpg:forge/ui/done",
    ]))


def build_gild(out, enchants):
    out.fn("op/gild/open", "\n".join([
        "execute if data storage rpg:forge e{gild:1b} run return run %s" % say("这件装备已经镀过金，每件只能镀一次"),
        "scoreboard players set @s rpg_fg_op 3",
        dialog("镀金", [
            tt("随机挑一条已有附魔，等级 +1，可以超过原版上限。", T_BODY), NL,
            tt("装备上没有附魔时，随机附上一条。", T_BODY), NL, NL,
            tt("每件装备只能镀一次。", T_MUTED)],
            [("镀金", T_HOLY, 1)]),
    ]))
    scan = ["data modify storage rpg:forge cand set value []"]
    for eid in enchants:
        scan.append('execute if data entity %s item.components."minecraft:enchantments"."minecraft:%s" run data modify storage rpg:forge cand append value {id:"minecraft:%s",k:"enchantment.minecraft.%s"}'
                    % (WS, eid, eid, eid))
    scan.append("execute store result score #n rpg_fg run data get storage rpg:forge cand")
    out.fn("op/gild/scan", "\n".join(scan))
    out.fn("op/gild/do", "\n".join([
        "function rpg:forge/op/gild/scan",
        "execute if score #n rpg_fg matches 0 run item modify entity %s contents {function:\"minecraft:enchant_randomly\",only_compatible:true}" % WS,
        "execute if score #n rpg_fg matches 0 run function rpg:forge/op/gild/scan",
        "execute if score #n rpg_fg matches 0 run return run %s" % say("这件装备附不上任何附魔，镀金箔没有消耗", T_WARN),
        "scoreboard players remove #n rpg_fg 1",
        "execute store result storage rpg:forge d.m int 1 run scoreboard players get #n rpg_fg",
        "function rpg:forge/op/gild/pick with storage rpg:forge d",
        "function rpg:forge/op/gild/up with storage rpg:forge pick",
        "data modify entity %s %s.gild set value 1b" % (WS, EQ),
        "data modify entity %s %s.gk set from storage rpg:forge pick.k" % (WS, EQ),
        "execute store result entity %s %s.gl int 1 run scoreboard players get #gl rpg_fg" % (WS, EQ),
        "function rpg:forge/render",
        CONSUME,
        "playsound minecraft:item.totem.use player @s ~ ~ ~ 0.6 1.6",
        "particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0.6 40",
    ]))
    out.fn("op/gild/pick", "\n".join([
        "$execute store result score #r rpg_fg run random value 0..$(m)",
        "execute store result storage rpg:forge d.r int 1 run scoreboard players get #r rpg_fg",
        "function rpg:forge/op/gild/get with storage rpg:forge d",
    ]))
    out.fn("op/gild/get", "$data modify storage rpg:forge pick set from storage rpg:forge cand[$(r)]")
    out.fn("op/gild/up", "\n".join([
        '$execute store result score #gl rpg_fg run data get entity %s item.components."minecraft:enchantments"."$(id)"' % WS,
        "scoreboard players add #gl rpg_fg 1",
        '$execute store result entity %s item.components."minecraft:enchantments"."$(id)" int 1 run scoreboard players get #gl rpg_fg' % WS,
    ]))


def build_sources(out):
    for i, s in enumerate(S.SOURCES):
        other = "devil_tag" if s["side"] == "holy" else "holy_weapon_tag"
        side = "恶魔武器" if s["side"] == "holy" else "神圣武器"
        body = [tt("源　", T_MUTED), tt("$(cur)", T_NAME), tt(" → ", T_MUTED),
                tt("[%s]" % s["name"], s["colour"], True), NL, NL, tt(s["text"], T_BODY)]
        if s["cost"]:
            body += [NL, tt("代价　", T_MUTED), tt(s["cost"], T_WARN)]
        body += [NL, NL, tt("新源会覆盖旧源。", T_MUTED)]
        out.fn("op/src/open_" + s["id"], "\n".join([
            'execute if data storage rpg:forge e{kind:"armor"} run return run %s' % say("源只能给武器", T_WARN),
            "execute if items entity %s contents *[minecraft:custom_data~{%s:1b}] run return run %s"
            % (WS, other, say("%s接不住%s之源" % (side, s["name"]), T_WARN)),
            'execute if data storage rpg:forge e{src:"%s"} run return run %s' % (s["id"], say("已经是这个源了")),
            "scoreboard players set @s rpg_fg_op 4",
            "scoreboard players set @s rpg_fg_arg %d" % i,
            'data modify storage rpg:forge d.cur set value "无"',
        ] + ['execute if data storage rpg:forge e{src:"%s"} run data modify storage rpg:forge d.cur set value "[%s]"' % (x["id"], x["name"])
             for x in S.SOURCES] + [
            "function rpg:forge/op/src/show_%s with storage rpg:forge d" % s["id"],
        ]))
        out.fn("op/src/show_" + s["id"], "$" + dialog(s["name"] + "之源", body, [("注入", T_HOLY, 1)]))
        out.fn("op/src/do_" + s["id"], "\n".join([
            'data modify entity %s %s.src set value "%s"' % (WS, EQ, s["id"]),
            "function rpg:forge/render",
            CONSUME,
            "function rpg:forge/ui/done",
            "playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.7 1.3",
        ]))


def build_runes(out):
    for i, r in enumerate(S.RUNES):
        rid = r["id"]
        kind_ok = 'execute unless data storage rpg:forge e{kind:"%s"} run return run %s' % (
            r["part"], say("[%s]只能镶在%s上" % (r["name"], S.PART_NAME[r["part"]]), T_WARN))
        out.fn("op/rune/open_" + rid, "\n".join([
            kind_ok,
            'execute if data storage rpg:forge e{runes:["%s"]} run return run %s' % (rid, say("同一件装备不能镶两枚[%s]" % r["name"], T_WARN)),
            "scoreboard players set @s rpg_fg_op 5",
            "scoreboard players set @s rpg_fg_arg %d" % i,
            "scoreboard players set #free rpg_fg -1",
            "execute store result score #lv rpg_fg run data get storage rpg:forge e.lv",
            "function rpg:forge/op/rune/free_at {i:0}",
            'execute if score #free rpg_fg matches -1 unless data storage rpg:forge e{kind:"armor"} if score #lv rpg_fg matches 5.. run function rpg:forge/op/rune/free_at {i:1}',
            "execute if score #free rpg_fg matches 0.. run scoreboard players operation @s rpg_fg_arg2 = #free rpg_fg",
            "execute if score #free rpg_fg matches 0.. store result storage rpg:forge d.slot int 1 run scoreboard players add #free rpg_fg 1",
            "execute if score #free rpg_fg matches 1.. run return run function rpg:forge/op/rune/show_%s with storage rpg:forge d" % rid,
            "function rpg:forge/op/rune/full",
            "function rpg:forge/op/rune/swap_%s with storage rpg:forge d" % rid,
        ]))
        name = tt("[%s]" % r["name"], S.PART_COLOUR[r["part"]], True)
        out.fn("op/rune/show_" + rid, "$" + dialog("镶嵌符文", [
            tt("把 ", T_BODY), name, tt(" 镶进第 $(slot) 个符文槽。", T_BODY), NL, NL, tt(r["text"], T_BODY)],
            [("镶嵌", T_HOLY, 1)]))
        out.fn("op/rune/swap_" + rid, "$" + dialog("替换符文", [
            tt("符文槽已满。选一枚换成 ", T_BODY), name, tt("，换下来的符文退回背包。", T_BODY), NL, NL,
            tt(r["text"], T_BODY)],
            [("替换 $(o1)", T_HOLY, 10), ("替换 $(o2)", T_HOLY, 11)] if r["part"] != "armor" else [("替换 $(o1)", T_HOLY, 10)]))
        out.fn("op/rune/do_" + rid, "\n".join([
            "execute if score #do rpg_fg matches 10 run scoreboard players set @s rpg_fg_arg2 0",
            "execute if score #do rpg_fg matches 11 run scoreboard players set @s rpg_fg_arg2 1",
            "execute if score #do rpg_fg matches 11 if data storage rpg:forge e{kind:\"armor\"} run return 0",
            "execute store result score #lv rpg_fg run data get storage rpg:forge e.lv",
            "execute if score @s rpg_fg_arg2 matches 1 if score #lv rpg_fg matches ..4 run return run %s" % say("第二个符文槽要到 Lv.5 才解锁", T_WARN),
            'execute if data storage rpg:forge e{runes:["%s"]} run return 0' % rid,
            "execute store result storage rpg:forge g.i int 1 run scoreboard players get @s rpg_fg_arg2",
            'data modify storage rpg:forge g.v set value "%s"' % rid,
            "function rpg:forge/op/rune/put with storage rpg:forge g",
            "function rpg:forge/render",
            CONSUME,
            "function rpg:forge/ui/done",
        ]))
    out.fn("op/rune/free_at", "\n".join([
        "$data modify storage rpg:forge g.t set from storage rpg:forge e.runes[$(i)]",
        '$execute if data storage rpg:forge g{t:"none"} run scoreboard players set #free rpg_fg $(i)',
    ]))
    full = ['data modify storage rpg:forge d.o1 set value "—"', 'data modify storage rpg:forge d.o2 set value "—"',
            'data modify storage rpg:forge g.a set value "none"', 'data modify storage rpg:forge g.b set value "none"',
            "data modify storage rpg:forge g.a set from storage rpg:forge e.runes[0]",
            "execute if data storage rpg:forge e.runes[1] run data modify storage rpg:forge g.b set from storage rpg:forge e.runes[1]"]
    for r in S.RUNES:
        full.append('execute if data storage rpg:forge g{a:"%s"} run data modify storage rpg:forge d.o1 set value "[%s]"' % (r["id"], r["name"]))
        full.append('execute if data storage rpg:forge g{b:"%s"} run data modify storage rpg:forge d.o2 set value "[%s]"' % (r["id"], r["name"]))
    out.fn("op/rune/full", "\n".join(full))
    out.fn("op/rune/put", "\n".join([
        "# 退回槽里原来的符文，再写入新的。",
        "$data modify storage rpg:forge g.o set from entity %s %s.runes[$(i)]" % (WS, EQ),
        'execute unless data storage rpg:forge g{o:"none"} run function rpg:forge/op/rune/refund',
        "$data modify entity %s %s.runes[$(i)] set value \"$(v)\"" % (WS, EQ),
    ]))
    out.fn("op/rune/refund", chr(10).join(
        ['execute if data storage rpg:forge g{o:"%s"} run loot give @s loot rpg:forge/item/rune_%s' % (r["id"], r["id"]) for r in S.RUNES]))


def build_stones(out):
    for i, s in enumerate(S.STONES):
        sid = s["id"]
        if s["part"] == "any":
            kind_ok = 'execute if data storage rpg:forge e{kind:"armor"} run return run %s' % say("符石只能镶在武器上", T_WARN)
        else:
            kind_ok = 'execute unless data storage rpg:forge e{kind:"%s"} run return run %s' % (
                s["part"], say("[%s]只能镶在%s上" % (s["name"], S.PART_NAME[s["part"]]), T_WARN))
        out.fn("op/stone/open_" + sid, "\n".join([
            kind_ok,
            "execute if items entity %s contents *[minecraft:custom_data~{jachin_tag:1b}] run return run %s" % (WS, say("双子武器靠换手作战，不开符石槽", T_WARN)),
            "execute if items entity %s contents *[minecraft:custom_data~{boaz_tag:1b}] run return run %s" % (WS, say("双子武器靠换手作战，不开符石槽", T_WARN)),
            'execute if data storage rpg:forge e{stone:"%s"} run return run %s' % (sid, say("已经镶着这枚符石了")),
            "scoreboard players set @s rpg_fg_op 6",
            "scoreboard players set @s rpg_fg_arg %d" % i,
            'data modify storage rpg:forge d.cur set value "空"',
        ] + ['execute if data storage rpg:forge e{stone:"%s"} run data modify storage rpg:forge d.cur set value "[%s]（退回背包）"' % (x["id"], x["name"])
             for x in S.STONES] + ["function rpg:forge/op/stone/show_%s with storage rpg:forge d" % sid]))
        out.fn("op/stone/show_" + sid, "$" + dialog("镶嵌符石", [
            tt("符石槽　", T_MUTED), tt("$(cur)", T_NAME), tt(" → ", T_MUTED),
            tt("[%s]" % s["name"], S.STONE_COLOUR[sid], True), NL, NL, tt(s["text"], T_BODY), NL, NL,
            tt("打怪攒能量，满 %d 时按 F 释放；潜行按 F 照常换手。" % S.ENERGY_MAX, T_MUTED)],
            [("镶嵌", T_HOLY, 1)]))
        out.fn("op/stone/do_" + sid, "\n".join([
            "data modify storage rpg:forge g.o set from entity %s %s.stone" % (WS, EQ),
            'execute unless data storage rpg:forge g{o:"none"} run function rpg:forge/op/stone/refund',
            'data modify entity %s %s.stone set value "%s"' % (WS, EQ, sid),
            "function rpg:forge/render",
            CONSUME,
            "function rpg:forge/ui/done",
        ]))
    out.fn("op/stone/refund", chr(10).join(
        ['execute if data storage rpg:forge g{o:"%s"} run loot give @s loot rpg:forge/item/stone_%s' % (s["id"], s["id"]) for s in S.STONES]))


# ---------------------------------------------------------------------------
# 魂火冶炼
# ---------------------------------------------------------------------------
def build_smelt(out, make_lines):
    out.js("data/rpg/tags/block/forge/soul_fire.json",
           {"values": ["minecraft:soul_campfire", "minecraft:soul_fire"]})
    out.fn("smelt/open", "\n".join([
        "scoreboard players set #i rpg_fg 30",
        "scoreboard players set #found rpg_fg 0",
        "execute anchored eyes positioned ^ ^ ^ run function rpg:forge/smelt/ray",
        "execute if score #found rpg_fg matches 0 run return run %s" % say("手持器胚，对准灵魂营火（或灵魂火）右键", T_WARN),
        "scoreboard players set @s rpg_fg_op 10",
        "scoreboard players set @s rpg_fg_arg -1",
        dialog("魂火冶炼 · 造什么", [tt("选择要冶炼的装备。", T_BODY), NL,
                                     tt("下一步选主材，主材决定档次。", T_MUTED), NL,
                                     tt("也可以在这里锻造罪器、转换材料。", T_MUTED)],
               [(name, T_NAME, 20 + k) for k, (_key, name, _kind, _b) in enumerate(S.SMELT_TYPES)] +
               [("罪器锻造", T_HOLY, 50), ("材料转换", T_HOLY, 60)]),
    ]))
    out.fn("smelt/ray", "\n".join([
        "execute if block ~ ~ ~ #rpg:forge/soul_fire run return run function rpg:forge/smelt/found",
        "scoreboard players remove #i rpg_fg 1",
        "execute if score #i rpg_fg matches 1.. positioned ^ ^ ^0.2 run function rpg:forge/smelt/ray",
    ]))
    out.fn("smelt/found", "\n".join([
        "scoreboard players set #found rpg_fg 1",
        "scoreboard players operation #me rpg_fg = @s rpg_fg_id",
        "execute as @e[type=minecraft:marker,tag=rpg.fg.fire] if score @s rpg_fg_eo = #me rpg_fg run kill @s",
        'execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fire","rpg.fg.new"]}',
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_eo = #me rpg_fg",
        "tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new",
    ]))
    count = [
        "execute store result score #ni rpg_fg run clear @s minecraft:iron_ingot[!minecraft:custom_data] 0",
        "execute store result score #nd rpg_fg run clear @s minecraft:diamond[!minecraft:custom_data] 0",
        "execute store result score #nn rpg_fg run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 0",
        'execute store result score #ns rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0',
        "execute store result storage rpg:forge d.ni int 1 run scoreboard players get #ni rpg_fg",
        "execute store result storage rpg:forge d.nd int 1 run scoreboard players get #nd rpg_fg",
        "execute store result storage rpg:forge d.nn int 1 run scoreboard players get #nn rpg_fg",
        "execute store result storage rpg:forge d.ns int 1 run scoreboard players get #ns rpg_fg",
    ]
    out.fn("smelt/count", "\n".join(count))
    # 档次是否够料：#ok_t0..2
    enough = []
    for k, (tkey, _disp, mats) in enumerate(S.TIERS):
        enough.append("scoreboard players set #ok%d rpg_fg 1" % k)
        for item, n in mats:
            sc = {"iron_ingot": "#ni", "diamond": "#nd", "netherite_ingot": "#nn"}[item]
            enough.append("execute if score %s rpg_fg matches ..%d run scoreboard players set #ok%d rpg_fg 0" % (sc, n - 1, k))
    out.fn("smelt/enough", "\n".join(enough))

    tier_body = [tt("主材决定档次，残魂决定品质抽几次（至多 %d 次）。" % S.SOUL_MAX, T_BODY), NL, NL]
    for k, (tkey, disp, mats) in enumerate(S.TIERS):
        label = ui.tier_tag(disp) if disp else "无档"
        colour = ui.tier_colour(disp) if disp else T_NAME
        need = "、".join("%s ×%d" % (S.TIER_MAT_NAME[i], n) for i, n in mats)
        tier_body += [tt(label + "　", colour, True), tt(need, T_BODY), NL]
    tier_body += [NL, tt("背包里　", T_MUTED),
                  tt("铁锭 $(ni)　钻石 $(nd)　下界合金锭 $(nn)　残魂 $(ns)", T_NAME)]
    out.fn("smelt/tiers", "$" + dialog("魂火冶炼 · 主材", tier_body,
                                        [((ui.tier_tag(d) if d else "无档"), (ui.tier_colour(d) if d else T_NAME), 30 + k)
                                         for k, (_t, d, _m) in enumerate(S.TIERS)]))
    conf = [tt("将冶炼　", T_MUTED), tt("$(what)", T_NAME, True), NL,
            tt("消耗　", T_MUTED), tt("器胚 ×1、$(mats)、残魂 ×$(souls)", T_BODY), NL,
            tt("品质　", T_MUTED), tt("抽 $(souls) 次，取最好的一次", T_BODY), NL, NL,
            tt("冶炼约 3 秒，成品从营火里弹出。", T_MUTED)]
    out.fn("smelt/confirm", "$" + dialog("魂火冶炼 · 确认", conf, [("开炉", T_HOLY, 40)]))

    d = [
        "# 冶炼对话框的三步：20..28 选类型，30..32 选档次，40 开炉。50..59 罪器锻造、60..69 材料转换（add_forge_world.py）。",
        "execute if score #do rpg_fg matches 50..59 run return run function rpg:forge/sin/do",
        "execute if score #do rpg_fg matches 60..69 run return run function rpg:forge/conv/do",
        "execute if score #do rpg_fg matches 20..28 run scoreboard players operation @s rpg_fg_arg = #do rpg_fg",
        "execute if score #do rpg_fg matches 20..28 run scoreboard players remove @s rpg_fg_arg 20",
        "execute if score #do rpg_fg matches 20..28 run function rpg:forge/smelt/count",
        "execute if score #do rpg_fg matches 20..28 run return run function rpg:forge/smelt/tiers with storage rpg:forge d",
        "execute if score #do rpg_fg matches 30..32 run scoreboard players operation @s rpg_fg_arg2 = #do rpg_fg",
        "execute if score #do rpg_fg matches 30..32 run scoreboard players remove @s rpg_fg_arg2 30",
        "execute if score #do rpg_fg matches 30..32 run return run function rpg:forge/smelt/check",
        "execute if score #do rpg_fg matches 40 run return run function rpg:forge/smelt/start",
    ]
    out.fn("smelt/do", "\n".join(d))
    chk = [
        "execute if score @s rpg_fg_arg matches ..-1 run return 0",
        "function rpg:forge/smelt/count",
        "function rpg:forge/smelt/enough",
        "scoreboard players set #ok rpg_fg 0",
    ]
    for k in range(len(S.TIERS)):
        chk.append("execute if score @s rpg_fg_arg2 matches %d if score #ok%d rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1" % (k, k))
    chk += [
        "execute if score #ok rpg_fg matches 0 run return run %s" % say("主材不够，这一档开不了炉", T_WARN),
        "execute if score #ns rpg_fg matches 0 run return run %s" % say("至少需要 1 枚残魂", T_WARN),
        "scoreboard players operation #souls rpg_fg = #ns rpg_fg",
        "execute if score #souls rpg_fg matches %d.. run scoreboard players set #souls rpg_fg %d" % (S.SOUL_MAX + 1, S.SOUL_MAX),
        "execute store result storage rpg:forge d.souls int 1 run scoreboard players get #souls rpg_fg",
    ]
    for k, (tkey, disp, mats) in enumerate(S.TIERS):
        need = "、".join("%s ×%d" % (S.TIER_MAT_NAME[i], n) for i, n in mats)
        chk.append('execute if score @s rpg_fg_arg2 matches %d run data modify storage rpg:forge d.mats set value "%s"' % (k, need))
        for j, (key, name, _kind, _b) in enumerate(S.SMELT_TYPES):
            label = (ui.tier_tag(disp) if disp else "") + name
            chk.append('execute if score @s rpg_fg_arg2 matches %d if score @s rpg_fg_arg matches %d run data modify storage rpg:forge d.what set value "%s"'
                       % (k, j, label))
    chk.append("function rpg:forge/smelt/confirm with storage rpg:forge d")
    out.fn("smelt/check", "\n".join(chk))

    st = [
        "# 开炉：再核对一遍，扣料，抽品质，把火点变成冶炼中的标记。",
        'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run %s' % say("主手要拿着器胚", T_WARN),
        "scoreboard players operation #me rpg_fg = @s rpg_fg_id",
        "scoreboard players set #fire rpg_fg 0",
        "execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1",
        "execute if score #fire rpg_fg matches 0 run return run %s" % say("离灵魂火太远了，靠近些再开炉", T_WARN),
        "function rpg:forge/smelt/count",
        "function rpg:forge/smelt/enough",
        "scoreboard players set #ok rpg_fg 0",
    ]
    for k in range(len(S.TIERS)):
        st.append("execute if score @s rpg_fg_arg2 matches %d if score #ok%d rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1" % (k, k))
    st += [
        "execute if score #ok rpg_fg matches 0 run return run %s" % say("主材不够了", T_WARN),
        "execute if score #ns rpg_fg matches 0 run return run %s" % say("至少需要 1 枚残魂", T_WARN),
        "scoreboard players operation #souls rpg_fg = #ns rpg_fg",
        "execute if score #souls rpg_fg matches %d.. run scoreboard players set #souls rpg_fg %d" % (S.SOUL_MAX + 1, S.SOUL_MAX),
        CONSUME,
    ]
    for k, (tkey, disp, mats) in enumerate(S.TIERS):
        for item, n in mats:
            st.append("execute if score @s rpg_fg_arg2 matches %d run clear @s minecraft:%s[!minecraft:custom_data] %d" % (k, item, n))
    st += [
        "execute store result storage rpg:forge d.souls int 1 run scoreboard players get #souls rpg_fg",
        "function rpg:forge/smelt/take with storage rpg:forge d",
        "scoreboard players set #best rpg_fg -100",
        "function rpg:forge/smelt/roll",
        "execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg run tag @s add rpg.fg.go",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_arg = @s rpg_fg_arg",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_arg2 = @s rpg_fg_arg2",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_mc = #best rpg_fg",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_t 60",
        "tag @e[type=minecraft:marker,tag=rpg.fg.go] add rpg.fg.smelt",
        "tag @e[type=minecraft:marker,tag=rpg.fg.go] remove rpg.fg.fire",
        "tag @e[type=minecraft:marker,tag=rpg.fg.go] remove rpg.fg.go",
        "scoreboard players set @s rpg_fg_op 0",
        "playsound minecraft:block.blastfurnace.fire_crackle player @a[distance=..16] ~ ~ ~ 1 0.6",
        say("魂火吞下了材料……"),
    ]
    out.fn("smelt/start", "\n".join(st))
    out.fn("smelt/take", '$clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] $(souls)')
    out.fn("smelt/roll", "\n".join([
        "execute if score #souls rpg_fg matches ..0 run return 0",
        "execute store result score #r rpg_fg run random value %d..%d" % (S.Q_MIN, S.Q_MAX),
        "execute if score #r rpg_fg > #best rpg_fg run scoreboard players operation #best rpg_fg = #r rpg_fg",
        "scoreboard players remove #souls rpg_fg 1",
        "function rpg:forge/smelt/roll",
    ]))
    out.fn("smelt/tick", "\n".join([
        "# 冶炼中的火点：3 秒魂火，然后出炉。",
        "particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.25 0.4 0.25 0.02 6",
        "particle minecraft:sculk_soul ~ ~1.2 ~ 0.2 0.3 0.2 0.02 2",
        "execute if score @s rpg_fg_t matches 20 run playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 0.6 0.7",
        "execute if score @s rpg_fg_t matches 40 run playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 0.6 0.9",
        "scoreboard players remove @s rpg_fg_t 1",
        "execute if score @s rpg_fg_t matches ..0 run function rpg:forge/smelt/make",
    ]))
    mk = [
        "function rpg:forge/wb/new",
        "execute store result score #r rpg_fg run random value 0..%d" % (len(S.NAME_PREFIXES) - 1),
        "execute store result storage rpg:forge nm.r int 1 run scoreboard players get #r rpg_fg",
        "function rpg:forge/smelt/prefix with storage rpg:forge nm",
    ]
    for k in range(len(S.TIERS)):
        for j, (key, _n, _kind, _b) in enumerate(S.SMELT_TYPES):
            mk.append("execute if score @s rpg_fg_arg2 matches %d if score @s rpg_fg_arg matches %d run function rpg:forge/smelt/m/%s_%s with storage rpg:forge nm"
                      % (k, j, key, S.TIERS[k][0]))
    mk += [
        "scoreboard players operation #q0 rpg_fg = @s rpg_fg_mc",
        "execute as %s run function rpg:forge/init" % WS,
        'summon minecraft:item ~ ~0.8 ~ {Item:{id:"minecraft:stone",count:1},Tags:["rpg.fg.out"],PickupDelay:10,Motion:[0.0,0.25,0.0]}',
        "data modify entity @e[type=minecraft:item,tag=rpg.fg.out,limit=1,sort=nearest] Item set from entity %s item" % WS,
        "tag @e[type=minecraft:item,tag=rpg.fg.out] remove rpg.fg.out",
        "function rpg:forge/wb/close",
        "particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.05 30",
        "playsound minecraft:block.trial_spawner.eject_item block @a[distance=..16] ~ ~ ~ 1 0.8",
        "scoreboard players operation #me rpg_fg = @s rpg_fg_eo",
        "execute as @a if score @s rpg_fg_id = #me rpg_fg run %s" % say("成品出炉了"),
        "kill @s",
    ]
    out.fn("smelt/make", "\n".join(mk))
    out.fn("smelt/prefix", "$data modify storage rpg:forge nm.p set from storage rpg:forge prefixes[$(r)]")
    for fn, text in make_lines:
        out.fn(fn, text)
