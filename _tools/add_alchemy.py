# -*- coding: utf-8 -*-
"""药水、炼药与制器（策划书「药水、遗物与器物纹理」；数据在 potion_spec.py）。

    python add_alchemy.py ../rpg --items   # make_boxes 之前：原来 8 瓶换成新写法，补 12 瓶、空瓶、空白圣具（进领取目录）
    python add_alchemy.py ../rpg           # 装备养成、商人、事件、精英之后：炼药页、制器页、效果、来路

* 空瓶对准灵魂营火右键 → 炼药页；空白圣具 → 制器页。走装备养成的 use / 按钮（rpg_fg_do 200..259），不加新的触发器。
* 材料一律只认没有 custom_data 的（遗物与锻造原料就是这样写的），点按钮时再核对一遍才扣。
* 药水图标由资源包按 custom_data 分派（add_relic_art.py），物品本身不写 item_model。
"""
import io
import json
import os
import re
import sys

import forge_ops as FO
import potion_spec as S
import rpg_ui_style as ui
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
LOOT = os.path.join(DP, "data", "rpg", "loot_table")
P = "rpg:alc"
COUNT = 0
C_ALC = "#8FD0C0"
VIAL = '*[minecraft:custom_data~{rpg_mat:"vial"}]'
BLANK = '*[minecraft:custom_data~{rpg_mat:"blank_rite"}]'
SOUL = 'minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}]'


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, "alc", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def snbt(v):
    if isinstance(v, dict):
        return "{" + ",".join("%s:%s" % (json.dumps(k), snbt(x)) for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    if isinstance(v, bool):
        return "1b" if v else "0b"
    if isinstance(v, float):
        return "%gf" % v
    if isinstance(v, int):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def give_item(iid, comps):
    return "%s[%s]" % (iid.replace("minecraft:", "", 1), ",".join("%s=%s" % (k.replace("minecraft:", ""), snbt(v)) for k, v in comps.items()))


def read(rel):
    return io.open(os.path.join(FUNC, rel), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel), "w", encoding="utf-8", newline="\n").write(s)


def patch(rel, guard, text, where="end"):
    s = read(rel)
    if guard in s:
        return
    if where == "end":
        s = s.rstrip("\n") + "\n" + text
    else:
        assert where in s, (rel, where)
        s = s.replace(where, text + where, 1)
    write(rel, s)


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def say(text, colour=None):
    return "tellraw @s " + J(["", seg("[炼药]", C_ALC, True), seg("　" + text, colour or ui.GRAY)])


def warn(text):
    return say(text, FO.T_WARN)


def dialog(title, body, actions, exit_label="取消", columns=2):
    doc = {"type": "minecraft:multi_action",
           "title": ["", seg("[炼药]" if "药" in title else "[制器]", C_ALC, True), seg(" " + title, FO.T_NAME)],
           "body": {"type": "minecraft:plain_message", "width": 300, "contents": [""] + body},
           "actions": [{"label": seg(l, c, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_fg_do set %d" % v}}
                       for l, c, v in actions],
           "columns": columns, "exit_action": {"label": seg(exit_label, FO.T_MUTED)},
           "can_close_with_escape": True, "pause": False, "after_action": "close"}
    return "dialog show @s " + J(doc)


def special(key):
    import add_world_items as WI
    return 'minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_%s"}]' % key, WI.SPECIAL[key][0]


# ============================================================================ 第一段：领取目录里的物品
def items():
    rel = "command/give/weapon.mcfunction"
    lines = read(rel).rstrip("\n").split("\n")
    out, done = [], set()
    for line in lines:
        hit = None
        if line.startswith("give ") and "potion[" in line[:40]:
            for k, p in S.POTIONS.items():
                if '"%s"' % p[0] in line:
                    hit = k
        if hit:
            iid, comps = S.potion_components(hit)
            out.append("give @a " + give_item(iid, comps))
            done.add(hit)
        else:
            out.append(line)
    assert len(done) == 8, done
    for k in S.POTIONS:
        if k not in done:
            iid, comps = S.potion_components(k)
            out.append("give @a " + give_item(iid, comps))
    out.append("give @a " + give_item("minecraft:paper", S.vial_components()))
    out.append("give @a " + give_item("minecraft:paper", S.blank_components()))
    write(rel, "\n".join(out) + "\n")
    print("alchemy items: 8 old potions rewritten, %d added" % (len(S.POTIONS) - 8 + 2))


# ============================================================================ 掉落表
def loot():
    def entry(iid, comps):
        comps = dict(comps)
        data = comps.pop("minecraft:custom_data")
        return {"type": "minecraft:item", "name": iid, "functions": [
            {"function": "minecraft:set_components", "components": comps},
            {"function": "minecraft:set_custom_data", "tag": snbt(data).replace('"rpg_potion"', "rpg_potion").replace('"rpg_fm"', "rpg_fm").replace('"rpg_mat"', "rpg_mat")}]}

    def table(name, entries):
        wj(os.path.join(LOOT, "potion", name + ".json"), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": entries}]})

    for k in S.POTIONS:
        table(k, [entry(*S.potion_components(k))])
    for tier in S.TIER:
        table("any_" + tier, [{"type": "minecraft:loot_table", "value": "rpg:potion/" + k} for k, p in S.POTIONS.items() if p[1] == tier])
    table("vial", [entry("minecraft:paper", S.vial_components())])
    table("blank_rite", [entry("minecraft:paper", S.blank_components())])


# ============================================================================ 页面
def recipes():
    """编号 → (名, 颜色, 材料谓词 [(谓词, 数, 名)], 要求, 成品命令, 主手谓词, 哪一页)"""
    out = []
    for k, (name, tier, use, _c, _e, _f, line, _fl, rec, sp) in S.POTIONS.items():
        tname, sef, souls, _st, _cd = S.TIER[tier]
        need = [("minecraft:%s[!minecraft:custom_data]" % i, n, S.item_name(i)) for i, n in rec]
        if souls:
            need.append((SOUL, souls, "残魂"))
        if sp:
            sel, spname = special(sp)
            need.append((sel, 1, spname))
        out.append((name, ui.tier_colour(tier), need, ("sef", sef), "loot give @s loot rpg:potion/" + k, VIAL, "potion", "[%s]" % tname, S.USE[use][1] + "：" + line))
    for k, (name, fun, rec, extra, req) in S.WATERS.items():
        need = [("minecraft:%s[!minecraft:custom_data]" % i, n, S.item_name(i)) for i, n in rec]
        if extra:
            need.append(extra)
        if k == "strong":
            sel, spname = special("bronze")
            need.append((sel, 1, spname))
        out.append((name, ui.HOLY, need, req, "function rpg:" + fun, VIAL, "potion", "[驱魔]", "点燃图腾用的圣水"))
    for k, (name, fun, rec, sp, req) in S.RITES.items():
        need = [("minecraft:%s[!minecraft:custom_data]" % i, n, S.item_name(i)) for i, n in rec]
        if sp:
            sel, spname = special(sp)
            need.append((sel, 1, spname))
        out.append((name, ui.HOLY, need, req, "function rpg:" + fun, BLANK, "rite", "[驱魔]", "驱魔器具"))
    return out


def pages():
    rec = recipes()
    assert len(rec) <= 49
    # 打开：对准灵魂火（沿用魂火冶炼的射线）
    for page, title, tip in (("potion", "炼药", "空瓶加遗物，炼出药水。选一种看配方："), ("rite", "制器", "空白圣具加遗物，做出驱魔器具。选一件看配方：")):
        acts = [(r[0], r[1], 200 + i) for i, r in enumerate(rec) if r[6] == page]
        fn("open_" + page, [
            "scoreboard players set #i rpg_fg 30",
            "scoreboard players set #found rpg_fg 0",
            "execute anchored eyes positioned ^ ^ ^ run function rpg:forge/smelt/ray",
            "execute if score #found rpg_fg matches 0 run return run " + warn("对准灵魂营火（或灵魂火）右键"),
            "scoreboard players set @s rpg_fg_op 10",
            "scoreboard players set @s rpg_fg_arg -1",
            dialog(title, [seg(tip, FO.T_BODY)], acts, columns=3)])
    do = ["# 200..248 选配方，250 动手（走 rpg:forge/smelt/do 的路由）",
          "execute if score #do rpg_fg matches 250 run return run function %s/make" % P,
          "scoreboard players operation @s rpg_fg_arg = #do rpg_fg",
          "scoreboard players remove @s rpg_fg_arg 200"]
    mk = ["# 再核对：靠近灵魂火、材料够，才扣",
          "scoreboard players operation #me rpg_fg = @s rpg_fg_id",
          "scoreboard players set #fire rpg_fg 0",
          "execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1",
          "execute if score #fire rpg_fg matches 0 run return run " + warn("离灵魂火太远了，靠近些")]
    for i, (name, col, need, req, out_cmd, hand, page, tag, line) in enumerate(rec):
        hand_name = "空瓶" if hand == VIAL else "空白圣具"
        body = [seg(tag, col, True), seg(name, FO.T_NAME, True), FO.NL, seg(line, FO.T_BODY), FO.NL, FO.NL,
                seg("消耗　", FO.T_MUTED), seg("%s ×1" % hand_name, FO.T_BODY), FO.NL]
        cnt = []
        for j, (sel, n, nm) in enumerate(need):
            cnt.append("execute store result storage rpg:alc d.a%d int 1 run clear @s %s 0" % (j, sel))
            body += [seg("　　　　%s ×%d" % (nm, n), FO.T_BODY), seg("　身上 $(a%d)" % j, FO.T_MUTED), FO.NL]
        rq = "原质第 %d 阶" % req[1] if req[0] == "sef" else "完成过 %d 次裁决" % req[1]
        body += [FO.NL, seg("要求　" + rq, FO.T_MUTED)]
        fn("show_%d" % i, cnt + ["data modify storage rpg:alc d.z set value 0", "function %s/show_%d_m with storage rpg:alc d" % (P, i)])
        fn("show_%d_m" % i, ["$" + dialog("炼药" if page == "potion" else "制器", body, [("动手", FO.T_HOLY, 250)], columns=1)])
        do.append("execute if score @s rpg_fg_arg matches %d run return run function %s/show_%d" % (i, P, i))
        score = "rpg_sef" if req[0] == "sef" else "rpg_ex_rites"
        chk = ["execute unless score @s %s matches %d.. run return run %s" % (score, req[1], warn("要%s才能做%s" % (rq, name))),
               "execute unless items entity @s weapon.mainhand %s run return run %s" % (hand, warn("主手要拿着" + hand_name))]
        for sel, n, nm in need:
            chk += ["execute store result score #c rpg_fg run clear @s %s 0" % sel,
                    "execute unless score #c rpg_fg matches %d.. run return run %s" % (n, warn("%s不够（要 %d）" % (nm, n)))]
        fn("make_%d" % i, ["# " + name] + chk + ["clear @s %s %d" % (sel, n) for sel, n, _nm in need] + [
            FO.CONSUME, out_cmd,
            "execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.25 0.4 0.25 0.04 40",
            "playsound minecraft:block.brewing_stand.brew player @s ~ ~ ~ 1 1" if page == "potion" else "playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 1.2",
            "scoreboard players add @s rpg_alc_made 1",
            "tellraw @s " + J(["", seg("[炼药]" if page == "potion" else "[制器]", C_ALC, True), seg("　做成：", ui.GRAY), seg(tag, col, True), seg(name, ui.WHITE)])])
        mk.append("execute if score @s rpg_fg_arg matches %d run return run function %s/make_%d" % (i, P, i))
    fn("do", do)
    fn("make", mk)
    patch("forge/use.mcfunction", "rpg:alc/open_potion",
          "execute if items entity @s weapon.mainhand %s run return run function rpg:alc/open_potion\n"
          "execute if items entity @s weapon.mainhand %s run return run function rpg:alc/open_rite\n" % (VIAL, BLANK),
          where="execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:\"blank\"}]")
    patch("forge/smelt/do.mcfunction", "rpg:alc/do",
          "execute if score #do rpg_fg matches 200..259 run return run function rpg:alc/do\n",
          where="execute if score #do rpg_fg matches 50..59")
    # 基础四件里没有单独 give 函数的：从领取目录抽行
    src = read("command/give/weapon.mcfunction") + read("command/give/item.mcfunction")
    for key, name in (("doll", "替死人偶"), ("star", "天启星"), ("totem", "驱魔图腾"), ("holy", "驱魔圣水")):
        line = next(l for l in src.split("\n") if l.startswith("give ") and "written_book" not in l[:30]
                    and re.search(r'"text":"%s"' % name, l[:400]))
        fn("give/" + key, [re.sub(r"^give @a", "give @s", line)])


# ============================================================================ 效果
NEG = ["poison", "wither", "slowness", "weakness", "blindness", "nausea", "hunger", "mining_fatigue", "darkness", "levitation", "unluck",
       "infested", "oozing", "weaving", "wind_charged"]


def effects():
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    fn("load", ["scoreboard objectives add rpg_alc_made dummy", "scoreboard objectives add rpg_alc dummy",
                "scoreboard objectives add rpg_po_sh dummy", "scoreboard objectives add rpg_po_bl dummy",
                "scoreboard objectives add rpg_po_ud dummy", "scoreboard objectives add rpg_po_lu dummy"])
    fn("tick", ["scoreboard players add #t rpg_alc 1",
                "execute if score #t rpg_alc matches 20.. run function %s/sec" % P])
    fn("sec", ["scoreboard players set #t rpg_alc 0",
               "scoreboard players remove @a[scores={rpg_po_sh=1..}] rpg_po_sh 1",
               "execute as @a[scores={rpg_po_sh=0}] run function %s/fx/shadow_off" % P,
               "scoreboard players remove @a[scores={rpg_po_bl=1..}] rpg_po_bl 1",
               "execute as @a[scores={rpg_po_bl=1..}] at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.01 4",
               "scoreboard players remove @a[scores={rpg_po_ud=1..}] rpg_po_ud 1",
               "execute as @a[scores={rpg_po_ud=1..}] at @s run particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.01 2",
               "scoreboard players remove @a[scores={rpg_po_lu=1..}] rpg_po_lu 1"])
    bodies = {
        "cleanse": ["effect clear @s minecraft:" + e for e in NEG] + ["particle minecraft:splash ~ ~1 ~ 0.3 0.6 0.3 0 30"],
        "shadow": ["attribute @s minecraft:attack_damage modifier remove rpg:po_shadow",
                   "attribute @s minecraft:attack_damage modifier add rpg:po_shadow 0.5 add_multiplied_total",
                   "scoreboard players set @s rpg_po_sh 15", "particle minecraft:smoke ~ ~1 ~ 0.4 0.8 0.4 0.01 40"],
        "blaze": ["scoreboard players set @s rpg_po_bl 15", "playsound minecraft:item.firecharge.use player @s ~ ~ ~ 1 0.8"],
        "exorcise": ["execute if score @s rpg_force matches 1 run scoreboard players remove @s rpg_assim 5",
                     "execute if score @s rpg_assim matches ..-1 run scoreboard players set @s rpg_assim 0",
                     "execute unless score @s rpg_force matches 1 run scoreboard players remove @s rpg_taint 15",
                     "execute if score @s rpg_taint matches ..-1 run scoreboard players set @s rpg_taint 0",
                     "particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.02 30"],
        "prayer": ["execute if score @s rpg_force matches 1 run scoreboard players add @s rpg_mana 40",
                   "execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana 40",
                   "execute if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max",
                   "execute if score @s rpg_force matches 1 run scoreboard players add @s rpg_vital 15",
                   "execute if score @s rpg_vital matches 101.. run scoreboard players set @s rpg_vital 100",
                   "execute unless score @s rpg_force matches 1 unless score @s rpg_force matches 3 run " + say("你没有圣力，只觉得嘴里有点甜。", FO.T_MUTED)],
        "rite": ["execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 50",
                 "execute if score @s rpg_force matches 2 if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max",
                 "execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 50",
                 "execute if score @s rpg_force matches 3 if score @s rpg_mana2 > @s rpg_mana_max run scoreboard players operation @s rpg_mana2 = @s rpg_mana_max",
                 "scoreboard players add @s rpg_taint 8",
                 "execute if score @s rpg_taint matches 101.. run scoreboard players set @s rpg_taint 100"],
        "undying": ["scoreboard players set @s rpg_po_ud 60", "playsound minecraft:item.totem.use player @s ~ ~ ~ 0.4 0.6"],
        "lure": ["scoreboard players set @s rpg_po_lu 60", "playsound minecraft:entity.warden.heartbeat player @s ~ ~ ~ 1 0.8"],
    }
    for k, p in S.POTIONS.items():
        if not p[5]:
            continue
        wj(os.path.join(DP, "data", "rpg", "advancement", "alc", k + ".json"), {
            "criteria": {"drink": {"trigger": "minecraft:consume_item", "conditions": {
                "item": {"predicates": {"minecraft:custom_data": '{rpg_potion:"%s"}' % k}}}}},
            "rewards": {"function": "%s/fx/%s" % (P, k)}})
        fn("fx/" + k, ["# " + p[0] + "：" + p[6], "advancement revoke @s only rpg:alc/" + k, "execute at @s run function %s/fx/%s_at" % (P, k)])
        fn("fx/%s_at" % k, bodies[p[5]])
    # 喝完手里会多出空瓶，右键还按着：借魂火界面的防抖锁挡住，松手才放开
    wj(os.path.join(DP, "data", "rpg", "advancement", "alc", "drank.json"), {
        "criteria": {"drink": {"trigger": "minecraft:consume_item", "conditions": {
            "item": {"items": "minecraft:potion"}}}},
        "rewards": {"function": P + "/drank"}})
    fn("drank", ["advancement revoke @s only rpg:alc/drank", "scoreboard players set @s rpg_fg_lk 10", "tag @s add rpg.fg.ui"])
    fn("fx/shadow_off", ["attribute @s minecraft:attack_damage modifier remove rpg:po_shadow", "scoreboard players reset @s rpg_po_sh"])
    # 打到人：影行现形、烈焰点燃
    wj(os.path.join(DP, "data", "rpg", "advancement", "alc", "hit.json"), {
        "criteria": {"hit": {"trigger": "minecraft:player_hurt_entity"}},
        "rewards": {"function": P + "/hit"}})
    fn("hit", ["advancement revoke @s only rpg:alc/hit",
               "execute if score @s rpg_po_sh matches 1.. run effect clear @s minecraft:invisibility",
               "execute if score @s rpg_po_sh matches 1.. run function %s/fx/shadow_off" % P,
               "execute if score @s rpg_po_bl matches 1.. at @s as @e[distance=0.1..6,type=!minecraft:player,type=!minecraft:item,type=!minecraft:item_display] "
               "if data entity @s {HurtTime:10s} run data merge entity @s {Fire:80s}"])
    # 不灭：挨打后血少就撑住（和「不死」同一种写法）
    patch("forge/hit/hurt_player.mcfunction", "rpg:alc/undying",
          "execute if score @s rpg_po_ud matches 1.. run function rpg:alc/undying\n")
    fn("undying", ["execute store result score #h rpg_alc run data get entity @s Health",
                   "execute unless score #h rpg_alc matches ..5 run return 0",
                   "scoreboard players set @s rpg_po_ud 0",
                   "effect give @s minecraft:resistance 3 2 true",
                   "effect give @s minecraft:regeneration 3 2 true",
                   "execute at @s run particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.05 40",
                   "playsound minecraft:item.totem.use player @s ~ ~ ~ 0.6 0.6",
                   say("不灭：你在致命的一击里撑住了。")])
    # 引潮：精英机率 ×3
    patch("elite/roll.mcfunction", "rpg_po_lu", "execute if entity @a[scores={rpg_po_lu=1..},distance=..48] run scoreboard players operation #p rpg_el *= #3 rpg_el\n",
          where="execute store result score #r rpg_el run random value 1..1000")


# ============================================================================ 来路
def sources():
    # 女巫 5% 勇者药水、30% 空瓶
    p = os.path.join(DP, "data", "minecraft", "loot_table", "entities", "witch.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    if "rpg:potion/" not in json.dumps(doc):
        for ref, ch in (("rpg:potion/any_brave", 0.05), ("rpg:potion/vial", 0.30)):
            doc["pools"].append({"rolls": 1, "conditions": [{"condition": "minecraft:killed_by_player"}, {"condition": "minecraft:random_chance", "chance": ch}],
                                 "entries": [{"type": "minecraft:loot_table", "value": ref}]})
        wj(p, doc)
    import world_loot_spec as W
    for g in W.GROUPS:
        patch("elite/kill/%s_champion.mcfunction" % g, "rpg:potion/any_epic",
              "execute if predicate {condition:\"minecraft:random_chance\",chance:0.1} run loot give @s loot rpg:potion/any_epic\n")
    patch("events/bt/all.mcfunction", "rpg:potion/any_epic", "loot give @s loot rpg:potion/any_epic\n")
    s = read("events/bt/all.mcfunction")
    write("events/bt/all.mcfunction", s.replace("今天的三条悬赏都完成了：铸造之石 ×1\"", "今天的三条悬赏都完成了：铸造之石 ×1、史诗药水 ×1\""))
    # 圣卫 30% 空白圣具；悬赏每条 10%
    for g in ("hg", "tg", "rg"):
        patch("world/kill_guard_%s.mcfunction" % g, "rpg:potion/blank_rite",
              "execute if predicate {condition:\"minecraft:random_chance\",chance:0.3} run loot give @s loot rpg:potion/blank_rite\n")
    patch("events/bt/reward.mcfunction", "rpg:potion/blank_rite",
          "execute if predicate {condition:\"minecraft:random_chance\",chance:0.1} run loot give @s loot rpg:potion/blank_rite\n")


def main():
    if "--items" in sys.argv:
        return items()
    import shutil
    shutil.rmtree(os.path.join(FUNC, "alc"), ignore_errors=True)
    shutil.rmtree(os.path.join(LOOT, "potion"), ignore_errors=True)
    loot()
    pages()
    effects()
    sources()
    print("alchemy: %d functions, %d potions, %d recipes" % (COUNT, len(S.POTIONS), len(recipes())))


if __name__ == "__main__":
    main()
