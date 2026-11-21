# -*- coding: utf-8 -*-
"""装备养成重置：战斗时的运行逻辑。

* 每刻：玩家状态标签（手里装备的源、符文、符石、种类）、护甲符文、窗口计时、
  F 键符石、弓箭标记、旧材料换新、自动登记。
* 命中管线：rpg.hurt 的受害者 -> on attacker 是玩家 -> 汇总百分比加成，
  用一发 rpg:forge_bonus（无视受击冷却、不击退）补伤害，再重新拍下血量快照，
  免得这发补伤又被当成新的一次受击。
"""

import rpg_ui_style as ui
import forge_spec as S
from forge_common import WS, EQ, J

T = "@e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,%s]"
ATK = "@a[tag=rpg.fg.atk,limit=1]"
HAS_EQ = "*[minecraft:custom_data~{rpg_eq:{}}]"
NO_STONE = '*[minecraft:custom_data~{rpg_eq:{stone:"none"}}]'
ELIG = ("*[minecraft:custom_data~{sword_tag:1b}|minecraft:custom_data~{bow_tag:1b}"
        "|minecraft:custom_data~{chestplate_tag:1b}|minecraft:custom_data~{weapon_tag:1b}]")
EBARS = ["▰" * i + "▱" * (10 - i) for i in range(11)]


def say(text, colour=ui.GRAY):
    return "tellraw @s " + J(["", {"text": "[锻造]", "color": ui.hex_of(S.C_FORGE), "bold": True, "italic": False},
                              {"text": "　" + text, "color": ui.hex_of(colour), "italic": False}])


def build_tick(out):
    out.fn("tick", "\n".join([
        "# 装备养成的每刻入口（#minecraft:tick，排在 rpg:command/tick_end 之前）。",
        "execute as @a[tag=rpg.fg.ui] run function rpg:forge/ui/lock",
        "execute as @a[scores={rpg_fg_do=1..}] at @s run function rpg:forge/ui/do",
        "scoreboard players add #clk rpg_fg 1",
        "scoreboard players operation #c10 rpg_fg = #clk rpg_fg",
        "scoreboard players operation #c10 rpg_fg %= #10 rpg_fg",
        "scoreboard players operation #c40 rpg_fg = #clk rpg_fg",
        "scoreboard players operation #c40 rpg_fg %= #40 rpg_fg",
        "execute as @a at @s run function rpg:forge/player",
        "execute as @e[tag=rpg.hurt] at @s run function rpg:forge/hit/victim",
        "execute as @e[scores={rpg_fg_ec=1..}] at @s run function rpg:forge/rune/echo_tick",
        "execute as @e[scores={rpg_fg_bt=1..}] run function rpg:forge/rune/ember_decay",
        "execute as @e[scores={rpg_fg_mt=1..}] at @s run function rpg:forge/rune/hunt_decay",
        "execute as @e[type=#minecraft:arrows,tag=rpg.fg.meteor] at @s run function rpg:forge/rune/meteor_tick",
        "execute as @e[type=minecraft:marker,tag=rpg.fg.smelt] at @s run function rpg:forge/smelt/tick",
        "execute as @e[type=minecraft:marker,tag=rpg.fg.fire] run function rpg:forge/smelt/fire_tick",
        "execute as @e[type=minecraft:marker,tag=rpg.fg.fx] at @s run function rpg:forge/stone/fx_tick",
        "execute as @a run function rpg:forge/player_late",
    ]))
    out.fn("smelt/fire_tick", "\n".join([
        "# 选好火点却没开炉，1 分钟后作废。",
        "scoreboard players add @s rpg_fg_t 1",
        "execute if score @s rpg_fg_t matches 1200.. run kill @s",
    ]))
    out.fn("new_id", "scoreboard players add #pid rpg_fg 1\nscoreboard players operation @s rpg_fg_id = #pid rpg_fg")


def build_player(out):
    p = [
        "execute unless score @s rpg_fg_id matches 1.. run function rpg:forge/new_id",
        "# F 键：上一刻主手是带符石的武器、副手不是；这一刻它到了副手 -> 换回来并释放。",
        "scoreboard players set #cast rpg_fg 0",
        "execute if entity @s[tag=rpg.fg.sm,tag=!rpg.fg.so] if items entity @s weapon.offhand %s unless items entity @s weapon.offhand %s run function rpg:forge/stone/swap" % (HAS_EQ, NO_STONE),
        "# 手里的装备 -> 状态标签",
        "execute if entity @s[tag=rpg.fg.m] run function rpg:forge/state/clear",
        "execute if items entity @s weapon.mainhand %s run function rpg:forge/state/main" % HAS_EQ,
        "execute if score #c10 rpg_fg matches 0 run function rpg:forge/state/armor",
        "execute if score #c10 rpg_fg matches 5 run function rpg:forge/auto/scan",
        "execute if score #c40 rpg_fg matches 7 run function rpg:forge/conv/scan",
        "execute if score #cast rpg_fg matches 1 run function rpg:forge/stone/try",
        "execute if score @s rpg_fg_kx matches 1.. run function rpg:forge/kill/credit",
        "# 记下这一刻的手，供下一刻判断 F 键",
        "tag @s remove rpg.fg.sm",
        "tag @s remove rpg.fg.so",
        "execute if items entity @s weapon.mainhand %s unless items entity @s weapon.mainhand %s run tag @s add rpg.fg.sm" % (HAS_EQ, NO_STONE),
        "execute if items entity @s weapon.offhand %s unless items entity @s weapon.offhand %s run tag @s add rpg.fg.so" % (HAS_EQ, NO_STONE),
        "# 窗口计时",
    ]
    for o in ("rpg_fg_rw", "rpg_fg_rs", "rpg_fg_shd", "rpg_fg_bl", "rpg_fg_lb", "rpg_fg_shot"):
        p.append("scoreboard players remove @s[scores={%s=1..}] %s 1" % (o, o))
    p += [
        "# 弓弩射出的箭",
        "execute if score @s rpg_fg_bow matches 1.. run function rpg:forge/arrow/shot",
        "execute if score @s rpg_fg_xbow matches 1.. run function rpg:forge/arrow/shot",
        "scoreboard players reset @s rpg_fg_bow",
        "scoreboard players reset @s rpg_fg_xbow",
        "# 持续效果",
        "execute if score #c10 rpg_fg matches 3 run function rpg:forge/rune/bloodpact_tick",
        "execute if entity @s[tag=rpg.fg.a.stillwater] run function rpg:forge/rune/stillwater",
        "execute if entity @s[tag=rpg.fg.src.malice] run function rpg:forge/src/malice_tick",
        "execute if entity @s[tag=rpg.fg.bl] run particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0 1",
        "tag @s remove rpg.fg.bl",
        "execute if score @s rpg_fg_bl matches 1.. run tag @s add rpg.fg.bl",
    ]
    out.fn("player", "\n".join(p))
    out.fn("player_late", "\n".join([
        "# 命中管线之后：蓄势的空闲计数、本刻伤害清零。",
        "execute if score @s rpg_fg_dd matches 1.. run scoreboard players set @s rpg_fg_idle 0",
        "execute unless score @s rpg_fg_dd matches 1.. run scoreboard players add @s rpg_fg_idle 1",
        "scoreboard players reset @s rpg_fg_dd",
    ]))

    clear = ["tag @s remove rpg.fg.m", "tag @s remove rpg.fg.k.melee", "tag @s remove rpg.fg.k.ranged",
             "tag @s remove rpg.fg.st", "tag @s remove rpg.fg.lv10"]
    clear += ["tag @s remove rpg.fg.src.%s" % s["id"] for s in S.SOURCES]
    clear += ["tag @s remove rpg.fg.r.%s" % r["id"] for r in S.RUNES if r["part"] != "armor"]
    clear += ["tag @s remove rpg.fg.st.%s" % s["id"] for s in S.STONES]
    out.fn("state/clear", "\n".join(clear))
    main = ["tag @s add rpg.fg.m",
            'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{kind:"melee"}}] run tag @s add rpg.fg.k.melee',
            'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{kind:"ranged"}}] run tag @s add rpg.fg.k.ranged',
            "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:%d}}] run tag @s add rpg.fg.lv10" % S.LV_MAX,
            "execute unless items entity @s weapon.mainhand %s run tag @s add rpg.fg.st" % NO_STONE]
    main += ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"%s"}}] run tag @s add rpg.fg.src.%s'
             % (s["id"], s["id"]) for s in S.SOURCES]
    main += ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["%s"]}}] run tag @s add rpg.fg.r.%s'
             % (r["id"], r["id"]) for r in S.RUNES if r["part"] != "armor"]
    main += ['execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"%s"}}] run tag @s add rpg.fg.st.%s'
             % (s["id"], s["id"]) for s in S.STONES]
    out.fn("state/main", "\n".join(main))
    arm = []
    for r in S.RUNES:
        if r["part"] != "armor":
            continue
        arm.append("tag @s remove rpg.fg.a.%s" % r["id"])
        for slot in ("head", "chest", "legs", "feet"):
            arm.append('execute if items entity @s armor.%s *[minecraft:custom_data~{rpg_eq:{runes:["%s"]}}] run tag @s add rpg.fg.a.%s'
                       % (slot, r["id"], r["id"]))
    out.fn("state/armor", "\n".join(arm))

    # 自动登记：手里或身上的养成装备第一次出现时
    scan = []
    for k, slot in (("main", "weapon.mainhand"), ("head", "armor.head"), ("chest", "armor.chest"),
                    ("legs", "armor.legs"), ("feet", "armor.feet")):
        for flag in ("sword_tag", "bow_tag", "chestplate_tag", "weapon_tag"):
            scan.append("execute if items entity @s %s *[minecraft:custom_data~{%s:1b}] unless items entity @s %s %s run function rpg:forge/auto/%s"
                        % (slot, flag, slot, HAS_EQ, k))
        out.fn("auto/" + k, "\n".join([
            "function rpg:forge/wb/new", "function rpg:forge/wb/load_" + k,
            "execute store result score #ok rpg_fg run function rpg:forge/init",
            "execute if score #ok rpg_fg matches 1 run function rpg:forge/wb/save_" + k,
            "function rpg:forge/wb/close", "function rpg:forge/mig/refund"]))
    out.fn("auto/scan", "\n".join(scan))


def build_conv(out, items):
    scan, idx = [], 0
    pairs = [(pred, key, mult) for pred, key, mult in S.OLD_MATERIAL_TO_NEW]
    for flag, new in sorted(S.OLD_RUNE_TO_NEW.items()):
        pairs.append(("{%s:1b,add_weapon_tag:1b}" % flag, "rune_" + new, 1))
    for flag, new in sorted(S.OLD_STONE_TO_NEW.items()):
        pairs.append(("{%s:1b,add_weapon_tag:1b}" % flag, "stone_" + new, 1))
    for s in S.SOURCES:
        pairs.append(("{weapon_tree:%db}" % s["old"], "source_" + s["id"], 1))
    for pred, key, mult in pairs:
        idx += 1
        scan.append("execute store result score #n rpg_fg run clear @s *[minecraft:custom_data~%s] 0" % pred)
        scan.append("execute if score #n rpg_fg matches 1.. run function rpg:forge/conv/c%d" % idx)
        body = ["execute store result score #n rpg_fg run clear @s *[minecraft:custom_data~%s]" % pred]
        if mult != 1:
            body.append("scoreboard players operation #n rpg_fg *= #%d rpg_fg" % mult)
        body += ["execute store result storage rpg:forge cv.n int 1 run scoreboard players get #n rpg_fg",
                 "function rpg:forge/conv/give_%s with storage rpg:forge cv" % key,
                 say("旧材料换成了新的养成材料")]
        out.fn("conv/c%d" % idx, "\n".join(body))
    out.fn("conv/scan", "\n".join(scan))
    for key, (snbt, _cat) in items.items():
        out.fn("conv/give_" + key, "$give @s %s $(n)" % snbt)
    return len(pairs)


def build_hit(out):
    out.js("data/rpg/damage_type/forge_bonus.json",
           {"message_id": "generic", "scaling": "never", "exhaustion": 0.0})
    out.fn("hit/victim", "\n".join([
        "scoreboard players operation #d rpg_fg = @s damage_timing",
        "scoreboard players operation #d rpg_fg -= @s damage_action",
        "execute if score #d rpg_fg matches ..0 run return 0",
        "execute if entity @s[type=minecraft:player] run function rpg:forge/hit/hurt_player",
        "tag @s add rpg.fg.v",
        "execute on attacker if entity @s[type=minecraft:player] run tag @s add rpg.fg.atk",
        "execute if entity %s run function rpg:forge/hit/apply" % ATK,
        "tag @a[tag=rpg.fg.atk] remove rpg.fg.atk",
        "tag @s remove rpg.fg.v",
    ]))
    out.fn("hit/apply", "\n".join([
        "scoreboard players set #mel rpg_fg 0",
        "scoreboard players set #rng rpg_fg 0",
        "execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_dd=1..}] run scoreboard players set #mel rpg_fg 1",
        "execute if score #mel rpg_fg matches 0 if entity @a[tag=rpg.fg.atk,tag=rpg.fg.k.ranged,scores={rpg_fg_shot=1..},distance=3..] if entity @s[nbt={HurtTime:10s}] run scoreboard players set #rng rpg_fg 1",
        "execute if score #mel rpg_fg matches 0 if score #rng rpg_fg matches 0 run return 0",
        "scoreboard players set #pct rpg_fg 0",
        "scoreboard players set #spct rpg_fg 0",
        "# 六源",
        "scoreboard players set #fa rpg_fg 0",
        "execute if entity @s[type=#minecraft:undead] run scoreboard players set #fa rpg_fg 1",
        "execute if entity @s[tag=rpg.demon] run scoreboard players set #fa rpg_fg 1",
        "execute if entity @s[tag=rpg.demon.minion] run scoreboard players set #fa rpg_fg 1",
        "execute if score #fa rpg_fg matches 1 if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.faith] run scoreboard players add #spct rpg_fg 25",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.malice] run scoreboard players add #spct rpg_fg 15",
        "execute as @a[tag=rpg.fg.atk,tag=rpg.fg.src.pride] run function rpg:forge/src/pride_check",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.resolve,scores={rpg_fg_rs=1..}] run scoreboard players add #spct rpg_fg 30",
        "scoreboard players set @a[tag=rpg.fg.atk,tag=rpg.fg.src.resolve] rpg_fg_rs 0",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.hatred] run function rpg:forge/src/hatred",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.lv10] run scoreboard players operation #spct rpg_fg *= #3 rpg_fg",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.lv10] run scoreboard players operation #spct rpg_fg /= #2 rpg_fg",
        "scoreboard players operation #pct rpg_fg += #spct rpg_fg",
        "# 符文与窗口",
        "execute if score #mel rpg_fg matches 1 run function rpg:forge/hit/melee",
        "execute if score #rng rpg_fg matches 1 run function rpg:forge/hit/ranged",
        "execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_bl=1..}] run function rpg:forge/stone/blood_leech",
        "# 符石能量",
        "execute if score #mel rpg_fg matches 1 as @a[tag=rpg.fg.atk,tag=rpg.fg.st] run scoreboard players add @s rpg_fg_en %d" % S.ENERGY["melee"],
        "execute if score #rng rpg_fg matches 1 as @a[tag=rpg.fg.atk,tag=rpg.fg.st] run scoreboard players add @s rpg_fg_en %d" % S.ENERGY["ranged"],
        "scoreboard players set @a[tag=rpg.fg.atk,scores={rpg_fg_en=%d..}] rpg_fg_en %d" % (S.ENERGY_MAX + 1, S.ENERGY_MAX),
        "execute if score #pct rpg_fg matches 1.. run function rpg:forge/hit/bonus",
    ]))
    out.fn("hit/melee", "\n".join([
        "# 处决：目标生命低于 25%",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.execute] run function rpg:forge/rune/execute",
        "# 背刺：攻击者站在目标身后",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.backstab] at @s rotated ~ 0 positioned ^ ^ ^-1.5 if entity @a[tag=rpg.fg.atk,distance=..1.7] run function rpg:forge/rune/backstab",
        "# 蓄势：2 秒没出手",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.poise,scores={rpg_fg_idle=40..}] run function rpg:forge/rune/poise",
        "# 追猎标记：标记它的人近战 +25%",
        "execute if score @s rpg_fg_mt matches 1.. run function rpg:forge/rune/hunt_bonus",
        "# 反震、影步窗口",
        "execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_rw=1..}] run scoreboard players add #pct rpg_fg 40",
        "scoreboard players set @a[tag=rpg.fg.atk] rpg_fg_rw 0",
        "execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_shd=1..}] run scoreboard players add #pct rpg_fg 60",
        "scoreboard players set @a[tag=rpg.fg.atk] rpg_fg_shd 0",
        "# 余烬、回响",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.ember] run function rpg:forge/rune/ember",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.echo] run function rpg:forge/rune/echo",
    ]))
    out.fn("hit/ranged", "\n".join([
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.hunt] run function rpg:forge/rune/hunt_mark",
        "execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.split,scores={rpg_fg_crit=1..}] run function rpg:forge/rune/split",
    ]))
    out.fn("hit/bonus", "\n".join([
        "scoreboard players operation #bd rpg_fg = #d rpg_fg",
        "scoreboard players operation #bd rpg_fg *= #pct rpg_fg",
        "scoreboard players operation #bd rpg_fg /= #100 rpg_fg",
        "execute if score #bd rpg_fg matches ..0 run scoreboard players set #bd rpg_fg 1",
        "execute store result storage rpg:forge dmg.n int 1 run scoreboard players get #bd rpg_fg",
        "function rpg:forge/hit/dmg with storage rpg:forge dmg",
        "particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 6",
    ]))
    out.fn("hit/dmg", "\n".join([
        "$damage @s $(n) rpg:forge_bonus by %s" % ATK,
        "execute store result score @s damage_action run data get entity @s Health",
    ]))
    # 击杀：三档进度，同一次击杀可能同时满足几档，记最大的那档
    def victim(tags, types):
        return [{"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": pred}]}}
            for pred in ([{"nbt": '{Tags:["%s"]}' % t} for t in tags] + [{"type": t} for t in types])]
    tiers = (("any", [], [], S.XP_KILL[0]),
             ("elite", S.KILL_ELITE_TAGS, S.KILL_ELITE_TYPES, S.XP_KILL[1]),
             ("boss", S.KILL_BOSS_TAGS, S.KILL_BOSS_TYPES, S.XP_KILL[2]))
    for name, tags, types, xp in tiers:
        crit = {"k%d" % i: c for i, c in enumerate(victim(tags, types))} if tags or types else \
            {"k": {"trigger": "minecraft:player_killed_entity"}}
        out.js("data/rpg/advancement/forge/kill_%s.json" % name, {
            "criteria": crit, "requirements": [list(crit)], "rewards": {"function": "rpg:forge/kill/%s" % name}})
        out.fn("kill/" + name, "\n".join([
            "advancement revoke @s only rpg:forge/kill_%s" % name,
            "execute unless score @s rpg_fg_kx matches %d.. run scoreboard players set @s rpg_fg_kx %d" % (xp, xp)]))
    out.fn("kill/credit", "\n".join([
        "scoreboard players operation #xa rpg_fg = @s rpg_fg_kx",
        "scoreboard players reset @s rpg_fg_kx",
        "execute if entity @s[tag=rpg.fg.src.hope] run function rpg:forge/src/hope",
        "execute if entity @s[tag=rpg.fg.a.swift] run effect give @s minecraft:speed 3 1 true",
        "execute if items entity @s weapon.mainhand %s run function rpg:forge/xp/main" % HAS_EQ,
        "scoreboard players set #xa rpg_fg 1",
    ] + ["execute if items entity @s armor.%s %s run function rpg:forge/xp/%s" % (k, HAS_EQ, k)
         for k in ("head", "chest", "legs", "feet")]))
    out.fn("hit/hurt_player", "\n".join([
        "# 玩家挨打：静水清零、不屈与反震的窗口、符石能量、傲慢的代价、余生。",
        "scoreboard players set @s rpg_fg_calm 0",
        "execute if entity @s[tag=rpg.fg.src.resolve] run scoreboard players set @s rpg_fg_rs 60",
        "execute if entity @s[tag=rpg.fg.a.recoil] on attacker if entity @s[distance=..4] run scoreboard players set #rc rpg_fg 1",
        "execute if score #rc rpg_fg matches 1 run scoreboard players set @s rpg_fg_rw 20",
        "scoreboard players set #rc rpg_fg 0",
        "execute if entity @s[tag=rpg.fg.st] run scoreboard players add @s rpg_fg_en %d" % S.ENERGY["hurt"],
        "scoreboard players set @s[scores={rpg_fg_en=%d..}] rpg_fg_en %d" % (S.ENERGY_MAX + 1, S.ENERGY_MAX),
        "execute if entity @s[tag=rpg.fg.src.pride] run function rpg:forge/src/pride_cost",
        "execute if entity @s[tag=rpg.fg.a.lastbreath] unless score @s rpg_fg_lb matches 1.. run function rpg:forge/rune/lastbreath",
    ]))


def build_sources(out):
    out.fn("src/pride_check", "\n".join([
        "execute store result score #hp rpg_fg run data get entity @s Health 100",
        "execute store result score #mx rpg_fg run attribute @s minecraft:max_health get 100",
        "execute if score #hp rpg_fg >= #mx rpg_fg run scoreboard players add #spct rpg_fg 30",
    ]))
    out.fn("src/pride_cost", "\n".join([
        "scoreboard players operation #bd rpg_fg = #d rpg_fg",
        "scoreboard players operation #bd rpg_fg *= #15 rpg_fg",
        "scoreboard players operation #bd rpg_fg /= #100 rpg_fg",
        "execute if score #bd rpg_fg matches ..0 run scoreboard players set #bd rpg_fg 1",
        "execute store result storage rpg:forge dmg.n int 1 run scoreboard players get #bd rpg_fg",
        "function rpg:forge/src/self_dmg with storage rpg:forge dmg",
    ]))
    out.fn("src/self_dmg", "\n".join([
        "$damage @s $(n) rpg:forge_bonus",
        "execute store result score @s damage_action run data get entity @s Health",
    ]))
    out.fn("src/hatred", "\n".join([
        "execute unless score @s rpg_fg_vid matches 1.. run scoreboard players add #vid rpg_fg 1",
        "execute unless score @s rpg_fg_vid matches 1.. run scoreboard players operation @s rpg_fg_vid = #vid rpg_fg",
        "scoreboard players operation #tv rpg_fg = @s rpg_fg_vid",
        "execute as @a[tag=rpg.fg.atk,tag=rpg.fg.src.hatred] run function rpg:forge/src/hatred_atk",
    ]))
    out.fn("src/hatred_atk", "\n".join([
        "execute if score @s rpg_fg_hv = #tv rpg_fg run scoreboard players add @s rpg_fg_hs 1",
        "execute unless score @s rpg_fg_hv = #tv rpg_fg if score @s rpg_fg_hv matches 1.. run function rpg:forge/src/hatred_switch",
        "execute unless score @s rpg_fg_hv = #tv rpg_fg run scoreboard players set @s rpg_fg_hs 1",
        "scoreboard players operation @s rpg_fg_hv = #tv rpg_fg",
        "scoreboard players set @s[scores={rpg_fg_hs=7..}] rpg_fg_hs 6",
        "scoreboard players operation #t rpg_fg = @s rpg_fg_hs",
        "scoreboard players operation #t rpg_fg *= #5 rpg_fg",
        "scoreboard players operation #spct rpg_fg += #t rpg_fg",
    ]))
    out.fn("src/hatred_switch", "\n".join([
        "damage @s 1 rpg:forge_bonus",
        "execute store result score @s damage_action run data get entity @s Health",
        "particle minecraft:damage_indicator ~ ~1.2 ~ 0.2 0.2 0.2 0 2",
    ]))
    out.fn("src/hope", "\n".join([
        "effect give @s minecraft:instant_health 1 0 true",
        "effect give @s minecraft:regeneration 3 0 true",
        "particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3",
    ]))
    out.fn("src/malice_tick", "\n".join([
        "scoreboard players add @s rpg_fg_tn 1",
        "execute if score @s rpg_fg_tn matches 200.. run scoreboard players add @s rpg_taint 1",
        "execute if score @s rpg_fg_tn matches 200.. run scoreboard players set @s rpg_fg_tn 0",
    ]))


def build_runes(out):
    out.fn("rune/execute", "\n".join([
        "execute store result score #hp rpg_fg run data get entity @s Health 100",
        "execute store result score #mx rpg_fg run attribute @s minecraft:max_health get 100",
        "scoreboard players operation #hp rpg_fg *= #4 rpg_fg",
        "execute if score #hp rpg_fg < #mx rpg_fg run scoreboard players add #pct rpg_fg 40",
        "execute if score #hp rpg_fg < #mx rpg_fg run particle minecraft:damage_indicator ~ ~1 ~ 0.2 0.3 0.2 0.1 4",
    ]))
    out.fn("rune/backstab", "\n".join([
        "scoreboard players add #pct rpg_fg 35",
        "particle minecraft:sweep_attack ~ ~1 ~ 0 0 0 0 1",
        "playsound minecraft:entity.player.attack.crit player @a[distance=..12] ~ ~ ~ 0.7 1.4",
    ]))
    out.fn("rune/poise", "\n".join([
        "scoreboard players add #pct rpg_fg 50",
        "tag %s add rpg.fg.from" % ATK,
        "function rpg:forge/fx/push",
        "tag @a[tag=rpg.fg.from] remove rpg.fg.from",
        "playsound minecraft:entity.player.attack.knockback player @a[distance=..12] ~ ~ ~ 1 0.8",
    ]))
    out.fn("rune/hunt_bonus", "\n".join([
        "scoreboard players operation #t rpg_fg = @s rpg_fg_mark",
        "execute as @a[tag=rpg.fg.atk] if score @s rpg_fg_id = #t rpg_fg run scoreboard players add #pct rpg_fg 25",
    ]))
    out.fn("rune/hunt_mark", "\n".join([
        "scoreboard players operation @s rpg_fg_mark = %s rpg_fg_id" % ATK,
        "scoreboard players set @s rpg_fg_mt 120",
        "effect give @s minecraft:glowing 6 0 true",
    ]))
    out.fn("rune/hunt_decay", "\n".join([
        "scoreboard players remove @s rpg_fg_mt 1",
        "execute if score @s rpg_fg_mt matches 0 run scoreboard players reset @s rpg_fg_mark",
        "execute if score @s rpg_fg_mt matches 1.. if score #c10 rpg_fg matches 0 run particle minecraft:crit ~ ~2.1 ~ 0.1 0.1 0.1 0 2",
    ]))
    out.fn("rune/ember", "\n".join([
        "scoreboard players add @s rpg_fg_burn 1",
        "scoreboard players set @s rpg_fg_bt 100",
        "particle minecraft:flame ~ ~1 ~ 0.2 0.3 0.2 0.01 3",
        "execute if score @s rpg_fg_burn matches 5.. run function rpg:forge/rune/ember_burst",
    ]))
    out.fn("rune/ember_burst", "\n".join([
        "scoreboard players set @s rpg_fg_burn 0",
        "scoreboard players set @s rpg_fg_bt 0",
        "damage @s 6 rpg:forge_bonus by %s" % ATK,
        "execute store result score @s damage_action run data get entity @s Health",
        "particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 10",
        "particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.08 24",
        "playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 0.8 0.8",
    ]))
    out.fn("rune/ember_decay", "\n".join([
        "scoreboard players remove @s rpg_fg_bt 1",
        "execute if score @s rpg_fg_bt matches 0 run scoreboard players set @s rpg_fg_burn 0",
    ]))
    out.fn("rune/echo", "\n".join([
        "scoreboard players add %s rpg_fg_hit 1" % ATK,
        "execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_hit=4..}] run function rpg:forge/rune/echo_arm",
    ]))
    out.fn("rune/echo_arm", "\n".join([
        "scoreboard players set %s rpg_fg_hit 0" % ATK,
        "scoreboard players operation @s rpg_fg_ea = #d rpg_fg",
        "scoreboard players operation @s rpg_fg_ea *= #60 rpg_fg",
        "scoreboard players operation @s rpg_fg_ea /= #100 rpg_fg",
        "execute if score @s rpg_fg_ea matches ..0 run scoreboard players set @s rpg_fg_ea 1",
        "scoreboard players operation @s rpg_fg_eo = %s rpg_fg_id" % ATK,
        "scoreboard players set @s rpg_fg_ec 10",
    ]))
    out.fn("rune/echo_tick", "\n".join([
        "scoreboard players remove @s rpg_fg_ec 1",
        "execute if score @s rpg_fg_ec matches 1.. run return 0",
        "scoreboard players operation #t rpg_fg = @s rpg_fg_eo",
        "execute as @a if score @s rpg_fg_id = #t rpg_fg run tag @s add rpg.fg.eo",
        "execute store result storage rpg:forge dmg.n int 1 run scoreboard players get @s rpg_fg_ea",
        "execute if entity @a[tag=rpg.fg.eo] run function rpg:forge/rune/echo_hit with storage rpg:forge dmg",
        "tag @a[tag=rpg.fg.eo] remove rpg.fg.eo",
    ]))
    out.fn("rune/echo_hit", "\n".join([
        "$damage @s $(n) rpg:forge_bonus by @a[tag=rpg.fg.eo,limit=1]",
        "execute store result score @s damage_action run data get entity @s Health",
        "particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2",
        "playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 0.8 1.3",
    ]))
    out.fn("rune/split", "\n".join([
        "data modify storage rpg:forge owner set from entity %s UUID" % ATK,
        "execute as %s run function rpg:forge/rune/split_one" % (T % "distance=1..8,tag=!rpg.fg.v,limit=2,sort=nearest"),
        "scoreboard players set @a[tag=rpg.fg.atk] rpg_fg_crit 0",
    ]))
    out.fn("rune/split_one", "\n".join([
        "execute at @e[tag=rpg.fg.v,limit=1] positioned ~ ~1.2 ~ facing entity @s eyes run function rpg:forge/fx/fire",
    ]))
    out.fn("rune/meteor_tick", "\n".join([
        "execute if data entity @s {inGround:1b} run function rpg:forge/rune/meteor_boom",
    ]))
    out.fn("rune/meteor_boom", "\n".join([
        "scoreboard players operation #t rpg_fg = @s rpg_fg_eo",
        "execute as @a if score @s rpg_fg_id = #t rpg_fg run tag @s add rpg.fg.eo",
        "execute as %s run damage @s 4 rpg:forge_bonus by @a[tag=rpg.fg.eo,limit=1]" % (T % "distance=..3"),
        "tag @a[tag=rpg.fg.eo] remove rpg.fg.eo",
        "particle minecraft:explosion ~ ~0.3 ~ 0.6 0.2 0.6 0 3",
        "particle minecraft:end_rod ~ ~0.5 ~ 0.4 0.6 0.4 0.15 16",
        "playsound minecraft:entity.firework_rocket.blast player @a[distance=..24] ~ ~ ~ 1 0.7",
        "kill @s",
    ]))
    out.fn("rune/lastbreath", "\n".join([
        "execute store result score #hp rpg_fg run data get entity @s Health",
        "execute if score #hp rpg_fg matches 4.. run return 0",
        "effect give @s minecraft:resistance 2 4 true",
        "effect give @s minecraft:regeneration 3 1 true",
        "scoreboard players set @s rpg_fg_lb 2400",
        "particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.4 30",
        "playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.6 1.4",
        say("［余生］护住了你，120 秒后才能再次生效", ui.HOLY),
    ]))
    out.fn("rune/stillwater", "\n".join([
        "scoreboard players add @s rpg_fg_calm 1",
        "execute if score @s rpg_fg_calm matches 60 run function rpg:forge/rune/stillwater_give",
        "execute if score @s rpg_fg_calm matches 120.. run scoreboard players set @s rpg_fg_calm 60",
    ]))
    out.fn("rune/stillwater_give", "\n".join([
        "execute store result score #t rpg_fg run data get entity @s AbsorptionAmount",
        "execute if score #t rpg_fg matches 1.. run return 0",
        "effect clear @s minecraft:absorption",
        "effect give @s minecraft:absorption 30 0 true",
        "particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0.02 10",
    ]))
    out.fn("rune/bloodpact_tick", "\n".join([
        "execute unless entity @s[tag=rpg.fg.r.bloodpact] run return run attribute @s minecraft:attack_damage modifier remove rpg:forge/bloodpact",
        "execute store result score #hp rpg_fg run data get entity @s Health 100",
        "execute store result score #mx rpg_fg run attribute @s minecraft:max_health get 100",
        "scoreboard players operation #t rpg_fg = #mx rpg_fg",
        "scoreboard players operation #t rpg_fg -= #hp rpg_fg",
        "scoreboard players operation #t rpg_fg *= #10 rpg_fg",
        "scoreboard players operation #t rpg_fg /= #mx rpg_fg",
        "execute if score #t rpg_fg matches 10.. run scoreboard players set #t rpg_fg 9",
        "execute if score #t rpg_fg matches ..-1 run scoreboard players set #t rpg_fg 0",
        "scoreboard players operation #t rpg_fg *= #4 rpg_fg",
        "attribute @s minecraft:attack_damage modifier remove rpg:forge/bloodpact",
        "execute if score #t rpg_fg matches 0 run return 0",
        "execute store result storage rpg:forge bp.p int 1 run scoreboard players get #t rpg_fg",
        'data modify storage rpg:forge bp.z set value ""',
        'execute if score #t rpg_fg matches ..9 run data modify storage rpg:forge bp.z set value "0"',
        "function rpg:forge/rune/bloodpact_set with storage rpg:forge bp",
    ]))
    out.fn("rune/bloodpact_set", "$attribute @s minecraft:attack_damage modifier add rpg:forge/bloodpact 0.$(z)$(p) add_multiplied_total")


def build_arrows(out):
    out.fn("arrow/shot", "\n".join([
        "# 刚松手：给附近还没登记的箭打上标记，按品质与等级放大伤害。",
        "scoreboard players set @s rpg_fg_shot 60",
        "scoreboard players set @s rpg_fg_crit 0",
        "execute unless entity @s[tag=rpg.fg.k.ranged] run return 0",
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_main",
        "execute store result score #fac rpg_fg run data get entity %s %s.fac" % (WS, EQ),
        "function rpg:forge/wb/close",
        "execute if score #fac rpg_fg matches ..0 run scoreboard players set #fac rpg_fg 100",
        "scoreboard players operation #me rpg_fg = @s rpg_fg_id",
        "scoreboard players set #met rpg_fg 0",
        "execute if entity @s[tag=rpg.fg.r.meteor,x_rotation=-90..-45] run scoreboard players set #met rpg_fg 1",
        "execute as @e[type=#minecraft:arrows,distance=..6,tag=!rpg.fg.a] run function rpg:forge/arrow/tag",
    ]))
    out.fn("arrow/tag", "\n".join([
        "tag @s add rpg.fg.a",
        "scoreboard players operation @s rpg_fg_eo = #me rpg_fg",
        "execute store result score #ad rpg_fg run data get entity @s damage 100",
        "scoreboard players operation #ad rpg_fg *= #fac rpg_fg",
        "scoreboard players operation #ad rpg_fg /= #100 rpg_fg",
        "execute store result entity @s damage double 0.01 run scoreboard players get #ad rpg_fg",
        "execute if data entity @s {crit:1b} as @a if score @s rpg_fg_id = #me rpg_fg run scoreboard players set @s rpg_fg_crit 1",
        "execute if score #met rpg_fg matches 1 run tag @s add rpg.fg.meteor",
    ]))


def build_fx(out):
    out.fn("fx/push", "\n".join([
        "# 把 @s 从 rpg.fg.from 那里推开（玩家不推）。",
        "execute if entity @s[type=minecraft:player] run return 0",
        "execute at @s facing entity @e[tag=rpg.fg.from,limit=1] feet rotated ~ 0 positioned ^ ^ ^-1 run summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.fg.vb\"]}",
        "execute store result score #ax rpg_fg run data get entity @s Pos[0] 1000",
        "execute store result score #az rpg_fg run data get entity @s Pos[2] 1000",
        "execute store result score #bx rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[0] 1000",
        "execute store result score #bz rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[2] 1000",
        "kill @e[type=minecraft:marker,tag=rpg.fg.vb]",
        "scoreboard players operation #bx rpg_fg -= #ax rpg_fg",
        "scoreboard players operation #bz rpg_fg -= #az rpg_fg",
        "execute store result entity @s Motion[0] double 0.0009 run scoreboard players get #bx rpg_fg",
        "execute store result entity @s Motion[2] double 0.0009 run scoreboard players get #bz rpg_fg",
        "data modify entity @s Motion[1] set value 0.42d",
    ]))
    out.fn("fx/fire", "\n".join([
        "# 沿当前朝向射出一支箭（速度 1.6），Owner 取 storage rpg:forge owner。",
        'summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.va"]}',
        'summon minecraft:marker ^ ^ ^1 {Tags:["rpg.fg.vb"]}',
    ] + ["execute store result score #%s%s rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.v%s,limit=1] Pos[%d] 1000" % (ab, ax, ab, i)
         for ab in "ab" for i, ax in enumerate("xyz")] + [
        "scoreboard players operation #bx rpg_fg -= #ax rpg_fg",
        "scoreboard players operation #by rpg_fg -= #ay rpg_fg",
        "scoreboard players operation #bz rpg_fg -= #az rpg_fg",
        'summon minecraft:arrow ^ ^ ^0.9 {Tags:["rpg.fg.na","rpg.fg.a"],pickup:0b,damage:3.0d}',
        "execute store result entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Motion[0] double 0.0016 run scoreboard players get #bx rpg_fg",
        "execute store result entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Motion[1] double 0.0016 run scoreboard players get #by rpg_fg",
        "execute store result entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Motion[2] double 0.0016 run scoreboard players get #bz rpg_fg",
        "data modify entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Owner set from storage rpg:forge owner",
        "tag @e[type=minecraft:arrow,tag=rpg.fg.na] remove rpg.fg.na",
        "kill @e[type=minecraft:marker,tag=rpg.fg.va]",
        "kill @e[type=minecraft:marker,tag=rpg.fg.vb]",
        "particle minecraft:crit ~ ~ ~ 0.1 0.1 0.1 0.2 4",
    ]))


def build_stones(out, volley_offsets):
    out.js("data/rpg/predicate/forge/sneaking.json",
           {"condition": "minecraft:entity_properties", "entity": "this",
            "predicate": {"flags": {"is_sneaking": True}}})
    out.js("data/rpg/tags/entity_type/forge/projectiles.json", {"values": [
        "#minecraft:arrows", "minecraft:small_fireball", "minecraft:fireball", "minecraft:wither_skull",
        "minecraft:shulker_bullet", "minecraft:llama_spit", "minecraft:breeze_wind_charge",
        "minecraft:snowball", "minecraft:splash_potion", "minecraft:lingering_potion", "minecraft:trident"]})
    out.fn("stone/swap", "\n".join([
        "# 潜行按 F 照常换手（比如要把武器放到副手进工坊）。",
        "execute if predicate rpg:forge/sneaking run return 0",
        'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fg.tmp"],view_range:0f}',
        "item replace entity @e[type=minecraft:item_display,tag=rpg.fg.tmp,limit=1] contents from entity @s weapon.mainhand",
        "item replace entity @s weapon.mainhand from entity @s weapon.offhand",
        "item replace entity @s weapon.offhand from entity @e[type=minecraft:item_display,tag=rpg.fg.tmp,limit=1] contents",
        "kill @e[type=minecraft:item_display,tag=rpg.fg.tmp]",
        "scoreboard players set #cast rpg_fg 1",
    ]))
    tries = [
        "execute unless score @s rpg_fg_en matches %d.. run return run function rpg:forge/stone/not_ready" % S.ENERGY_MAX,
        "scoreboard players set @s rpg_fg_en 0",
    ]
    tries += ["execute if entity @s[tag=rpg.fg.st.%s] run function rpg:forge/stone/%s" % (s["id"], s["id"]) for s in S.STONES]
    out.fn("stone/try", "\n".join(tries))
    out.fn("stone/not_ready", "\n".join([
        "execute store result storage rpg:forge d.en int 1 run scoreboard players get @s rpg_fg_en",
        "function rpg:forge/stone/not_ready_msg with storage rpg:forge d",
        "playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.6",
    ]))
    out.fn("stone/not_ready_msg", "$" + say("符石能量 $(en)/%d，还放不出来" % S.ENERGY_MAX))
    tgt = T
    out.fn("stone/rift", "\n".join([
        "tag @s add rpg.fg.from",
        "execute anchored feet positioned ^ ^ ^2 run particle minecraft:explosion ~ ~0.3 ~ 0.4 0.1 0.4 0 2",
        "execute anchored feet positioned ^ ^ ^4 run particle minecraft:explosion ~ ~0.3 ~ 0.6 0.1 0.6 0 3",
        "execute anchored feet positioned ^ ^ ^3 run particle minecraft:block{block_state:\"minecraft:coarse_dirt\"} ~ ~0.2 ~ 1.2 0.1 1.2 0 60",
        "playsound minecraft:entity.generic.explode player @a[distance=..24] ~ ~ ~ 0.7 1.3",
        "execute rotated ~ 0 positioned ^ ^ ^3 as %s run function rpg:forge/stone/rift_hit" % (tgt % "distance=..3.3"),
        "tag @s remove rpg.fg.from",
    ]))
    out.fn("stone/rift_hit", "\n".join([
        "damage @s 8 rpg:forge_bonus by @a[tag=rpg.fg.from,limit=1]",
        "execute store result score @s damage_action run data get entity @s Health",
        "function rpg:forge/fx/push",
    ]))
    out.fn("stone/frost", "\n".join([
        "execute as %s run function rpg:forge/stone/frost_hit" % (tgt % "distance=..5"),
        "particle minecraft:snowflake ~ ~1 ~ 2.5 0.3 2.5 0.02 120",
        "particle minecraft:item_snowball ~ ~0.5 ~ 2.5 0.2 2.5 0.1 40",
        "playsound minecraft:block.powder_snow.break player @a[distance=..24] ~ ~ ~ 1 0.6",
        "playsound minecraft:block.glass.break player @a[distance=..24] ~ ~ ~ 0.6 1.6",
    ]))
    out.fn("stone/frost_hit", "\n".join([
        "effect give @s minecraft:slowness 2 4 true",
        "effect give @s minecraft:mining_fatigue 2 2 true",
        "data modify entity @s TicksFrozen set value 140",
        "particle minecraft:snowflake ~ ~1 ~ 0.3 0.6 0.3 0.01 10",
    ]))
    out.fn("stone/shadow", "\n".join([
        "tag @s add rpg.fg.caster",
        "scoreboard players set #i rpg_fg 24",
        "execute anchored eyes positioned ^ ^ ^1 run function rpg:forge/stone/shadow_ray",
        "execute unless entity @e[tag=rpg.fg.tgt] run scoreboard players set @s rpg_fg_en %d" % S.ENERGY_MAX,
        "execute unless entity @e[tag=rpg.fg.tgt] run %s" % say("12 格内没有可以影步的目标，能量已退回", ui.WARN),
        "execute if entity @e[tag=rpg.fg.tgt] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 20",
        "execute as @e[tag=rpg.fg.tgt,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-1.6 run tp @a[tag=rpg.fg.caster,limit=1] ~ ~ ~ facing entity @s eyes",
        "execute if entity @e[tag=rpg.fg.tgt] run scoreboard players set @s rpg_fg_shd 60",
        "execute if entity @e[tag=rpg.fg.tgt] at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 40",
        "execute if entity @e[tag=rpg.fg.tgt] at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 0.8 0.7",
        "tag @e[tag=rpg.fg.tgt] remove rpg.fg.tgt",
        "tag @s remove rpg.fg.caster",
    ]))
    out.fn("stone/shadow_ray", "\n".join([
        "execute positioned ~-0.5 ~-0.5 ~-0.5 as %s run tag @s add rpg.fg.tgt" % (tgt % "dx=0,dy=0,dz=0,limit=1"),
        "execute if entity @e[tag=rpg.fg.tgt] run return 0",
        "execute unless block ~ ~ ~ #minecraft:replaceable run return 0",
        "scoreboard players remove #i rpg_fg 1",
        "execute if score #i rpg_fg matches 1.. positioned ^ ^ ^0.5 run function rpg:forge/stone/shadow_ray",
    ]))
    out.fn("stone/blood", "\n".join([
        "execute store result score #t rpg_fg run data get entity @s Health",
        "scoreboard players operation #t rpg_fg /= #5 rpg_fg",
        "execute if score #t rpg_fg matches ..0 run scoreboard players set #t rpg_fg 1",
        "execute store result storage rpg:forge dmg.n int 1 run scoreboard players get #t rpg_fg",
        "function rpg:forge/src/self_dmg with storage rpg:forge dmg",
        "scoreboard players set @s rpg_fg_bl 160",
        "scoreboard players set @s rpg_fg_blh 0",
        "particle minecraft:damage_indicator ~ ~1 ~ 0.4 0.6 0.4 0.1 16",
        "playsound minecraft:entity.warden.heartbeat player @a[distance=..16] ~ ~ ~ 1 1.2",
    ]))
    out.fn("stone/blood_leech", "\n".join([
        "scoreboard players operation #t rpg_fg = #d rpg_fg",
        "scoreboard players operation #t rpg_fg *= #25 rpg_fg",
        "scoreboard players operation %s rpg_fg_blh += #t rpg_fg" % ATK,
        "execute as @a[tag=rpg.fg.atk,scores={rpg_fg_blh=400..}] run function rpg:forge/stone/blood_heal",
    ]))
    out.fn("stone/blood_heal", "\n".join([
        "scoreboard players remove @s rpg_fg_blh 400",
        "effect give @s minecraft:instant_health 1 0 true",
        "execute if score @s rpg_fg_blh matches 400.. run function rpg:forge/stone/blood_heal",
    ]))
    out.fn("stone/gale", "\n".join([
        'execute rotated ~ 0 positioned ^ ^ ^2.5 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.gale","rpg.fg.new"]}',
        "execute rotated ~ 0 run tp @e[type=minecraft:marker,tag=rpg.fg.new,limit=1] ^ ^ ^2.5 ~ 0",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_t 80",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_eo = @s rpg_fg_id",
        "tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new",
        "playsound minecraft:entity.breeze.wind_burst player @a[distance=..24] ~ ~ ~ 1 0.8",
    ]))
    out.fn("stone/volley", "\n".join([
        "scoreboard players set #i rpg_fg 48",
        "execute anchored eyes positioned ^ ^ ^ run function rpg:forge/stone/volley_ray",
        "data modify entity @e[type=minecraft:marker,tag=rpg.fg.new,limit=1] data.owner set from entity @s UUID",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_t 60",
        "tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new",
        "playsound minecraft:item.crossbow.loading_end player @a[distance=..16] ~ ~ ~ 1 0.7",
    ]))
    out.fn("stone/volley_ray", "\n".join([
        "scoreboard players remove #i rpg_fg 1",
        'execute if score #i rpg_fg matches ..0 run return run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.volley","rpg.fg.new"]}',
        'execute unless block ~ ~ ~ #minecraft:replaceable run return run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.volley","rpg.fg.new"]}',
        'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity %s positioned ~0.5 ~0.5 ~0.5 run return run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.volley","rpg.fg.new"]}' % (tgt % "dx=0,dy=0,dz=0"),
        "execute positioned ^ ^ ^0.5 run function rpg:forge/stone/volley_ray",
    ]))
    out.fn("stone/banner", "\n".join([
        'summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.banner","rpg.fg.new"]}',
        'summon minecraft:item_display ~ ~1.3 ~ {Tags:["rpg.fg.bdisp"],item:{id:"minecraft:white_banner",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.4f,1.4f,1.4f]}}',
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_t 200",
        "tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new",
        "playsound minecraft:event.raid.horn player @a[distance=..32] ~ ~ ~ 0.6 1.4",
    ]))
    fx = [
        "scoreboard players remove @s rpg_fg_t 1",
        "execute if entity @s[tag=rpg.fg.gale] run function rpg:forge/stone/gale_tick",
        "execute if entity @s[tag=rpg.fg.volley] run function rpg:forge/stone/volley_tick",
        "execute if entity @s[tag=rpg.fg.banner] run function rpg:forge/stone/banner_tick",
        "execute if score @s rpg_fg_t matches ..0 if entity @s[tag=rpg.fg.banner] run kill @e[type=minecraft:item_display,tag=rpg.fg.bdisp,distance=..2,limit=1,sort=nearest]",
        "execute if score @s rpg_fg_t matches ..0 run kill @s",
    ]
    out.fn("stone/fx_tick", "\n".join(fx))
    out.fn("stone/gale_tick", "\n".join([
        "particle minecraft:cloud ^-1.5 ^0.5 ^ 0 0.6 0 0.01 2",
        "particle minecraft:cloud ^ ^0.5 ^ 0 0.6 0 0.01 2",
        "particle minecraft:cloud ^1.5 ^0.5 ^ 0 0.6 0 0.01 2",
        "particle minecraft:gust ^ ^1 ^ 1 0.6 0.2 0 1",
        "tag @s add rpg.fg.from",
        "execute as %s run function rpg:forge/fx/push" % (tgt % "distance=..2.6"),
        "tag @s remove rpg.fg.from",
        "kill @e[type=#rpg:forge/projectiles,distance=..2.6,tag=!rpg.fg.a]",
    ]))
    vt = []
    for t, (dx, dz) in volley_offsets:
        vt.append('execute if score @s rpg_fg_t matches %d run summon minecraft:arrow ~%.1f ~9 ~%.1f {Tags:["rpg.fg.rain","rpg.fg.a"],pickup:0b,damage:4.0d,Motion:[0.0,-2.2,0.0]}' % (t, dx, dz))
    vt += [
        "execute as @e[type=minecraft:arrow,tag=rpg.fg.rain,tag=!rpg.fg.own,distance=..12] run data modify entity @s Owner set from entity @e[type=minecraft:marker,tag=rpg.fg.volley,limit=1,sort=nearest] data.owner",
        "tag @e[type=minecraft:arrow,tag=rpg.fg.rain,distance=..12] add rpg.fg.own",
        "kill @e[type=minecraft:arrow,tag=rpg.fg.rain,tag=rpg.fg.own,nbt={inGround:1b},distance=..12]",
        "particle minecraft:crit ~ ~0.2 ~ 2 0.1 2 0 6",
    ]
    out.fn("stone/volley_tick", "\n".join(vt))
    out.fn("stone/banner_tick", "\n".join([
        "particle minecraft:end_rod ~ ~0.3 ~ 3 0.05 3 0 2",
        "execute if score @s rpg_fg_t matches 1.. run scoreboard players operation #t rpg_fg = @s rpg_fg_t",
        "scoreboard players operation #t rpg_fg %= #20 rpg_fg",
        "execute if score #t rpg_fg matches 0 run effect give @e[tag=rpg.unit,distance=..6] minecraft:strength 2 0 true",
        "execute if score #t rpg_fg matches 0 run effect give @e[tag=rpg.unit,distance=..6] minecraft:resistance 2 0 true",
        "execute if score #t rpg_fg matches 0 run effect give @a[distance=..6] minecraft:strength 2 0 true",
        "execute if score #t rpg_fg matches 0 run effect give @a[distance=..6] minecraft:resistance 2 0 true",
    ]))


def build_hud(out):
    lines = []
    for i, b in enumerate(EBARS):
        colour = ui.READY if i == 10 else ui.WHITE
        lines.append("execute if score #e rpg_fg matches %d run data modify storage rpg:forge hud.v set value '%s'"
                     % (i, J({"text": b, "color": ui.hex_of(colour), "italic": False})))
    out.fn("hud", "\n".join([
        "# 屏幕下方状态行里的符石能量（rpg:hud/status 调用）。占第一个空槽。",
        "scoreboard players operation #e rpg_fg = @s rpg_fg_en",
        "scoreboard players operation #e rpg_fg /= #10 rpg_fg",
    ] + lines + [
        "scoreboard players set @s rpg_hud_on 1",
        "execute if data storage rpg:hud {d:'{\"text\":\"\"}'} run return run function rpg:forge/hud_d",
        "execute if data storage rpg:hud {c:'{\"text\":\"\"}'} run return run function rpg:forge/hud_c",
        "execute if data storage rpg:hud {b:'{\"text\":\"\"}'} run return run function rpg:forge/hud_b",
    ]))
    for slot in "dcb":
        out.fn("hud_" + slot, ('data modify storage rpg:forge hud.slot set value "%s"' % slot)
               + "\n" + "function rpg:forge/hud_put with storage rpg:forge hud")
    out.fn("hud_put", "$data modify storage rpg:hud $(slot) set value '[\"\",%s,$(v)]'" % J(
        {"text": "🔱 ", "color": ui.hex_of(ui.GRAY), "italic": False}).replace("'", ""))
