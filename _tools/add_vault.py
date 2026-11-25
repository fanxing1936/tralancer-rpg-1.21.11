# -*- coding: utf-8 -*-
"""宝库抽奖重写（用户 2026-11-25：「宝库抽奖得重写，里面都是旧的东西，而且一开始的表现方式不够好」）。

    python add_vault.py ../rpg          （在 add_paradise 之后）

* 钥匙与锁、触发沿用原来的：宝库吐出 loot_trigger 下界之星（rpg:loot/loot*），这里接手。
* 普通宝库：八件奖品绕着宝库转，越转越慢，停在开箱人面前的就是结果；亮出品级与名字，再落下来。
* 灾厄宝库：十把封着的钥匙一圈，逐件揭开，最后一件必是史诗以上、飞到中间。
* 四档：勇者、史诗、传说、限定。保底：连续 9 次没有史诗则下一次必出，连续 39 次没有传说则下一次必出。
* 亮出来的就是给的：奖品在开始时就放进展示实体，落地时原样取出，归开箱人捡。
"""
import io
import json
import os
import re
import sys

import add_paradise as PL
import make_boxes as B
import rpg_ui_style as ui
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
P = "rpg:vault"
O = "rpg_vt"
TIERS = {1: ("勇者", ui.tier_colour("brave"), "Brave"), 2: ("史诗", ui.tier_colour("epic"), "Epic"),
         3: ("传说", ui.tier_colour("legend"), "Legend"), 4: ("限定", ui.tier_colour("limited"), "Limited")}
ODDS = [(4, 8), (3, 100), (2, 330)]              # 千分比，其余勇者
ODDS_LAST = [(4, 25), (3, 225)]                  # 灾厄最后一件，其余史诗
PITY = {2: 9, 3: 39}
SPIN, HOLD = 72, 46                              # 普通宝库：转的刻数、亮出来停的刻数
RADIUS = 1.25


def ref(t, w, n=None):
    e = {"type": "minecraft:loot_table", "value": t, "weight": w}
    if n:
        e["functions"] = [{"function": "minecraft:set_count", "count": n if isinstance(n, int) else {"type": "minecraft:uniform", "min": n[0], "max": n[1]}}]
    return e


POOL = {
    1: [ref("rpg:world/currency", 14, (8, 14)), ref("rpg:forge/item/forge_stone", 10, (2, 3)), ref("rpg:forge/item/wash_gem", 8, 2), ref("rpg:forge/item/gild_leaf", 6, 2),
        ref("rpg:forge/item/soul", 12, (8, 12)), ref("rpg:paradise/relic_any", 14, (8, 12)), ref("rpg:potion/any_brave", 12, 2), ref("rpg:paradise/mud", 6, 3), ref("rpg:elite/badge", 8, 2)],
    2: [ref("rpg:paradise/sp_any", 14, (1, 2)), ref("rpg:forge/rune_any", 12), ref("rpg:potion/any_epic", 10, (1, 2)), ref("rpg:world/bp_fragment", 12, (2, 3)), ref("rpg:elite/badge", 8, (5, 7)),
        ref("rpg:paradise/feather", 8, 2), ref("rpg:paradise/fruit", 8), ref("rpg:forge/item/blank", 6, 2), ref("rpg:potion/blank_rite", 6, 2), ref("rpg:trial/key", 5)],
    3: [ref("rpg:world/bp_epic_any", 12), ref("rpg:forge/stone_any", 10), ref("rpg:potion/any_legend", 8), ref("rpg:world/bp_fragment", 8, 6), ref("rpg:paradise/sp_any", 8, 4),
        ref("rpg:trial/ominous_key", 4)] + [ref("rpg:world/sin_shard_%d" % k, 1, 4) for k in range(1, 8)],
    4: [ref("rpg:world/bp_legend_any", 7)] + [ref("rpg:forge/item/source_%s" % k, 1) for k in ("faith", "hope", "resolve", "malice", "hatred", "pride")],
}


def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def rgb(h):
    return "[%s]" % ",".join("%.2f" % (int(h[i:i + 2], 16) / 255.0) for i in (1, 3, 5))


def num(h):
    return int(h[1:], 16)


def fn(name, lines):
    path = os.path.join(FUNC, "vault", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def sakura():
    """「樱怒之日」现行的那件：从 give/weapon 里取，改成 item replace。"""
    for l in io.open(os.path.join(FUNC, "command", "give", "weapon.mcfunction"), encoding="utf-8"):
        l = l.strip()
        if "樱怒之日" in l and l.startswith("give "):
            m = re.match(r"give \S+ (.*?)(?:\s+\d+)?$", l)
            return "item replace entity @s contents with " + m.group(1)
    raise SystemExit("vault: give/weapon 里没有樱怒之日")


def T(tr, sc, rot="0f,0f,0f,1f"):
    return "transformation:{translation:[%.3ff,%.3ff,%.3ff],scale:[%.3ff,%.3ff,%.3ff],left_rotation:[%s],right_rotation:[0f,0f,0f,1f]}" % (tr + (sc, sc, sc) + (rot,))


def grow(tr, sc, dur):
    return "data merge entity @s {start_interpolation:0,interpolation_duration:%d,%s}" % (dur, T(tr, sc))


def lock(omen):
    """演出时的宝库：不感应，插不进钥匙。"""
    s = PL.vault_nbt(omen)
    return s[:-2] + ",activation_range:0.0d,deactivation_range:0.0d}}"


def main():
    for t, ents in POOL.items():
        PL.wj(os.path.join(DP, "data", "rpg", "loot_table", "vault", "t%d.json" % t), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": ents}]})
    PL.wj(os.path.join(DP, "data", "rpg", "loot_table", "vault", "decoy.json"), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [
        {"type": "minecraft:loot_table", "value": "rpg:vault/t%d" % t, "weight": w} for t, w in ((1, 40), (2, 35), (3, 20), (4, 5))]}]})
    hook_tag(DP, "load", P + "/load", False)
    fn("load", ["scoreboard objectives add %s dummy" % o for o in (O, O + "_id", O + "_t", O + "_q", O + "_k", O + "_m", O + "_e", O + "_l", O + "_n")])
    # 入口：原来的每刻函数整个换掉
    with io.open(os.path.join(FUNC, "loot", "loot.mcfunction"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(["# 宝库：钥匙开出触发星，这里接手（add_vault.py）",
                            "execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s align xyz positioned ~0.5 ~-1 ~0.5 run function %s/open" % P,
                            "execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s align xyz positioned ~0.5 ~-1 ~0.5 run function %s/open_om" % P,
                            "execute as @e[type=minecraft:marker,tag=rpg.vt.c] at @s run function %s/step" % P]) + "\n")
    for f in ("trigger", "trigger_ominous", "loot/g0", "loot/g1"):
        p = os.path.join(FUNC, "loot", f + ".mcfunction")
        if os.path.exists(p):
            os.remove(p)
    for omen in (False, True):
        n = 10 if omen else 8
        name = "open_om" if omen else "open"
        fn(name, ["# 开%s宝库（as 触发星，at 宝库底面中心）" % ("灾厄" if omen else "试炼"),
                  "kill @s",
                  "# 不在宝库旁边（被人捡走又丢出来之类）：直接给一份勇者奖",
                  "execute unless block ~ ~ ~ minecraft:vault run return run loot spawn ~ ~1 ~ loot rpg:vault/t1",
                  "setblock ~ ~ ~ minecraft:air", "setblock ~ ~ ~ " + lock(omen),
                  "scoreboard players add #id %s 1" % O,
                  "tag @a remove rpg.vt.op", "tag @p[distance=..8,gamemode=!spectator] add rpg.vt.op",
                  "scoreboard players operation @a[tag=rpg.vt.op] %s_id = #id %s" % (O, O),
                  'summon minecraft:marker ~ ~1.55 ~ {Tags:["rpg.vt.c","rpg.vt.new"]}',
                  "execute as @e[type=minecraft:marker,tag=rpg.vt.new] at @s run function %s/begin_%d" % (P, omen)])
        beg = ["scoreboard players operation @s %s_id = #id %s" % (O, O), "scoreboard players set @s %s_t 0" % O, "scoreboard players set @s %s_m %d" % (O, omen),
               "data modify entity @s data.owner set from entity @a[tag=rpg.vt.op,limit=1] UUID",
               "execute facing entity @p[tag=rpg.vt.op] feet run rotate @s ~ 0",
               "tag @s remove rpg.vt.new"]
        for k in range(n):
            beg.append('summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},%s}' % T((0.0, 0.0, RADIUS + 0.35 * omen), 0.01))
            beg.append("execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function %s/slot_%d_%d" % (P, omen, k))
        beg += ["playsound minecraft:block.vault.open_shutter block @a[distance=..20] ~ ~ ~ 1 %s" % ("0.6" if omen else "0.9"),
                "playsound minecraft:block.beacon.activate block @a[distance=..20] ~ ~ ~ 0.7 %s" % ("0.7" if omen else "1.3"),
                "particle minecraft:trial_spawner_detection%s ~ ~-0.8 ~ 0.5 0.2 0.5 0.05 30" % ("_ominous" if omen else "")]
        fn("begin_%d" % omen, beg)
        for k in range(n):
            fn("slot_%d_%d" % (omen, k), ["tag @s remove rpg.vt.new", "scoreboard players operation @s %s_id = #id %s" % (O, O), "scoreboard players set @s %s_k %d" % (O, k),
                                          "rotate @s ~%d 0" % (k * 360 // n)] +
               (["loot replace entity @s contents loot rpg:trial/ominous_key"] if omen else
                ["scoreboard players operation #c %s = #id %s" % (O, O), "function %s/roll" % P] if k == 0 else ["loot replace entity @s contents loot rpg:vault/decoy"]))
    # ------------------------------------------------------------------ 抽
    fn("roll", ["# 抽一件放进自己（as 展示实体；#c = 场次，#mn = 2 时是灾厄最后一件）",
                "tag @a remove rpg.vt.op", "execute as @a if score @s %s_id = #c %s run tag @s add rpg.vt.op" % (O, O),
                "scoreboard players add @a[tag=rpg.vt.op] %s_e 0" % O, "scoreboard players add @a[tag=rpg.vt.op] %s_l 0" % O,
                "scoreboard players set #e %s 0" % O, "scoreboard players set #l %s 0" % O,
                "execute as @a[tag=rpg.vt.op,limit=1] run scoreboard players operation #e %s = @s %s_e" % (O, O),
                "execute as @a[tag=rpg.vt.op,limit=1] run scoreboard players operation #l %s = @s %s_l" % (O, O),
                "execute store result score #r %s run random value 1..1000" % O,
                "scoreboard players set #q %s 1" % O] +
       odds(ODDS, "unless score #mn %s matches 2 " % O) +
       ["execute if score #mn %s matches 2 run scoreboard players set #q %s 2" % (O, O)] + odds(ODDS_LAST, "if score #mn %s matches 2 " % O) +
       ["execute if score #e %s matches %d.. if score #q %s matches ..1 run scoreboard players set #q %s 2" % (O, PITY[2], O, O),
        "execute if score #l %s matches %d.. if score #q %s matches ..2 run scoreboard players set #q %s 3" % (O, PITY[3], O, O),
        "scoreboard players set #mn %s 0" % O,
        "scoreboard players add @a[tag=rpg.vt.op] %s_n 1" % O,
        "scoreboard players add @a[tag=rpg.vt.op] %s_e 1" % O, "scoreboard players add @a[tag=rpg.vt.op] %s_l 1" % O,
        "execute if score #q %s matches 2.. run scoreboard players set @a[tag=rpg.vt.op] %s_e 0" % (O, O),
        "execute if score #q %s matches 3.. run scoreboard players set @a[tag=rpg.vt.op] %s_l 0" % (O, O),
        "scoreboard players operation @s %s_q = #q %s" % (O, O)] +
       ["execute if score #q %s matches %d run loot replace entity @s contents loot rpg:vault/t%d" % (O, t, t) for t in POOL] +
       ["execute if score #q %s matches 4 store result score #r %s run random value 1..20" % (O, O),
        "execute if score #q %s matches 4 if score #r %s matches 1 run function %s/sakura" % (O, O, P)])
    fn("sakura", ["# 只在这里的那一件", sakura()])
    # ------------------------------------------------------------------ 每刻
    fn("step", ["scoreboard players add @s %s_t 1" % O, "scoreboard players operation #c %s = @s %s_id" % (O, O),
                "execute as @e[type=minecraft:item_display,tag=rpg.vt.i,distance=..6] if score @s %s_id = #c %s run tag @s add rpg.vt.me" % (O, O),
                "execute if score @s %s_m matches 0 run function %s/n" % (O, P), "execute if score @s %s_m matches 1 run function %s/o" % (O, P),
                "tag @e[tag=rpg.vt.me,distance=..8] remove rpg.vt.me"])
    ME = "@e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6"
    t_ = "execute if score @s %s_t matches " % O
    # 普通：转盘
    n = [t_ + "3 as %s] run %s" % (ME, grow((0.0, 0.0, RADIUS), 0.52, 8))]
    total, prev, last = 1440.0, 0.0, 0
    for i in range(1, SPIN + 1):
        a = total * (1 - (1 - i / float(SPIN)) ** 3)
        n.append(t_ + "%d as %s] at @s run rotate @s ~%.2f ~" % (i + 6, ME, a - prev))
        c = int((a + 22.5) // 45)
        if c != last:
            n.append(t_ + "%d run playsound minecraft:block.note_block.hat block @a[distance=..16] ~ ~ ~ 0.7 %.2f" % (i + 6, 0.7 + 0.8 * i / SPIN))
            last = c
        prev = a
    n += [t_ + "..%d run particle minecraft:dust{color:[0.85,0.62,0.28],scale:0.7} ~ ~-0.45 ~ 0.9 0.05 0.9 0 3" % (SPIN + 6),
          t_ + "%d run function %s/reveal" % (SPIN + 8, P),
          t_ + "%d as %s,scores={%s_k=1..}] run kill @s" % (SPIN + 18, ME, O),
          t_ + "%d..%d as %s] at @s run rotate @s ~5 ~" % (SPIN + 18, SPIN + 8 + HOLD, ME),
          t_ + "%d.. run function %s/finish" % (SPIN + 8 + HOLD, P)]
    fn("n", n)
    fn("reveal", ["# 停在开箱人面前的那件亮出来"] +
       ["execute as %s,scores={%s_k=1..}] run %s" % (ME, O, grow((0.0, 0.0, RADIUS), 0.0, 6)),
        "execute as %s,scores={%s_k=0}] run %s" % (ME, O, grow((0.0, 0.45, 0.0), 1.0, 8)),
        "scoreboard players operation #q %s = %s,scores={%s_k=0},limit=1] %s_q" % (O, ME, O, O),
        "data modify storage rpg:vault i set from entity %s,scores={%s_k=0},limit=1] item" % (ME, O),
        "function %s/show" % P])
    # 灾厄：十把封着的钥匙逐件揭开
    o = [t_ + "3 as %s] run %s" % (ME, grow((0.0, 0.0, RADIUS + 0.35), 0.44, 8)),
         t_ + "..30 as %s] at @s run rotate @s ~6 ~" % ME, t_ + "31.. as %s,scores={%s_k=..8}] at @s run rotate @s ~1.5 ~" % (ME, O),
         t_ + "31..124 as %s,scores={%s_k=9}] at @s run rotate @s ~1.5 ~" % (ME, O),
         t_ + "..120 run particle minecraft:dust{color:[0.35,0.75,0.80],scale:0.7} ~ ~-0.45 ~ 1.1 0.05 1.1 0 4"]
    for k in range(9):
        o.append(t_ + "%d as %s,scores={%s_k=%d}] at @s run function %s/one" % (34 + k * 9, ME, O, k, P))
    o += [t_ + "114 run playsound minecraft:block.trial_spawner.about_to_spawn_item block @a[distance=..20] ~ ~ ~ 1 0.6",
          t_ + "124 as %s,scores={%s_k=9}] run function %s/last" % (ME, O, P),
          t_ + "125 run function %s/last_show" % P,
          t_ + "134..175 as %s,scores={%s_k=9}] at @s run rotate @s ~5 ~" % (ME, O),
          t_ + "176.. run function %s/finish" % P]
    fn("o", o)
    fn("one", ["# 揭开一件", "function %s/roll" % P, grow((0.0, 0.0, RADIUS + 0.35), 0.56, 4),
               "playsound minecraft:block.vault.eject_item block @a[distance=..16] ~ ~ ~ 0.9 1.1"] +
       ["execute if score #q %s matches %d positioned ^ ^ ^%.2f run function %s/pop_%d" % (O, t, RADIUS + 0.35, P, t) for t in TIERS])
    for t, (_n, col, _e) in TIERS.items():
        fn("pop_%d" % t, ["particle minecraft:dust{color:%s,scale:1.1} ~ ~ ~ 0.2 0.2 0.2 0 %d" % (rgb(col), 6 + 4 * t)] +
           (["particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.06 %d" % (4 * t), "playsound minecraft:block.amethyst_block.resonate block @a[distance=..16] ~ ~ ~ 1 %.1f" % (0.6 + 0.2 * t)] if t > 1 else []))
    fn("last", ["scoreboard players set #mn %s 2" % O, "function %s/roll" % P, grow((0.0, 0.55, 0.0), 1.05, 9)])
    fn("last_show", ["scoreboard players operation #q %s = %s,scores={%s_k=9},limit=1] %s_q" % (O, ME, O, O),
                     "data modify storage rpg:vault i set from entity %s,scores={%s_k=9},limit=1] item" % (ME, O), "function %s/show" % P])
    # ------------------------------------------------------------------ 亮相：名字、光柱、声音、公告
    fn("show", ["tag @a remove rpg.vt.op", "execute as @a if score @s %s_id = #c %s run tag @s add rpg.vt.op" % (O, O),
                'data modify storage rpg:vault n set value {text:"",extra:[]}',
                "data modify storage rpg:vault n.extra append from storage rpg:vault i.components.\"minecraft:custom_name\"",
                "execute store result storage rpg:vault c.n int 1 run data get storage rpg:vault i.count",
                "execute unless data storage rpg:vault i{count:1} run function %s/count with storage rpg:vault c" % P,
                'summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.vt.t","rpg.vt.tn"],billboard:"center",background:0,see_through:0b,brightness:{block:15,sky:15},'
                'transformation:{translation:[0f,0f,0f],scale:[0.95f,0.95f,0.95f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}',
                "data modify entity @e[type=minecraft:text_display,tag=rpg.vt.tn,distance=..3,limit=1] text set from storage rpg:vault n",
                "scoreboard players operation @e[type=minecraft:text_display,tag=rpg.vt.tn,distance=..3] %s_id = #c %s" % (O, O),
                "tag @e[type=minecraft:text_display,tag=rpg.vt.tn,distance=..3] remove rpg.vt.tn"] +
       ["execute if score #q %s matches %d run function %s/fx_%d" % (O, t, P, t) for t in TIERS])
    fn("count", ['$data modify storage rpg:vault n.extra append value {text:" ×$(n)",color:"%s",bold:false,italic:false}' % ui.BROADCAST_NAME])
    for t, (name, col, en) in TIERS.items():
        l = ["# %s" % name,
             "particle minecraft:dust{color:%s,scale:1.6} ~ ~0.6 ~ 0.35 0.5 0.35 0 %d" % (rgb(col), 12 + 8 * t),
             "title @a[tag=rpg.vt.op] times 4 30 12", "title @a[tag=rpg.vt.op] title " + J({"text": ""}),
             "title @a[tag=rpg.vt.op] subtitle " + J(["", {"text": "%s　" % name, "color": col, "bold": True, "italic": False}, {"text": ui.fraktur(en), "color": ui.BROADCAST_GLOSS, "italic": False}])]
        if t == 1:
            l.append("playsound minecraft:entity.player.levelup block @a[distance=..20] ~ ~ ~ 0.6 1.5")
        if t >= 2:
            l += ["particle minecraft:flash{color:[%s,1.0]} ~ ~0.7 ~ 0 0 0 0 1" % rgb(col)[1:-1],
                  "particle minecraft:end_rod ~ ~0.6 ~ 0.1 0.1 0.1 0.14 %d" % (12 * t),
                  "playsound minecraft:item.totem.use block @a[distance=..24] ~ ~ ~ 0.35 1.5", "playsound minecraft:block.bell.resonate block @a[distance=..24] ~ ~ ~ 1 %.1f" % (0.8 + 0.1 * t)]
        if t >= 3:
            l += ["particle minecraft:dust{color:%s,scale:2.2} ~ ~4 ~ 0.12 3.2 0.12 0 90" % rgb(col),
                  "playsound minecraft:ui.toast.challenge_complete block @a[distance=..32] ~ ~ ~ 0.9 1",
                  "summon minecraft:firework_rocket ~ ~1.2 ~ {Life:0,LifeTime:0,FireworksItem:{id:\"minecraft:firework_rocket\",count:1,components:{\"minecraft:fireworks\":{flight_duration:0,explosions:["
                  "{shape:\"large_ball\",has_twinkle:1b,has_trail:1b,colors:[I;%d,16777215],fade_colors:[I;%d]}]}}}}" % (num(col), num(col)),
                  "tellraw @a[distance=..64] " + J(["", {"text": "〖失乐园%s宝库〗" % ui.TAG_JOIN, "color": PL.COL, "bold": True, "italic": False}, {"text": " " + ui.fraktur("Vault"), "color": ui.BROADCAST_GLOSS, "italic": False},
                                                     {"text": "  ", "italic": False}, {"selector": "@a[tag=rpg.vt.op,limit=1]", "color": ui.BROADCAST_NAME}, {"text": " 抽到了 ", "color": ui.BROADCAST_BODY, "italic": False},
                                                     {"storage": "rpg:vault", "nbt": "n", "interpret": True}])]
        if t == 4:
            l += ["playsound minecraft:entity.lightning_bolt.thunder block @a[distance=..48] ~ ~ ~ 0.7 1.2", "particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.5 60"]
        fn("fx_%d" % t, l)
    # ------------------------------------------------------------------ 收尾
    fn("finish", ["# 奖品原样落下来，归开箱人；宝库解锁",
                  "tag @s add rpg.vt.me_c",
                  "execute as %s] run function %s/drop" % (ME, P),
                  "kill %s]" % ME,
                  "execute as @e[type=minecraft:text_display,tag=rpg.vt.t,distance=..5] if score @s %s_id = #c %s run kill @s" % (O, O),
                  "playsound minecraft:block.vault.close_shutter block @a[distance=..16] ~ ~ ~ 1 1",
                  "execute if score @s %s_m matches 0 positioned ~ ~-1.55 ~ if block ~ ~ ~ minecraft:vault run function %s/unlock_0" % (O, P),
                  "execute if score @s %s_m matches 1 positioned ~ ~-1.55 ~ if block ~ ~ ~ minecraft:vault run function %s/unlock_1" % (O, P),
                  "kill @s"])
    for m in (0, 1):
        fn("unlock_%d" % m, ["setblock ~ ~ ~ minecraft:air", "setblock ~ ~ ~ " + PL.vault_nbt(bool(m))])
    fn("drop", ['execute at @e[type=minecraft:marker,tag=rpg.vt.me_c,distance=..6,limit=1] run summon minecraft:item ~ ~0.2 ~ {Tags:["rpg.vt.d"],PickupDelay:10s,Item:{id:"minecraft:stone",count:1}}',
                "data modify entity @e[type=minecraft:item,tag=rpg.vt.d,distance=..4,limit=1] Item set from entity @s item",
                "data modify entity @e[type=minecraft:item,tag=rpg.vt.d,distance=..4,limit=1] Owner set from entity @e[type=minecraft:marker,tag=rpg.vt.me_c,distance=..6,limit=1] data.owner",
                "tag @e[type=minecraft:item,tag=rpg.vt.d,distance=..4] remove rpg.vt.d"])
    print("vault: %d prizes in 4 tiers" % (sum(len(v) for v in POOL.values()) + 1))


def odds(tab, cond):
    out, at = [], 1
    for q, per in tab:
        out.append("execute %sif score #r %s matches %d..%d run scoreboard players set #q %s %d" % (cond, O, at, at + per - 1, O, q))
        at += per
    return out


if __name__ == "__main__":
    main()
