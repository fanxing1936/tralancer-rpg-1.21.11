# -*- coding: utf-8 -*-
"""精英怪（策划书第二步，用户 2026-11-23：出现率基础 3%、封顶 8%）。

    python add_elites.py ../rpg

* 自然生成、没有名字、没有任何本包标签、有 AI 的敌对生物，第一次被扫到时掷骰：
  千分之 30 + 5 × 附近玩家最高原质阶（封顶 80），夜里 ×1.5；48 格内已有 3 只精英就不再出。
  附近玩家原质 ≥ 6 时，五分之一的精英是首领（两条词缀）。
* 精英：生命 ×2.5、伤害 +30%、体型 ×1.15；首领：×5、+50%、×1.3，24 格内有一条共用的血条。
* 名牌：[词缀]+生物名（首领：[首领·词缀·词缀]），颜色取 rpg_ui_style；身上一圈对应颜色的粒子。
* 10 条词缀；命中类的走 rpg:forge/hit/hurt_player（玩家挨打 → on attacker 是精英）。
  圣印在 rpg:force/hit 里按 #tree 改伤害。
* 死亡（DeathTime 1）时按组掉精英表，杀手是玩家才掉；击杀进锻造的「精英」档（forge_spec.KILL_ELITE_TAGS 加了 rpg.el）。
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
import world_loot_spec as W
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function", "elite")
LOOT = os.path.join(DP, "data", "rpg", "loot_table", "elite")
P = "rpg:elite"
O = "rpg_el"
COUNT = 0

C_LEGEND = ui.tier_colour("legend")
C_FORGE = ui.mix(ui.HOLY_DARK, ui.WARN, 0.35)
# (编号, 名, 颜色, 一句说明)
AFFIX = [
    (1, "迅捷", ui.CYAN, "速度 II"),
    (2, "铁壁", ui.mix(ui.WHITE, ui.MUTED, 0.35), "护甲 +10、击退抗性"),
    (3, "狂怒", ui.WARN, "生命低于 40% 时力量 II"),
    (4, "吸血", ui.pillar("belial")["lit"], "命中回复生命"),
    (5, "寒霜", ui.CYAN_LIGHT, "命中附带缓慢 II"),
    (6, "剧毒", ui.READY, "命中附带中毒 II"),
    (7, "爆裂", ui.mix(ui.WARN, ui.HOLY, 0.5), "死后 2 秒原地爆开"),
    (8, "召唤", ui.BROADCAST_VOID, "半血时召来 2 只同类"),
    (9, "罪染", ui.mix(ui.BROADCAST_VOID, ui.WARN, 0.4), "命中让你魔化 +2"),
    (10, "圣印", ui.HOLY, "圣力对它 −50%，魔力对它 +30%"),
]
AF = {a[0]: a for a in AFFIX}
# 不出精英的：Boss 级、太小的、本来就是召唤物的
POOL = [m for m in W.WORLD_TABLES if m not in ("elder_guardian", "vex", "silverfish", "endermite")]
# 组 → 本组原料（第一个是「主原料」）、高一档原料
UPGRADE = {"undead": ("iron_ingot", "diamond"), "arthropod": ("iron_ingot", "diamond"),
           "explosive": ("iron_ingot", "diamond"), "arcane": ("iron_ingot", "diamond"),
           "nether": ("gold_ingot", "netherite_ingot"), "end": ("iron_ingot", "diamond"),
           "water": ("iron_ingot", "diamond")}
GROUP_OF = dict((m, g) for g, (_n, mobs, *_r) in W.GROUPS.items() for m in mobs)


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, name + ".mcfunction")
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


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def rgb(hexcol):
    h = hexcol.lstrip("#")
    return "[%.2f,%.2f,%.2f]" % tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ============================================================================ 物品：精英徽记
def badge_entry(lo, hi):
    return {"type": "minecraft:item", "name": "minecraft:paper", "functions": [
        {"function": "minecraft:set_components", "components": {
            "minecraft:custom_name": ["", seg("[货币]", ui.tier_colour("legend"), True), seg("精英徽记", ui.WHITE)],
            "minecraft:lore": [["", seg(ui.RULE_TEXT, ui.WHITE)],
                               ["", seg("打败精英怪的凭证", ui.GRAY)],
                               ["", seg("在商人和悬赏板处使用", ui.GRAY)],
                               ["", seg(ui.RULE_TEXT, ui.WHITE)]],
            "minecraft:item_model": "rpg:world/elite_badge",
            "minecraft:max_stack_size": 64}},
        {"function": "minecraft:set_custom_data", "tag": "{rpg_mat:\"elite_badge\"}"},
        {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi} if lo != hi else lo}]}


def raw_ref(item, lo, hi):
    """复用世界掉落表的原料格式（[锻造] 前缀）"""
    import add_world_loot as L
    return L.raw_entry(item, lo, hi)


def loot():
    def table(group, champ):
        main, up = UPGRADE[group]
        n_lo, n_hi, up_n, soul, blank, extra, rune, stone, badge = (
            (4, 6, 2, (3, 4), 0.6, 0.10, 0.10, 0.06, 3) if champ else (2, 4, 1, (1, 2), 0.2, 0.03, 0.03, 0.02, 1))
        pools = [
            {"rolls": 1, "entries": [raw_ref(main, n_lo, n_hi)]},
            {"rolls": 1, "entries": [raw_ref(up, up_n, up_n)]},
            {"rolls": {"type": "minecraft:uniform", "min": soul[0], "max": soul[1]},
             "entries": [{"type": "minecraft:loot_table", "value": "rpg:forge/item/soul"}]},
            {"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": blank}],
             "entries": [{"type": "minecraft:loot_table", "value": "rpg:forge/item/blank"}]},
        ]
        for k in ("forge_stone", "wash_gem", "gild_leaf"):
            pools.append({"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": extra}],
                          "entries": [{"type": "minecraft:loot_table", "value": "rpg:forge/item/" + k}]})
        pools.append({"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": rune}],
                      "entries": [{"type": "minecraft:loot_table", "value": "rpg:forge/rune_any"}]})
        pools.append({"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": stone}],
                      "entries": [{"type": "minecraft:loot_table", "value": "rpg:forge/stone_any"}]})
        pools.append({"rolls": 1, "entries": [badge_entry(badge, badge)]})
        return {"type": "minecraft:generic", "pools": pools}

    for g in W.GROUPS:
        wj(os.path.join(LOOT, "%s.json" % g), table(g, False))
        wj(os.path.join(LOOT, "%s_champion.json" % g), table(g, True))
    wj(os.path.join(LOOT, "badge.json"), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [badge_entry(1, 1)]}]})


# ============================================================================ 生成
def spawn():
    wj(os.path.join(DP, "data", "rpg", "tags", "entity_type", "elite_pool.json"),
       {"values": ["minecraft:" + m for m in POOL]})
    hook_tag(DP, "load", P + "/load", False)
    fn("load", ["scoreboard objectives add %s dummy" % o for o in (O, "rpg_el_a1", "rpg_el_a2", "rpg_el_kill", "rpg_el_t")] + [
        "scoreboard players set #2 %s 2" % O, "scoreboard players set #3 %s 3" % O,
        "scoreboard players set #5 %s 5" % O, "scoreboard players set #10 %s 10" % O,
        "scoreboard players set #100 %s 100" % O,
        "scoreboard players set #13 rpg_fo 13",
        "# 首领血条：和正式 Boss 同一套位图横幅（add_elite_bar_art.py）；原版粉色血条贴图是透明的。",
        "# 横幅、王冠与词缀图标、花体英文名合成一条，名字在横幅下方（与正式 Boss 的标题同位）",
        "bossbar remove rpg:elite_champion",
        "bossbar add rpg:elite_champion_bar \"\"",
        "bossbar set rpg:elite_champion_bar color pink",
    ])
    hook_tag(DP, "tick", P + "/tick", True)
    fn("tick", [
        "scoreboard players add #t %s 1" % O,
        "execute if score #t %s matches 10 run execute as @e[type=#rpg:elite_pool,tag=!rpg.el.seen] at @s run function %s/roll" % (O, P),
        "execute as @e[type=minecraft:item_display,tag=rpg.el.bomb] at @s run function %s/a/7/check" % P,
        "execute if score #t %s matches 20.. run function %s/sec" % (O, P),
    ])
    fn("roll", [
        "# 第一次见到这只生物（as/at 它）",
        "tag @s add rpg.el.seen",
        "execute if data entity @s CustomName run return 0",
        "execute if data entity @s {NoAI:1b} run return 0",
        "# 本包召唤的生物都带标签；掉落策略那一枚不算",
        "execute store result score #nt %s run data get entity @s Tags" % O,
        "scoreboard players remove #nt %s 1" % O,
        "execute if entity @s[tag=rpg.drop_policy.v1] run scoreboard players remove #nt %s 1" % O,
        "execute if score #nt %s matches 1.. run return 0" % O,
        "execute unless entity @a[distance=..64,gamemode=!spectator] run return 0",
        "execute store result score #near %s if entity @e[tag=rpg.el,distance=..48]" % O,
        "execute if score #near %s matches 3.. run return 0" % O,
        "# 千分之 30 + 5 × 原质阶，封顶 80；夜里 ×1.5",
        "scoreboard players set #sef %s 0" % O,
        "execute as @a[distance=..64] if score @s rpg_sef > #sef %s run scoreboard players operation #sef %s = @s rpg_sef" % (O, O),
        "scoreboard players operation #p %s = #sef %s" % (O, O),
        "scoreboard players operation #p %s *= #5 %s" % (O, O),
        "scoreboard players add #p %s 30" % O,
        "execute if score #p %s matches 81.. run scoreboard players set #p %s 80" % (O, O),
        "execute store result score #day %s run time query daytime" % O,
        "execute if score #day %s matches 13000..23000 run scoreboard players operation #p %s *= #3 %s" % (O, O, O),
        "execute if score #day %s matches 13000..23000 run scoreboard players operation #p %s /= #2 %s" % (O, O, O),
        "execute store result score #r %s run random value 1..1000" % O,
        "execute if score #r %s > #p %s run return 0" % (O, O),
        "function %s/make" % P,
    ])
    # 掷词缀、首领
    mk = ["# 变成精英（as/at 它）",
          "tag @s add rpg.el",
          "execute store result score @s rpg_el_a1 run random value 1..10",
          "scoreboard players set @s rpg_el_a2 0",
          "execute if score #sef %s matches 6.. store result score #c %s run random value 1..5" % (O, O),
          "execute if score #sef %s matches 6.. if score #c %s matches 1 run function %s/champion" % (O, O, P),
          "function %s/stats" % P,
          "function %s/type" % P,
          "function %s/name_pick" % P]
    for k in AF:
        mk.append("execute if score @s rpg_el_a1 matches %d run function %s/a/%d/on" % (k, P, k))
        mk.append("execute if score @s rpg_el_a2 matches %d run function %s/a/%d/on" % (k, P, k))
    fn("make", mk)
    fn("champion", ["tag @s add rpg.el.boss",
                    "execute store result score @s rpg_el_a2 run random value 1..9",
                    "execute if score @s rpg_el_a2 >= @s rpg_el_a1 run scoreboard players add @s rpg_el_a2 1"])
    fn("stats", [
        "attribute @s minecraft:max_health modifier add rpg:elite_hp 1.5 add_multiplied_base",
        "attribute @s[tag=rpg.el.boss] minecraft:max_health modifier add rpg:elite_hp2 2.5 add_multiplied_base",
        "attribute @s minecraft:attack_damage modifier add rpg:elite_dmg 0.3 add_multiplied_base",
        "attribute @s[tag=rpg.el.boss] minecraft:attack_damage modifier add rpg:elite_dmg2 0.2 add_multiplied_base",
        "attribute @s minecraft:scale modifier add rpg:elite_scale 0.15 add_multiplied_base",
        "attribute @s[tag=rpg.el.boss] minecraft:scale modifier add rpg:elite_scale2 0.15 add_multiplied_base",
        "data modify entity @s Health set value 2048f",
        "data modify entity @s PersistenceRequired set value 1b",
    ])
    import add_elite_bar_art as BA
    t = ["# 生物种类 → 花体英文名、召唤用的 id、血条上的名字字形与居中退格（storage rpg:elite t）"]
    for m in POOL:
        t.append("execute if entity @s[type=minecraft:%s] run data modify storage rpg:elite t set value {id:\"%s\",nm:\"%s\",g:\"%s\",bn:\"%s\",bb:\"%s\",bo:\"%s\"}"
                 % (m, m, ui.fraktur(W.MOB_EN[m]), GROUP_OF[m], BA.name_char(m), BA.back_char(m), BA.on_char(m)))
    fn("type", t)
    # 名牌：词缀图标（Codex 交付后，字体 rpg:world_affix）或文字前缀，+ 生物名
    import add_world_art as WA
    icons = WA.affix_icons_ready()
    name = ["# 名牌（as 精英，storage t 已有 key）"]
    for k, nm, col, _d in AFFIX:
        v1 = WA.AFFIX_CHARS[k] if icons else nm
        name.append("execute if score @s rpg_el_a1 matches %d run data merge storage rpg:elite {t:{n1:\"%s\",c1:\"%s\"}}" % (k, v1, col))
        name.append("execute if score @s rpg_el_a2 matches %d run data merge storage rpg:elite {t:{n2:\"%s\",c2:\"%s\"}}" % (k, v1, col))
    name += ["execute unless entity @s[tag=rpg.el.boss] run return run function %s/name1 with storage rpg:elite t" % P,
             "function %s/name2 with storage rpg:elite t" % P]
    fn("name_pick", name)
    tail = "{\"text\":\"$(nm)\",\"color\":\"%s\",\"bold\":false,\"italic\":false}]" % ui.WHITE
    if icons:
        g = lambda v: "{\"text\":\"%s\",\"font\":\"rpg:world_affix\",\"color\":\"%s\",\"italic\":false}," % (v, ui.WHITE)
        gap = g("\uE6AF")
        fn("name1", ["$data modify entity @s CustomName set value [\"\"," + g("$(n1)") + gap + tail,
                     "data modify entity @s CustomNameVisible set value 1b"])
        fn("name2", ["$data modify entity @s CustomName set value [\"\"," + g(WA.AFFIX_CHARS[0]) + g("$(n1)") + g("$(n2)") + gap + tail,
                     "data modify entity @s CustomNameVisible set value 1b"])
    else:
        fn("name1", ["$data modify entity @s CustomName set value [\"\",{\"text\":\"[$(n1)]\",\"color\":\"$(c1)\",\"bold\":true,\"italic\":false}," + tail,
                     "data modify entity @s CustomNameVisible set value 1b"])
        fn("name2", ["$data modify entity @s CustomName set value [\"\",{\"text\":\"[首领·\",\"color\":\"%s\",\"bold\":true,\"italic\":false},"
                     "{\"text\":\"$(n1)\",\"color\":\"$(c1)\",\"bold\":true,\"italic\":false},"
                     "{\"text\":\"·\",\"color\":\"%s\",\"bold\":true,\"italic\":false},"
                     "{\"text\":\"$(n2)\",\"color\":\"$(c2)\",\"bold\":true,\"italic\":false},"
                     "{\"text\":\"]\",\"color\":\"%s\",\"bold\":true,\"italic\":false}," % (C_LEGEND, C_LEGEND, C_LEGEND) + tail,
                     "data modify entity @s CustomNameVisible set value 1b"])


# ============================================================================ 每秒：光环、狂怒、召唤、首领血条
def per_second():
    sec = ["scoreboard players set #t %s 0" % O,
           "bossbar set rpg:elite_champion_bar players",
           "execute as @e[tag=rpg.el] at @s run function %s/each" % P]
    fn("sec", sec)
    each = ["# 每只精英每秒（as/at）"]
    for k, nm, col, _d in AFFIX:
        each.append("execute if score @s rpg_el_a1 matches %d run particle minecraft:dust{color:%s,scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4" % (k, rgb(col)))
        each.append("execute if score @s rpg_el_a2 matches %d run particle minecraft:dust{color:%s,scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3" % (k, rgb(col)))
    each += [
        "execute if entity @s[scores={rpg_el_a1=3}] run function %s/a/3/sec" % P,
        "execute if entity @s[scores={rpg_el_a2=3}] run function %s/a/3/sec" % P,
        "execute if entity @s[scores={rpg_el_a1=8}] run function %s/a/8/sec" % P,
        "execute if entity @s[scores={rpg_el_a2=8}] run function %s/a/8/sec" % P,
        "execute if entity @s[tag=rpg.el.boss] if entity @a[distance=..24] run function %s/bar" % P,
    ]
    fn("each", each)
    import add_elite_bar_art as BA
    bar = ["# 首领血条（as/at 首领，24 格内有玩家）：横幅第几档 + 图标 + 名字 → 一条",
           "execute store result score #h %s run data get entity @s Health %d" % (O, BA.STEPS),
           "execute store result score #mh %s run attribute @s minecraft:max_health get" % O,
           "scoreboard players operation #h %s /= #mh %s" % (O, O),
           "function %s/type" % P]
    for k in range(BA.STEPS + 1):
        bar.append("execute if score #h %s matches %d run data modify storage rpg:elite t.st set value \"%s\"" % (O, k, BA.char(k)))
    for k in range(1, 11):
        bar.append("execute if score @s rpg_el_a1 matches %d run data modify storage rpg:elite t.i1 set value \"%s\"" % (k, BA.icon(k)))
        bar.append("execute if score @s rpg_el_a2 matches %d run data modify storage rpg:elite t.i2 set value \"%s\"" % (k, BA.icon(k)))
    bar += ["function %s/bar_set with storage rpg:elite t" % P,
            "bossbar set rpg:elite_champion_bar players @a[distance=..24]"]
    fn("bar", bar)
    fn("bar_set", ["$bossbar set rpg:elite_champion_bar name {\"text\":\"$(st)$(bb)%s$(i1)$(i2)%s$(bn)$(bo)\",\"font\":\"%s\",\"color\":\"white\"}"
                   % (BA.icon(0), BA.GAP, BA.FONT)])


# ============================================================================ 词缀
def affixes():
    fn("a/1/on", ["effect give @s minecraft:speed infinite 1 true"])
    fn("a/2/on", ["attribute @s minecraft:armor modifier add rpg:elite_armor 10 add_value",
                  "attribute @s minecraft:knockback_resistance modifier add rpg:elite_kb 0.6 add_value"])
    fn("a/3/on", [])
    fn("a/3/sec", ["execute store result score #h %s run data get entity @s Health 10" % O,
                   "execute store result score #mh %s run attribute @s minecraft:max_health get 4" % O,
                   "execute if score #h %s <= #mh %s run effect give @s minecraft:strength 2 1 true" % (O, O)])
    for k in (4, 5, 6, 9):
        fn("a/%d/on" % k, [])
    fn("a/10/on", ["tag @s add rpg.el.h"])
    fn("a/8/on", [])
    fn("a/8/sec", ["execute if entity @s[tag=rpg.el.called] run return 0",
                   "execute store result score #h %s run data get entity @s Health 10" % O,
                   "execute store result score #mh %s run attribute @s minecraft:max_health get 5" % O,
                   "execute if score #h %s > #mh %s run return 0" % (O, O),
                   "tag @s add rpg.el.called",
                   "function %s/type" % P,
                   "function %s/a/8/call with storage rpg:elite t" % P,
                   "function %s/a/8/call with storage rpg:elite t" % P,
                   "playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..24] ~ ~ ~ 1 1",
                   "particle minecraft:dust{color:%s,scale:1.4} ~ ~1 ~ 1 0.6 1 0 30" % rgb(AF[8][2])])
    fn("a/8/call", ["$summon minecraft:$(id) ~ ~ ~ {Tags:[\"rpg.el.seen\",\"rpg.el.minion\"]}"])
    # 命中：rpg:forge/hit/hurt_player（as 挨打的玩家）→ on attacker 是精英
    fn("hit", ["# as 挨打的玩家",
               "tag @s add rpg.el.vic",
               "execute on attacker if entity @s[tag=rpg.el] run function %s/hit_by" % P,
               "tag @s remove rpg.el.vic"])
    fn("hit_by", ["# as 打人的精英"] +
       ["execute if score @s rpg_el_a1 matches %d run function %s/a/%d/hit" % (k, P, k) for k in (4, 5, 6, 9)] +
       ["execute if score @s rpg_el_a2 matches %d run function %s/a/%d/hit" % (k, P, k) for k in (4, 5, 6, 9)])
    fn("a/4/hit", ["execute store result score #h %s run data get entity @s Health 10" % O,
                   "scoreboard players add #h %s 40" % O,
                   "execute store result entity @s Health float 0.1 run scoreboard players get #h %s" % O,
                   "particle minecraft:damage_indicator ~ ~1.5 ~ 0.3 0.3 0.3 0 4"])
    fn("a/5/hit", ["effect give @a[tag=rpg.el.vic] minecraft:slowness 2 1"])
    fn("a/6/hit", ["effect give @a[tag=rpg.el.vic] minecraft:poison 3 1"])
    fn("a/9/hit", ["scoreboard players add @a[tag=rpg.el.vic] rpg_taint 2"])
    # 爆裂：死后 2 秒
    fn("a/7/boom", ["# as/at 掉在原地的爆裂标记",
                    "scoreboard players add @s rpg_el_t 1",
                    "execute if score @s rpg_el_t matches ..19 run return run particle minecraft:dust{color:%s,scale:1.2} ~ ~0.5 ~ 0.6 0.3 0.6 0 4" % rgb(AF[7][2]),
                    "particle minecraft:explosion ~ ~0.5 ~ 1 0.5 1 0 6",
                    "playsound minecraft:entity.generic.explode hostile @a[distance=..24] ~ ~ ~ 1 1",
                    "execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:explosion",
                    "kill @s"])


# ============================================================================ 死亡
def death():
    """死掉的实体不会被 @e 选中，所以击杀走「玩家击杀实体」进度：按组、按是否首领各一个，奖励直接给击杀者。"""
    adv = os.path.join(DP, "data", "rpg", "advancement", "elite")
    for g in W.GROUPS:
        wj(os.path.join(DP, "data", "rpg", "tags", "entity_type", "elite_%s.json" % g),
           {"values": ["minecraft:" + m for m in POOL if GROUP_OF[m] == g]})
        for champ in (False, True):
            key = "%s%s" % (g, "_champion" if champ else "")
            cond = [{"condition": "minecraft:entity_properties", "entity": "this",
                     "predicate": {"type": "#rpg:elite_%s" % g, "nbt": "{Tags:[\"rpg.el\"]}"}}]
            boss = {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.el.boss\"]}"}}
            cond.append(boss if champ else {"condition": "minecraft:inverted", "term": boss})
            wj(os.path.join(adv, "kill_%s.json" % key), {
                "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": cond}}},
                "rewards": {"function": "%s/kill/%s" % (P, key)}})
            fn("kill/%s" % key, [
                "# 玩家打死了%s精英（as/at 玩家）" % ("首领" if champ else ""),
                "advancement revoke @s only rpg:elite/kill_%s" % key,
                "loot give @s loot rpg:elite/%s" % key,
                "scoreboard players add @s rpg_el_kill 1",
            ] + (["scoreboard players add @s rpg_ex_xp 15",
                  "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.4"] if champ else []) + [
                "playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.6"])
    # 爆裂：头上挂一个看不见的展示实体；精英死了它掉在原地，2 秒后炸开
    fn("a/7/on", ["summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.el.bomb\",\"rpg.el.bnew\"]}",
                  "ride @e[tag=rpg.el.bnew,limit=1] mount @s",
                  "tag @e[tag=rpg.el.bnew] remove rpg.el.bnew"])
    fn("a/7/check", ["# as/at 爆裂标记（每刻）：身下的精英还在就不动",
                     "execute on vehicle run return 0",
                     "function %s/a/7/boom" % P])


# ============================================================================ 接线
def wire():
    F = os.path.join(DP, "data", "rpg", "function")

    def patch(rel, guard, text, where="end"):
        p = os.path.join(F, rel)
        s = io.open(p, encoding="utf-8").read()
        if guard in s:
            return
        if where == "end":
            s = s.rstrip("\n") + "\n" + text
        else:
            assert where in s, (rel, where)
            s = s.replace(where, text + where, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)

    patch("forge/hit/hurt_player.mcfunction", P + "/hit", "function %s/hit\n" % P)
    # 圣印：圣力技能 −50%、魔力技能 +30%（rpg:force/hit，as 目标，#tree 是这次施放的树）
    patch("force/hit.mcfunction", "rpg.el.h", (
        "execute if entity @s[tag=rpg.el.h] if score #tree rpg_fo matches 1 run scoreboard players operation #d rpg_fo /= #2 rpg_fo\n"
        "execute if entity @s[tag=rpg.el.h] if score #tree rpg_fo matches 2 run scoreboard players operation #d rpg_fo *= #13 rpg_fo\n"
        "execute if entity @s[tag=rpg.el.h] if score #tree rpg_fo matches 2 run scoreboard players operation #d rpg_fo /= #10 rpg_fo\n"),
          "execute store result storage rpg:force h.d")


def validate():
    for g in W.GROUPS:
        assert os.path.exists(os.path.join(LOOT, "%s_champion.json" % g))
    assert len(AFFIX) == 10


def main():
    import shutil
    shutil.rmtree(FUNC, ignore_errors=True)
    loot()
    spawn()
    per_second()
    affixes()
    death()
    wire()
    validate()
    print("elites: %d functions, %d affixes, %d mob types" % (COUNT, len(AFFIX), len(POOL)))


if __name__ == "__main__":
    main()
