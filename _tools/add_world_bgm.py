# -*- coding: utf-8 -*-
"""失乐园与主世界的背景音乐（用户 2026-11-25：「失乐园的音乐单独寻找，需要有独立的背景音乐，不依托于音乐这个声音选项，主世界也要有，要求相同」）。

    python add_world_bgm.py ../rpg

曲子在 bgm_ref/{pl,ow}_*.ogg（来源见 bgm_ref/SOURCES.md），由 add_boss_bgm.py 登记成 rpg:bgm.<名>。
每名玩家一个小调度器，每秒跑一次，走 record（唱片机）声道，并停掉原版背景音乐：
  * 失乐园：门内、猎场、灰烬边境与黑石堡垒、血月、河庭各一首，连续循环；换区要稳 3 秒才换，免得在边界上来回切。
  * 主世界：白天三首、夜里两首，随机不重复，一首放完静 60 到 120 秒。昼夜交替不打断正在放的曲子。
  * Boss 战、序章、新手开局、支线的配乐在放时让路，停了再接。
退出重进后声音没了，所以按 leave_game 重新起头。
"""
import io
import os
import sys

import add_paradise as PL
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function", "bgm")
P = "rpg:bgm"
LEN = {"pl_gate": 72.0, "pl_hunt": 185.7, "pl_ash": 224.1, "pl_court": 240.1, "pl_moon": 261.2,
       "ow_day1": 161.6, "ow_day2": 192.1, "ow_day3": 104.8, "ow_night1": 153.6, "ow_night2": 120.1}
GATE, HUNT, ASH, COURT, MOON, DAY, NIGHT = 1, 2, 3, 4, 5, 10, 11
PLACE = {GATE: "pl_gate", HUNT: "pl_hunt", ASH: "pl_ash", COURT: "pl_court", MOON: "pl_moon"}
SETS = {DAY: ["ow_day1", "ow_day2", "ow_day3"], NIGHT: ["ow_night1", "ow_night2"]}
# 有自己配乐的 Boss：场地中心的标记
CENTERS = ["rpg.jqb.center", "rpg.lub.center", "rpg.mkb.center", "rpg.slb.center", "rpg.usb.center", "rpg.pf.center"]


def fn(name, lines):
    path = os.path.join(FUNC, name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    fn("load", ["scoreboard objectives add rpg_bgm dummy",
                "scoreboard objectives add rpg_bgm_w dummy", "scoreboard objectives add rpg_bgm_c dummy", "scoreboard objectives add rpg_bgm_t dummy",
                "scoreboard objectives add rpg_bgm_s dummy", "scoreboard objectives add rpg_bgm_g dummy", "scoreboard objectives add rpg_bgm_l dummy",
                "scoreboard objectives add rpg_bgm_lv minecraft.custom:minecraft.leave_game"])
    fn("tick", ["scoreboard players add #t rpg_bgm 1", "execute if score #t rpg_bgm matches 20.. run function %s/sec" % P])
    fn("sec", ["scoreboard players set #t rpg_bgm 0",
               "execute store result score #day rpg_bgm run time query daytime",
               "execute as @a at @s run function %s/player" % P])
    fn("player", [
        "# 每秒：先定该放什么（w），再和正在放的（c）比",
        "execute if score @s rpg_bgm_lv matches 1.. run function %s/rejoin" % P,
        "scoreboard players add @s rpg_bgm_c 0", "scoreboard players add @s rpg_bgm_t 0",
        "scoreboard players set @s rpg_bgm_w 0",
        "execute if dimension minecraft:overworld run function %s/want_ow" % P,
        "execute if dimension rpg:paradise_lost run function %s/want_pl" % P,
        "execute unless score @s rpg_bgm_w matches 0 run function %s/yield" % P,
        "execute if score @s rpg_bgm_w matches 0 if score @s rpg_bgm_c matches 0 run return 0",
        "execute if score @s rpg_bgm_w matches 0 run return run function %s/stop" % P,
        "stopsound @s music",
        "execute if score @s rpg_bgm_c = @s rpg_bgm_w run return run function %s/same" % P,
        "execute if score @s rpg_bgm_c matches 0 run return run function %s/begin" % P,
        "# 昼夜交替：不打断，只换后面的曲单",
        "execute if score @s rpg_bgm_c matches %d..%d if score @s rpg_bgm_w matches %d..%d run return run function %s/shift" % (DAY, NIGHT, DAY, NIGHT, P),
        "# 换区：稳 3 秒才换（还在放的曲子照常计时）",
        "scoreboard players add @s rpg_bgm_s 1", "scoreboard players remove @s rpg_bgm_t 1",
        "execute if score @s rpg_bgm_s matches 3.. run function %s/swap" % P])
    fn("rejoin", ["scoreboard players set @s rpg_bgm_lv 0", "scoreboard players set @s rpg_bgm_c 0", "scoreboard players set @s rpg_bgm_t 0"])
    fn("want_ow", ["scoreboard players set @s rpg_bgm_w %d" % DAY,
                   "execute if score #day rpg_bgm matches 12800..23200 run scoreboard players set @s rpg_bgm_w %d" % NIGHT])
    pl = ["scoreboard players set @s rpg_bgm_w %d" % HUNT,
          "execute if entity @s[x=0,y=83,z=0,distance=%d..] run scoreboard players set @s rpg_bgm_w %d" % (PL.ZONE_R[1], ASH),
          "execute if predicate rpg:paradise/in_fortress run scoreboard players set @s rpg_bgm_w %d" % ASH,
          "execute if score #moon %s matches 1.. run scoreboard players set @s rpg_bgm_w %d" % (PL.O, MOON),
          "execute if entity @s[x=0,y=83,z=0,distance=..%d] run scoreboard players set @s rpg_bgm_w %d" % (PL.GATE_R, GATE)]
    for k, c in PL.COURTS.items():
        pl.append("execute if score #c%d %s matches 1..2 if entity @s[x=%d,y=83,z=%d,distance=..34] run scoreboard players set @s rpg_bgm_w %d" % (k, PL.O, c[2], c[3], COURT))
    fn("want_pl", pl)
    fn("yield", ["# 别的配乐在放：让路"] + [
        "execute if entity @s[tag=%s] run return run scoreboard players set @s rpg_bgm_w 0" % t for t in ("rpg.pr", "rpg.ob")] + [
        "execute if score @s %s matches 1.. run return run scoreboard players set @s rpg_bgm_w 0" % o for o in ("rpg_ob_mi", "rpg_q_mt")] + [
        "execute if entity @e[type=minecraft:marker,tag=%s,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0" % t for t in CENTERS])
    fn("same", ["scoreboard players set @s rpg_bgm_s 0", "scoreboard players remove @s rpg_bgm_t 1",
                "execute if score @s rpg_bgm_t matches ..0 run function %s/next" % P])
    fn("shift", ["scoreboard players operation @s rpg_bgm_c = @s rpg_bgm_w", "scoreboard players set @s rpg_bgm_s 0"])
    fn("swap", ["function %s/stop" % P, "function %s/begin" % P])
    fn("begin", ["# 从头起：主世界先静一小会儿",
                 "scoreboard players operation @s rpg_bgm_c = @s rpg_bgm_w", "scoreboard players set @s rpg_bgm_s 0", "scoreboard players set @s rpg_bgm_g 0",
                 "execute if score @s rpg_bgm_c matches %d.. run return run function %s/begin_ow" % (DAY, P),
                 "function %s/next" % P])
    fn("begin_ow", ["scoreboard players set @s rpg_bgm_g 1", "execute store result score @s rpg_bgm_t run random value 6..15"])
    fn("next", ["# 一首放完（或间歇结束）",
                "execute if score @s rpg_bgm_c matches %d.. if score @s rpg_bgm_g matches 0 run return run function %s/gap" % (DAY, P),
                "scoreboard players set @s rpg_bgm_g 0"] +
       ["execute if score @s rpg_bgm_c matches %d run return run function %s/play/%s" % (k, P, t) for k, t in PLACE.items()] +
       ["execute if score @s rpg_bgm_c matches %d run return run function %s/pick_%d" % (k, P, k) for k in SETS])
    fn("gap", ["scoreboard players set @s rpg_bgm_g 1", "execute store result score @s rpg_bgm_t run random value 60..120"])
    for k, ts in SETS.items():
        n = len(ts)
        fn("pick_%d" % k, ["# 随机一首，和上一首不同（最近一首记在 l，从 1 数）",
                           "execute store result score #r rpg_bgm run random value 1..%d" % n,
                           "execute if score #r rpg_bgm = @s rpg_bgm_l run scoreboard players add #r rpg_bgm 1",
                           "execute if score #r rpg_bgm matches %d.. run scoreboard players set #r rpg_bgm 1" % (n + 1),
                           "scoreboard players operation @s rpg_bgm_l = #r rpg_bgm"] +
           ["execute if score #r rpg_bgm matches %d run return run function %s/play/%s" % (i, P, t) for i, t in enumerate(ts, 1)])
    for t, sec in LEN.items():
        fn("play/" + t, ["playsound rpg:bgm.%s record @s ~ ~ ~ 1 1" % t, "scoreboard players set @s rpg_bgm_t %d" % (int(sec) + 1)])
    fn("stop", ["scoreboard players set @s rpg_bgm_c 0", "scoreboard players set @s rpg_bgm_t 0", "scoreboard players set @s rpg_bgm_s 0"] +
       ["stopsound @s record rpg:bgm.%s" % t for t in LEN])
    print("world bgm: %d tracks, %d places + day/night" % (len(LEN), len(PLACE)))


if __name__ == "__main__":
    main()
