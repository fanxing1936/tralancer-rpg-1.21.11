# -*- coding: utf-8 -*-
"""Build the configurable endless exorcism dungeon.

The mode combines the 35 authored seven-sin retainers with the remaining 37
spirits of the Ars Goetia.  A 72-formation deck exposes every named spirit;
the roaming spirits inherit one of five readable combat jobs and one of seven
affinities, so the expanded roster changes behaviour as well as name colour.
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
from pathlib import Path

from add_demon_minions import LORDS, ROLES


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
FUNC = DP / "data" / "rpg" / "function"
ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "_endless_exorcism_config.json"

GOLD = "#D4AF37"
PALE = "#FFF2A8"
RED = "#FF665E"
VIOLET = "#C28BE0"
CYAN = "#62D9E8"
GRAY = "#AAB4C3"

# Goetic order 36–72.  The first 35 remain the personal cohorts of the seven
# sin lords; these later spirits are unaffiliated "roaming pillars" encountered
# only inside the endless corridor.  English slugs follow the common Goetia
# spellings while Chinese display names follow the pack's concise transliteration.
WANDERING_SPIRITS = (
    # number, stable slug, display name, combat role
    (36, "stolas", "斯托拉斯", 3), (37, "phenex", "菲尼克斯", 5),
    (38, "halphas", "哈帕斯", 1), (39, "malphas", "玛帕斯", 1),
    (40, "raum", "劳姆", 2), (41, "focalor", "佛卡洛", 2),
    (42, "vepar", "威沛", 2), (43, "sabnock", "撒布诺克", 1),
    (44, "shax", "沙克斯", 4), (45, "vine", "拜恩", 1),
    (46, "bifrons", "比弗隆斯", 3), (47, "uvall", "华尔", 4),
    (48, "haagenti", "哈艮地", 3), (49, "crocell", "克罗赛尔", 2),
    (50, "furcas", "富卡斯", 5), (51, "balam", "巴拉姆", 5),
    (52, "alloces", "安洛先", 1), (53, "caim", "卡米奥", 5),
    (54, "murmur", "毛莫", 3), (55, "orobas", "欧洛巴士", 3),
    (56, "gremory", "格莫瑞", 4), (57, "ose", "欧塞", 4),
    (58, "amy", "阿米", 3), (59, "orias", "欧利亚斯", 4),
    (60, "vapula", "瓦布拉", 1), (61, "zagan", "撒共", 3),
    (62, "valac", "瓦拉克", 2), (63, "andras", "安德拉斯", 5),
    (64, "haures", "浩瑞士", 5), (65, "andrealphus", "安德雷斐斯", 4),
    (66, "cimejes", "锡蒙利", 1), (67, "amdusias", "安度西亚斯", 5),
    (68, "belial_68", "贝利尔·王影", 1), (69, "decarabia", "单卡拉比", 2),
    (70, "seere", "系尔", 2), (71, "dantalion", "但他林", 4),
    (72, "andromalius", "安杜马里", 2),
)


def load_config():
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    required = ("boss_interval", "roster_cycle", "reward_window_ticks",
                "intermission_ticks", "start_party_radius", "active_radius",
                "enemy_leash_radius", "idle_abort_ticks", "spawn_offsets",
                "boss_offset", "difficulty", "reward_quality")
    missing = [key for key in required if key not in cfg]
    if missing:
        raise RuntimeError("endless config missing: " + ", ".join(missing))
    if cfg["boss_interval"] != 5 or cfg["roster_cycle"] != 72:
        raise RuntimeError("endless mode contract requires boss_interval=5 and roster_cycle=72")
    if len(cfg["spawn_offsets"]) != 5 or any(len(v) != 3 for v in cfg["spawn_offsets"]):
        raise RuntimeError("spawn_offsets must contain five [x,y,z] vectors")
    if len(cfg["boss_offset"]) != 3:
        raise RuntimeError("boss_offset must be [x,y,z]")
    if cfg["enemy_leash_radius"] >= cfg["active_radius"]:
        raise RuntimeError("enemy leash must be smaller than active radius")
    return cfg


CFG = load_config()


def fpath(rel):
    return FUNC / Path(rel)


def read(rel):
    return fpath(rel).read_text(encoding="utf-8")


def write(rel, content):
    target = fpath(rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def comp(value, color="white", bold=False, click=None, hover=None):
    out = {"text": value, "color": color, "bold": bold, "italic": False}
    if click:
        out["click_event"] = {"action": "run_command", "command": click}
    if hover:
        out["hover_event"] = {"action": "show_text", "value": {"text": hover, "color": GRAY, "italic": False}}
    return out


def score(name, objective, color="white", bold=False):
    return {"score": {"name": name, "objective": objective}, "color": color,
            "bold": bold, "italic": False}


def raw(*parts):
    return json.dumps([""] + list(parts), ensure_ascii=False, separators=(",", ":"))


def tell(selector, *parts):
    return "tellraw %s %s" % (selector, raw(*parts))


def title(selector, channel, *parts):
    return "title %s %s %s" % (selector, channel, raw(*parts))


def reset_tree():
    target = fpath("endless")
    if target.is_dir():
        shutil.rmtree(target)


def patch_load_and_tick():
    objectives = (
        ("rpg_end_id", "dummy"), ("rpg_end_floor", "dummy"),
        ("rpg_end_state", "dummy"), ("rpg_end_time", "dummy"),
        ("rpg_end_idle", "dummy"), ("rpg_end_pick", "trigger"),
        ("rpg_end_leave", "trigger"), ("rpg_end_claim", "dummy"),
        ("rpg_end_best", "dummy"), ("rpg_end_power", "dummy"),
        ("rpg_end_vital", "dummy"), ("rpg_end_tmp", "dummy"),
    )
    rel = "command/soreboard.mcfunction"
    lines = [line for line in read(rel).splitlines()
             if not any(("scoreboard objectives add " + name + " ") in line for name, _kind in objectives)]
    lines += ["scoreboard objectives add %s %s" % pair for pair in objectives]
    write(rel, "\n".join(lines))

    rel = "command/bossbar.mcfunction"
    lines = [line for line in read(rel).splitlines() if "rpg:endless" not in line]
    lines += [
        "bossbar add rpg:endless " + raw(comp("无尽驱魔 · 七柱回廊", GOLD, True)),
        "bossbar set rpg:endless max 5",
        "bossbar set rpg:endless value 0",
        "bossbar set rpg:endless color yellow",
        "bossbar set rpg:endless style notched_10",
        "bossbar set rpg:endless visible true",
    ]
    write(rel, "\n".join(lines))

    rel = "exorcism.mcfunction"
    lines = [line for line in read(rel).splitlines()
             if "function rpg:endless/tick" not in line
             and "function rpg:endless/member/stale_cleanup" not in line
             and "无尽驱魔控制器" not in line]
    lines += ["", "# 无尽驱魔控制器：公共 Bossbar 只允许一个活动实例。",
              "execute as @a[tag=rpg.end.member] unless entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run function rpg:endless/member/stale_cleanup",
              "execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run execute as @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] at @s run function rpg:endless/tick"]
    write(rel, "\n".join(lines))


def patch_competing_mode_and_panel():
    rel = "campaign/beelzebub/start.mcfunction"
    guard = "execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run " + tell("@s", comp("[回廊封锁] ", "#FF806B", True), comp("无尽副本正在运行，暂时不能开启第一章。", "#706B5E"))
    src = "\n".join(line for line in read(rel).splitlines() if "[回廊封锁]" not in line)
    write(rel, guard + "\n" + src)

    rel = "panel/open.mcfunction"
    src = read(rel)
    button_line = tell("@s", comp("[无尽副本]", VIOLET, True, "/trigger rpg_panel set 7"), comp("  "),
                       comp("逐层挑战 · 三选一成长 · 每五层领主战", GRAY))
    if button_line not in src:
        lines = src.splitlines()
        indices = [index for index, line in enumerate(lines) if "切走再切回面板" in line]
        if len(indices) != 1:
            raise RuntimeError("player panel insertion point changed")
        lines.insert(indices[0], button_line)
        write(rel, "\n".join(lines))

    rel = "panel/tick.mcfunction"
    src = read(rel)
    route = "execute if score @s rpg_panel matches 7 run function rpg:panel/endless"
    if route not in src:
        anchor = "execute if score @s rpg_panel matches 6 run function rpg:panel/help"
        if anchor not in src:
            raise RuntimeError("player panel route point changed")
        write(rel, src.replace(anchor, anchor + "\n" + route, 1))
        src = read(rel)
    extra_routes = (
        "execute if score @s rpg_panel matches 16 run function rpg:endless/start",
        "execute if score @s rpg_panel matches 17 run function rpg:endless/join",
    )
    lines = [line for line in src.splitlines() if line not in extra_routes]
    reset = "execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0"
    if reset not in lines:
        raise RuntimeError("player panel reset point changed")
    index = lines.index(reset)
    lines[index:index] = list(extra_routes)
    write(rel, "\n".join(lines))

    write("panel/endless.mcfunction", "\n".join([
        tell("@s", comp("+------ 无尽驱魔 · 七柱回廊 ------+", GOLD, True)),
        tell("@s", comp("历史最深层数 ", "gray"), score("@s", "rpg_end_best", PALE, True),
             comp("　每 5 层进入七罪领主战", "dark_gray")),
        tell("@s", comp("72 柱完整轮换；直属罪仆与游离魔神在同层不会重名。", GRAY)),
        tell("@s", comp("[开启副本]", "#B5D957", True, "/trigger rpg_panel set 16", "以当前位置建立回廊原点"), comp("  "),
             comp("[加入附近]", CYAN, True, "/trigger rpg_panel set 17", "加入 16 格内正在运行的副本"), comp("  "),
             comp("[离开]", RED, True, "/trigger rpg_end_leave set 1")),
        tell("@s", comp("奖励路线：圣恩强化生存，断罪强化输出，遗珍立即取得战利品。", "gray")),
        tell("@s", comp("[返回面板]", GOLD, True, "/trigger rpg_panel set 8")),
    ]))


def suppress_endless_summon_spam():
    for path in (fpath("minion/summon")).rglob("*.mcfunction"):
        if path.name == "all.mcfunction":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        changed = False
        for index, line in enumerate(lines):
            if line.startswith("tellraw @a["):
                lines[index] = "execute unless entity @s[tag=rpg.end.controller] run " + line
                changed = True
        if changed:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def build_entrypoints():
    radius = CFG["start_party_radius"]
    active = CFG["active_radius"]
    write("endless/start.mcfunction", "\n".join([
        "execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run " + tell("@s", comp("[回廊占用] ", RED, True), comp("已有无尽副本正在运行；请加入或等待其结束。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run " + tell("@s", comp("[章节占用] ", RED, True), comp("第一章实例运行期间不能开启无尽副本。", GRAY)),
        "scoreboard players add #next rpg_end_id 1",
        "execute if score #next rpg_end_id matches ..0 run scoreboard players set #next rpg_end_id 1",
        "execute as @a[tag=rpg.end.member] run function rpg:endless/member/stale_cleanup",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.end.controller\",\"rpg.end.controller.new\"]}",
        "data modify entity @e[type=minecraft:marker,tag=rpg.end.controller.new,distance=..2,sort=nearest,limit=1] Rotation set from entity @s Rotation",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.end.controller.new,distance=..2,sort=nearest,limit=1] rpg_end_id = #next rpg_end_id",
        "execute as @e[type=minecraft:marker,tag=rpg.end.controller.new,distance=..2,sort=nearest,limit=1] at @s run function rpg:endless/setup",
    ]))

    write("endless/setup.mcfunction", "\n".join([
        "tag @s remove rpg.end.controller.new",
        "tag @s add rpg.end.controller.current",
        "scoreboard players set @s rpg_end_floor 1",
        "scoreboard players set @s rpg_end_state 0",
        "scoreboard players set @s rpg_end_time 0",
        "scoreboard players set @s rpg_end_idle 0",
        "tag @a[distance=..%d,gamemode=!spectator] add rpg.end.member" % radius,
        "tag @a[tag=rpg.end.member,distance=..%d,gamemode=!spectator] add rpg.end.member.current" % radius,
        "scoreboard players operation @a[tag=rpg.end.member.current,distance=..%d] rpg_end_id = @s rpg_end_id" % radius,
        "scoreboard players set @a[tag=rpg.end.member.current,distance=..%d] rpg_end_power 0" % radius,
        "scoreboard players set @a[tag=rpg.end.member.current,distance=..%d] rpg_end_vital 0" % radius,
        "scoreboard players set @a[tag=rpg.end.member.current,distance=..%d] rpg_end_claim 0" % radius,
        "execute as @a[tag=rpg.end.member.current,distance=..%d] run function rpg:endless/member/clear_boons" % radius,
        "bossbar set rpg:endless players @a[tag=rpg.end.member.current,distance=..%d]" % active,
        "playsound minecraft:block.end_portal.spawn master @a[tag=rpg.end.member.current,distance=..%d] ~ ~ ~ 0.8 0.72" % radius,
        "title @a[tag=rpg.end.member.current,distance=..%d] times 10 45 15" % radius,
        title("@a[tag=rpg.end.member.current,distance=..%d]" % radius, "title", comp("七柱回廊", GOLD, True)),
        title("@a[tag=rpg.end.member.current,distance=..%d]" % radius, "subtitle", comp("无尽驱魔协议已建立", VIOLET)),
        tell("@a[tag=rpg.end.member.current,distance=..%d]" % radius, comp("[回廊协议] ", GOLD, True), comp("每层清除不同编队，随后选择一项个人奖励；第 5 层起每五层迎战一位罪之领主。", GRAY)),
    ]))

    write("endless/join.mcfunction", "\n".join([
        "execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller,distance=..16,sort=nearest,limit=1] run return run " + tell("@s", comp("[无法加入] ", RED, True), comp("附近 16 格没有活动回廊控制器。", GRAY)),
        "tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current",
        "tag @e[type=minecraft:marker,tag=rpg.end.controller,distance=..16,sort=nearest,limit=1] add rpg.end.controller.current",
        "execute if entity @s[tag=rpg.end.member] run function rpg:endless/member/stale_cleanup",
        "tag @s add rpg.end.member",
        "tag @s add rpg.end.member.current",
        "scoreboard players operation @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id",
        "scoreboard players set @s rpg_end_power 0",
        "scoreboard players set @s rpg_end_vital 0",
        "scoreboard players set @s rpg_end_claim 1",
        "scoreboard players set @s rpg_end_pick 0",
        tell("@s", comp("[已加入] ", CYAN, True), comp("从下一层奖励开始参与选择。", GRAY)),
    ]))

    write("endless/leave.mcfunction", "\n".join([
        "scoreboard players set @s rpg_end_leave 0",
        "function rpg:endless/member/clear_boons",
        "tag @s remove rpg.end.member",
        "tag @s remove rpg.end.member.current",
        tell("@s", comp("[已离开] ", RED, True), comp("本轮圣恩与断罪层数已冻结；历史最深层保留。", GRAY)),
    ]))

    write("endless/abort.mcfunction", "\n".join([
        "execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller,distance=..%d,sort=nearest,limit=1] run return run " % active + tell("@s", comp("[无活动副本]", GRAY)),
        "tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current",
        "tag @e[type=minecraft:marker,tag=rpg.end.controller,distance=..%d,sort=nearest,limit=1] add rpg.end.controller.current" % active,
        "execute as @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] at @s run function rpg:endless/cleanup",
    ]))

    write("endless/cleanup.mcfunction", "\n".join([
        tell("@a[tag=rpg.end.member.current,distance=..%d]" % active, comp("[回廊闭合] ", RED, True), comp("本次挑战已结束，历史最深层记录保留。", GRAY)),
        "tp @e[tag=rpg.end.enemy] ~ -200 ~",
        "kill @e[tag=rpg.end.enemy]",
        "execute as @a[tag=rpg.end.member.current] run function rpg:endless/member/stale_cleanup",
        "bossbar set rpg:endless players",
        "bossbar set rpg:endless value 0",
        "kill @s",
    ]))

    write("endless/member/clear_boons.mcfunction", """# 只移除本模式自己的可逆属性，不触碰玩家原有药水效果。
attribute @s minecraft:max_health modifier remove rpg:endless/vital_health
attribute @s minecraft:armor modifier remove rpg:endless/vital_armor
attribute @s minecraft:knockback_resistance modifier remove rpg:endless/vital_anchor
attribute @s minecraft:attack_damage modifier remove rpg:endless/power_damage
attribute @s minecraft:movement_speed modifier remove rpg:endless/power_speed
""")
    write("endless/member/stale_cleanup.mcfunction", """function rpg:endless/member/clear_boons
tag @s remove rpg.end.member
tag @s remove rpg.end.member.current
scoreboard players set @s rpg_end_pick 0
scoreboard players set @s rpg_end_leave 0
scoreboard players set @s rpg_end_claim 1
scoreboard players set @s rpg_end_power 0
scoreboard players set @s rpg_end_vital 0
""")


def build_tick():
    active = CFG["active_radius"]
    leash = CFG["enemy_leash_radius"]
    idle = CFG["idle_abort_ticks"]
    reward_ticks = CFG["reward_window_ticks"]
    intermission = CFG["intermission_ticks"]
    write("endless/tick.mcfunction", "\n".join([
        "tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current",
        "tag @s add rpg.end.controller.current",
        "tag @a remove rpg.end.member.current",
        "execute as @a[tag=rpg.end.member] if score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run tag @s add rpg.end.member.current",
        "execute as @a[tag=rpg.end.member,tag=!rpg.end.member.current] run function rpg:endless/member/stale_cleanup",
        "scoreboard players operation #floor rpg_end_tmp = @s rpg_end_floor",
        "bossbar set rpg:endless players @a[tag=rpg.end.member.current,distance=..%d,gamemode=!spectator]" % active,
        "scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_leave",
        "execute as @a[tag=rpg.end.member.current,scores={rpg_end_leave=1..}] run function rpg:endless/leave",
        "execute if entity @a[tag=rpg.end.member.current,distance=..%d,gamemode=!spectator,limit=1] run scoreboard players set @s rpg_end_idle 0" % active,
        "execute unless entity @a[tag=rpg.end.member.current,distance=..%d,gamemode=!spectator,limit=1] run scoreboard players add @s rpg_end_idle 1" % active,
        "execute if score @s rpg_end_idle matches %d.. run return run function rpg:endless/cleanup" % idle,
        "execute unless entity @a[tag=rpg.end.member.current,distance=..%d,gamemode=!spectator,limit=1] run return 0" % active,
        "execute if score @s rpg_end_state matches 0 run function rpg:endless/state/prepare",
        "execute if score @s rpg_end_state matches 1 run function rpg:endless/state/combat",
        "execute if score @s rpg_end_state matches 2 run function rpg:endless/state/reward",
        "execute if score @s rpg_end_state matches 3 run function rpg:endless/state/intermission",
    ]))

    write("endless/state/prepare.mcfunction", "\n".join([
        "scoreboard players add @s rpg_end_time 1",
        "execute if score @s rpg_end_time matches 80.. run function rpg:endless/floor/begin",
    ]))
    write("endless/state/combat.mcfunction", "\n".join([
        "scoreboard players add @s rpg_end_time 1",
        "function rpg:endless/enemy/refresh",
        "tp @e[tag=rpg.end.enemy.current,distance=%g..] ~ ~1 ~" % (leash + 0.01),
        "execute store result score #alive rpg_end_tmp if entity @e[tag=rpg.end.enemy.current]",
        "execute store result bossbar rpg:endless value run scoreboard players get #alive rpg_end_tmp",
        "bossbar set rpg:endless name " + raw(comp("回廊清剿｜第 ", GOLD, True), score("#floor", "rpg_end_tmp", PALE, True), comp(" 层　剩余 ", GRAY), score("#alive", "rpg_end_tmp", RED, True)),
        "execute if score @s rpg_end_time matches 20.. unless entity @e[tag=rpg.end.enemy.current,limit=1] run function rpg:endless/floor/clear",
    ]))
    write("endless/state/reward.mcfunction", "\n".join([
        "scoreboard players add @s rpg_end_time 1",
        "scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_pick",
        "execute as @a[tag=rpg.end.member.current,scores={rpg_end_claim=0,rpg_end_pick=1..3}] run function rpg:endless/reward/claim",
        "execute if score @s rpg_end_time matches %d.. run function rpg:endless/reward/timeout" % reward_ticks,
        "execute unless entity @a[tag=rpg.end.member.current,scores={rpg_end_claim=0},limit=1] run function rpg:endless/reward/close",
    ]))
    write("endless/state/intermission.mcfunction", "\n".join([
        "scoreboard players add @s rpg_end_time 1",
        "execute if score @s rpg_end_time matches %d.. run function rpg:endless/floor/begin" % intermission,
    ]))
    write("endless/enemy/refresh.mcfunction", "\n".join([
        "tag @e[tag=rpg.end.enemy] remove rpg.end.enemy.current",
        "execute as @e[tag=rpg.end.enemy] if score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run tag @s add rpg.end.enemy.current",
    ]))


def roster():
    out = []
    for lord_index, lord in LORDS.items():
        for role_index, spirit in enumerate(lord["spirits"], 1):
            out.append({"lord": lord_index, "slug": lord["slug"], "spirit": spirit[0],
                        "name": spirit[1], "role": role_index,
                        "function": "rpg:minion/summon/%s/%s" % (lord["slug"], spirit[0])})
    for offset, (number, slug, name, role_index) in enumerate(WANDERING_SPIRITS):
        lord_index = offset % 7 + 1
        out.append({"lord": lord_index, "slug": "roaming", "spirit": slug,
                    "name": name, "role": role_index, "number": number,
                    "function": "rpg:endless/summon/%s" % slug})
    return out


def wandering_name(lord, role, name):
    return json.dumps(["",
        {"text": "[游柱·%s] " % role["name"], "color": lord["base"], "bold": True, "italic": False},
        {"text": name, "color": lord["light"], "bold": False, "italic": False},
    ], ensure_ascii=False, separators=(",", ":"))


def build_wandering_summons():
    """Generate order 36–72 as endless-only combatants using five clear jobs."""
    for offset, (number, slug, name, role_index) in enumerate(WANDERING_SPIRITS):
        lord_index = offset % 7 + 1
        lord, role = LORDS[lord_index], ROLES[role_index]
        no_ai = ",NoAI:1b" if role.get("no_ai") else (",NoAI:0b" if role_index == 4 else "")
        snbt = (
            "{Tags:[\"rpg.demon.minion\",\"rpg.demon.minion.new\",\"rpg.demon.minion.roaming\","
            "\"rpg.demon.minion.lord%d\",\"rpg.demon.minion.role%d\"],CanJoinRaid:0b,"
            "PersistenceRequired:1b,CustomNameVisible:1b%s,CustomName:%s,Health:%sf,"
            "active_effects:[{id:\"minecraft:fire_resistance\",duration:-1,amplifier:0,show_particles:0b}],"
            "attributes:[{id:\"minecraft:max_health\",base:%sf},{id:\"minecraft:attack_damage\",base:%sf},"
            "{id:\"minecraft:armor\",base:%sf},{id:\"minecraft:follow_range\",base:36f},"
            "{id:\"minecraft:movement_speed\",base:%sf},{id:\"minecraft:knockback_resistance\",base:0.35f}],"
            "equipment:{mainhand:{id:\"%s\",count:1}},drop_chances:{mainhand:0f},"
            "DeathLootTable:\"minecraft:empty\"}"
        ) % (lord_index, role_index, no_ai, wandering_name(lord, role, name), role["health"],
             role["health"], role["attack"], role["armor"], role["speed"], role["weapon"])
        selector = "@e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest]"
        write("endless/summon/%s.mcfunction" % slug, "\n".join([
            "# 第 %d 柱 · %s；游离魔神，职责为%s，亲和%s。" % (number, name, role["name"], lord["lord"]),
            "summon minecraft:%s ~ ~ ~ %s" % (role["entity"], snbt),
            "scoreboard players set %s rpg_mn_lord %d" % (selector, lord_index),
            "scoreboard players set %s rpg_mn_role %d" % (selector, role_index),
            "scoreboard players set %s rpg_mn_owner 0" % selector,
            "scoreboard players set %s rpg_mn_cd %d" % (selector, role["cd"] // 2 + offset % 31),
            "scoreboard players set %s rpg_mn_cast 0" % selector,
            "tag %s remove rpg.demon.minion.new" % selector,
            "particle %s ~ ~1 ~ 0.45 0.65 0.45 0.025 8" % lord["particle"],
        ]))


def summon_capture(entry, offset, minimum):
    x, y, z = offset
    pos = "^%g ^%g ^%g" % (x, y, z)
    prefix = "execute if score #spawn rpg_end_tmp matches %d.. positioned %s run " % (minimum, pos)
    selector = "@e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1]"
    return [
        prefix + "function " + entry["function"],
        prefix + "tag %s add rpg.end.enemy" % selector,
        prefix + "tag %s add rpg.end.enemy.current" % selector,
        prefix + "scoreboard players operation %s rpg_end_id = @s rpg_end_id" % selector,
        prefix + "tag %s add rpg.end.preexisting" % selector,
    ]


def build_floor_deck():
    spirits = roster()
    cycle = CFG["roster_cycle"]
    if len(spirits) != cycle or len({item["spirit"] for item in spirits}) != cycle:
        raise RuntimeError("72-pillar roster is incomplete or duplicated")
    role_buckets = {role: [item for item in spirits if item["role"] == role]
                    for role in range(1, 6)}
    if sorted(len(items) for items in role_buckets.values()) != [14, 14, 14, 15, 15]:
        raise RuntimeError("72-pillar five-role distribution changed")
    phase = (0, 3, 6, 9, 12)
    for floor in range(1, cycle + 1):
        lineup = [role_buckets[role][((floor - 1) + phase[role - 1]) % len(role_buckets[role])]
                  for role in range(1, 6)]
        lines = ["# 第 %d 号编队：%s" % (floor, " / ".join(item["name"] for item in lineup)),
                 "tag @e[tag=rpg.demon.minion] add rpg.end.preexisting"]
        for slot, (entry, position) in enumerate(zip(lineup, CFG["spawn_offsets"]), 1):
            lines += summon_capture(entry, position, slot)
        lines += ["tag @e[tag=rpg.demon.minion] remove rpg.end.preexisting",
                  "execute as @e[tag=rpg.end.enemy.current] run function rpg:endless/enemy/scale"]
        write("endless/deck/%d.mcfunction" % floor, "\n".join(lines))
    write("endless/deck/dispatch.mcfunction", "\n".join(
        "execute if score #deck rpg_end_tmp matches %d run function rpg:endless/deck/%d" % (n, n)
        for n in range(1, cycle + 1)))


def build_floor_logic():
    begin = [
        "scoreboard players set @s rpg_end_state 1",
        "scoreboard players set @s rpg_end_time 0",
        "scoreboard players operation #floor rpg_end_tmp = @s rpg_end_floor",
        "scoreboard players operation #ordinary rpg_end_tmp = @s rpg_end_floor",
        "scoreboard players operation #skipped rpg_end_tmp = @s rpg_end_floor",
        "scoreboard players set #five rpg_end_tmp 5",
        "scoreboard players operation #skipped rpg_end_tmp /= #five rpg_end_tmp",
        "scoreboard players operation #ordinary rpg_end_tmp -= #skipped rpg_end_tmp",
        "scoreboard players operation #deck rpg_end_tmp = #ordinary rpg_end_tmp",
        "scoreboard players remove #deck rpg_end_tmp 1",
        "scoreboard players set #cycle_size rpg_end_tmp %d" % CFG["roster_cycle"],
        "scoreboard players operation #deck rpg_end_tmp %= #cycle_size rpg_end_tmp",
        "scoreboard players add #deck rpg_end_tmp 1",
        "scoreboard players operation #cycle rpg_end_tmp = #ordinary rpg_end_tmp",
        "scoreboard players remove #cycle rpg_end_tmp 1",
        "scoreboard players operation #cycle rpg_end_tmp /= #cycle_size rpg_end_tmp",
        "scoreboard players add #cycle rpg_end_tmp 1",
        "scoreboard players operation #tier rpg_end_tmp = @s rpg_end_floor",
        "scoreboard players add #tier rpg_end_tmp 4",
        "scoreboard players operation #tier rpg_end_tmp /= #five rpg_end_tmp",
        "execute if score #tier rpg_end_tmp matches 21.. run scoreboard players set #tier rpg_end_tmp 20",
        "scoreboard players operation #mod rpg_end_tmp = @s rpg_end_floor",
        "scoreboard players operation #mod rpg_end_tmp %= #five rpg_end_tmp",
        "scoreboard players set #boss rpg_end_tmp 0",
        "execute if score #mod rpg_end_tmp matches 0 run scoreboard players set #boss rpg_end_tmp 1",
        "execute store result score #party rpg_end_tmp if entity @a[tag=rpg.end.member.current,distance=..%d,gamemode=!spectator]" % CFG["active_radius"],
        "scoreboard players set #spawn rpg_end_tmp 3",
        "execute if score #floor rpg_end_tmp matches %d.. run scoreboard players set #spawn rpg_end_tmp 4" % CFG["difficulty"]["fourth_enemy_floor"],
        "execute if score #floor rpg_end_tmp matches %d.. run scoreboard players set #spawn rpg_end_tmp 5" % CFG["difficulty"]["fifth_enemy_floor"],
        "execute if score #party rpg_end_tmp matches 2.. if score #spawn rpg_end_tmp matches ..3 run scoreboard players set #spawn rpg_end_tmp 4",
        "execute if score #party rpg_end_tmp matches 4.. run scoreboard players set #spawn rpg_end_tmp 5",
        "scoreboard players set @a[tag=rpg.end.member.current] rpg_end_pick 0",
        "execute as @a[tag=rpg.end.member.current,distance=..%d,gamemode=!spectator] at @s run function rpg:endless/member/apply_boons" % CFG["active_radius"],
        "bossbar set rpg:endless color red",
        "execute if score #boss rpg_end_tmp matches 0 store result bossbar rpg:endless max run scoreboard players get #spawn rpg_end_tmp",
        "execute if score #boss rpg_end_tmp matches 0 store result bossbar rpg:endless value run scoreboard players get #spawn rpg_end_tmp",
        "execute if score #boss rpg_end_tmp matches 1 run bossbar set rpg:endless max 1",
        "execute if score #boss rpg_end_tmp matches 1 run bossbar set rpg:endless value 1",
        "bossbar set rpg:endless name " + raw(comp("七柱回廊｜第 ", GOLD, True), score("#floor", "rpg_end_tmp", PALE, True), comp(" 层", GOLD, True), comp("　轮回 ", "dark_gray"), score("#cycle", "rpg_end_tmp", VIOLET)),
        "title @a[tag=rpg.end.member.current,distance=..%d] times 5 35 10" % CFG["active_radius"],
        title("@a[tag=rpg.end.member.current,distance=..%d]" % CFG["active_radius"], "title", comp("第 ", GOLD), score("#floor", "rpg_end_tmp", PALE, True), comp(" 层", GOLD)),
        "execute if score #boss rpg_end_tmp matches 0 run " + title("@a[tag=rpg.end.member.current,distance=..%d]" % CFG["active_radius"], "subtitle", comp("所罗门七十二柱 · 编队不重复", GRAY)),
        "execute if score #boss rpg_end_tmp matches 1 run " + title("@a[tag=rpg.end.member.current,distance=..%d]" % CFG["active_radius"], "subtitle", comp("领主层 · 七罪降临", RED, True)),
        "execute if score #boss rpg_end_tmp matches 0 run function rpg:endless/deck/dispatch",
        "execute if score #boss rpg_end_tmp matches 1 run function rpg:endless/boss/dispatch",
        "function rpg:endless/enemy/refresh",
    ]
    write("endless/floor/begin.mcfunction", "\n".join(begin))

    write("endless/floor/clear.mcfunction", "\n".join([
        "scoreboard players set @s rpg_end_state 2",
        "scoreboard players set @s rpg_end_time 0",
        "scoreboard players set @a[tag=rpg.end.member.current] rpg_end_claim 0",
        "scoreboard players set @a[tag=rpg.end.member.current] rpg_end_pick 0",
        "scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_pick",
        "execute as @a[tag=rpg.end.member.current] if score @s rpg_end_best < #floor rpg_end_tmp run scoreboard players operation @s rpg_end_best = #floor rpg_end_tmp",
        "execute as @a[tag=rpg.end.member.current] run function rpg:endless/reward/base_xp",
        "bossbar set rpg:endless value 0",
        "bossbar set rpg:endless color yellow",
        "bossbar set rpg:endless name " + raw(comp("层结算｜第 ", GOLD, True), score("#floor", "rpg_end_tmp", PALE, True), comp(" 层 · 选择一项恩赐", GOLD)),
        "playsound minecraft:ui.toast.challenge_complete player @a[tag=rpg.end.member.current,distance=..%d] ~ ~ ~ 0.75 1.15" % CFG["active_radius"],
        "execute as @a[tag=rpg.end.member.current] run function rpg:endless/reward/open",
    ]))


def build_bosses():
    bx, by, bz = CFG["boss_offset"]
    lines = [
        "scoreboard players operation #lord rpg_end_tmp = @s rpg_end_floor",
        "scoreboard players operation #lord rpg_end_tmp /= #five rpg_end_tmp",
        "scoreboard players remove #lord rpg_end_tmp 1",
        "scoreboard players set #seven rpg_end_tmp 7",
        "scoreboard players operation #lord rpg_end_tmp %= #seven rpg_end_tmp",
        "scoreboard players add #lord rpg_end_tmp 1",
    ]
    for lord in range(1, 8):
        lines.append("execute if score #lord rpg_end_tmp matches %d positioned ^%g ^%g ^%g run function rpg:endless/boss/%d" % (lord, bx, by, bz, lord))
    write("endless/boss/dispatch.mcfunction", "\n".join(lines))

    for lord_index, lord in LORDS.items():
        selector = "@e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.end.preexisting,distance=..4,sort=nearest,limit=1]"
        write("endless/boss/%d.mcfunction" % lord_index, "\n".join([
            "tag @e[type=minecraft:vindicator,tag=rpg.advent] add rpg.end.preexisting",
            "function rpg:taint/lord%d" % lord_index,
            "tag %s add rpg.end.enemy" % selector,
            "tag %s add rpg.end.enemy.current" % selector,
            "tag %s add rpg.end.boss" % selector,
            "scoreboard players operation %s rpg_end_id = @s rpg_end_id" % selector,
            "tag @e[type=minecraft:vindicator,tag=rpg.advent] remove rpg.end.preexisting",
            "execute as @e[tag=rpg.end.enemy.current,tag=rpg.end.boss] run function rpg:endless/enemy/scale",
            tell("@a[tag=rpg.end.member.current,distance=..%d]" % CFG["active_radius"], comp("[领主降临] ", lord["base"], True), comp(lord["lord"] + " ", lord["light"], False), comp("封锁本层出口。", GRAY)),
        ]))


def build_scaling():
    lines = ["# 难度每五层提高一级；100 层后维持第 20 级数值，但轮回与奖励继续推进。"]
    for tier in range(1, 21):
        for role_index, role in ROLES.items():
            factor = 1.0 + 0.18 * (tier - 1)
            hp = int(round(role["health"] * factor))
            attack = round(role["attack"] * (1.0 + 0.08 * (tier - 1)), 2)
            armor = round(min(28.0, role["armor"] + 0.55 * (tier - 1)), 2)
            gate = "execute unless entity @s[tag=rpg.end.boss] if score #tier rpg_end_tmp matches %d if score @s rpg_mn_role matches %d run " % (tier, role_index)
            lines += [
                gate + "attribute @s minecraft:max_health base set %d" % hp,
                gate + "attribute @s minecraft:attack_damage base set %g" % attack,
                gate + "attribute @s minecraft:armor base set %g" % armor,
                gate + "data merge entity @s {Health:%df}" % hp,
            ]
        boss_hp = int(round(700 * (1.0 + 0.22 * (tier - 1))))
        boss_attack = round(11 * (1.0 + 0.07 * (tier - 1)), 2)
        gate = "execute if entity @s[tag=rpg.end.boss] if score #tier rpg_end_tmp matches %d run " % tier
        lines += [
            gate + "attribute @s minecraft:max_health base set %d" % boss_hp,
            gate + "attribute @s minecraft:attack_damage base set %g" % boss_attack,
            gate + "attribute @s minecraft:armor base set %g" % min(30, 8 + 0.7 * (tier - 1)),
            gate + "data merge entity @s {Health:%df}" % boss_hp,
        ]
    write("endless/enemy/scale.mcfunction", "\n".join(lines))


def build_rewards():
    open_lines = [
        tell("@s", comp("+-------- 层间赐予 --------+", GOLD, True)),
        tell("@s", comp("第 ", "gray"), score("#floor", "rpg_end_tmp", PALE, True), comp(" 层已净空　请选择一项：", "gray")),
        tell("@s", comp("[圣恩]", "#B5D957", True, "/trigger rpg_end_pick set 1", "恢复生命，并永久提高本轮生存恩赐"), comp("　恢复并强化后续生存", GRAY)),
        tell("@s", comp("[断罪]", RED, True, "/trigger rpg_end_pick set 2", "永久提高本轮输出恩赐"), comp("　强化后续伤害与机动", GRAY)),
        tell("@s", comp("[遗珍]", VIOLET, True, "/trigger rpg_end_pick set 3", "立即领取随层数成长的物资"), comp("　立即获得本层战利品", GRAY)),
        tell("@s", comp("20 秒未选择将自动领取遗珍。", "dark_gray")),
    ]
    write("endless/reward/open.mcfunction", "\n".join(open_lines))

    claim = [
        "execute unless score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run return 0",
        "execute if score @s rpg_end_claim matches 1.. run return 0",
        "scoreboard players set @s rpg_end_claim 1",
        "execute if score @s rpg_end_pick matches 1 run function rpg:endless/reward/grace",
        "execute if score @s rpg_end_pick matches 2 run function rpg:endless/reward/judgment",
        "execute if score @s rpg_end_pick matches 3 run function rpg:endless/reward/loot_dispatch",
        "execute if score #boss rpg_end_tmp matches 1 run function rpg:endless/reward/boss_bonus",
        "scoreboard players set @s rpg_end_pick 0",
        "playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.7 1.3",
    ]
    write("endless/reward/claim.mcfunction", "\n".join(claim))
    write("endless/reward/grace.mcfunction", "\n".join([
        "execute if score @s rpg_end_vital matches ..7 run scoreboard players add @s rpg_end_vital 1",
        "effect give @s minecraft:instant_health 1 2 true",
        "effect give @s minecraft:regeneration 12 1 true",
        "function rpg:endless/member/apply_boons",
        tell("@s", comp("[圣恩入档] ", "#B5D957", True), comp("生存恩赐提升至 ", GRAY), score("@s", "rpg_end_vital", PALE, True), comp(" / 8", "dark_gray")),
    ]))
    write("endless/reward/judgment.mcfunction", "\n".join([
        "execute if score @s rpg_end_power matches ..7 run scoreboard players add @s rpg_end_power 1",
        "function rpg:endless/member/apply_boons",
        tell("@s", comp("[断罪入档] ", RED, True), comp("输出恩赐提升至 ", GRAY), score("@s", "rpg_end_power", PALE, True), comp(" / 8", "dark_gray")),
    ]))

    loot_sets = {
        1: ((1, 2), (("gold_ingot", 4), ("emerald", 2), ("experience_bottle", 4))),
        2: ((3, 4), (("iron_block", 2), ("emerald", 5), ("experience_bottle", 8))),
        3: ((5, 7), (("diamond", 2), ("amethyst_shard", 8), ("experience_bottle", 12))),
        4: ((8, 10), (("diamond", 4), ("echo_shard", 1), ("experience_bottle", 16))),
        5: ((11, 14), (("netherite_scrap", 1), ("diamond", 6), ("echo_shard", 2))),
        6: ((15, 19), (("netherite_scrap", 2), ("diamond", 8), ("echo_shard", 4))),
        7: ((20, 20), (("netherite_ingot", 1), ("enchanted_golden_apple", 1), ("echo_shard", 8))),
    }
    dispatch = []
    for index, ((lo, hi), items) in loot_sets.items():
        dispatch.append("execute if score #tier rpg_end_tmp matches %d..%d run function rpg:endless/reward/loot/%d" % (lo, hi, index))
        body = ["give @s minecraft:%s %d" % item for item in items]
        body.append(tell("@s", comp("[遗珍入档] ", VIOLET, True), comp("战利品品质随深度提升。", GRAY)))
        write("endless/reward/loot/%d.mcfunction" % index, "\n".join(body))
    write("endless/reward/loot_dispatch.mcfunction", "\n".join(dispatch))

    xp_lines = []
    for tier in range(1, 21):
        xp_lines.append("execute if score #tier rpg_end_tmp matches %d run scoreboard players add @s rpg_ex_xp %d" % (tier, 4 + tier * 2))
    write("endless/reward/base_xp.mcfunction", "\n".join(xp_lines))

    write("endless/reward/boss_bonus.mcfunction", "\n".join([
        "scoreboard players add @s rpg_ex_xp 12",
        "execute if score #floor rpg_end_tmp matches ..14 run give @s minecraft:diamond 1",
        "execute if score #floor rpg_end_tmp matches 15..29 run give @s minecraft:netherite_scrap 1",
        "execute if score #floor rpg_end_tmp matches 30..49 run give @s minecraft:netherite_scrap 2",
        "execute if score #floor rpg_end_tmp matches 30..49 run give @s minecraft:echo_shard 2",
        "execute if score #floor rpg_end_tmp matches 50.. run give @s minecraft:netherite_ingot 1",
        "execute if score #floor rpg_end_tmp matches 50.. run give @s minecraft:enchanted_golden_apple 1",
        tell("@s", comp("[领主宝库] ", GOLD, True), comp("额外获得 Boss 层战利品与 12 点驱魔阅历。", PALE)),
    ]))

    write("endless/reward/timeout.mcfunction", "\n".join([
        "scoreboard players set @a[tag=rpg.end.member.current,scores={rpg_end_claim=0}] rpg_end_pick 3",
        "execute as @a[tag=rpg.end.member.current,scores={rpg_end_claim=0}] run function rpg:endless/reward/claim",
    ]))
    write("endless/reward/close.mcfunction", "\n".join([
        "scoreboard players set @s rpg_end_state 3",
        "scoreboard players set @s rpg_end_time 0",
        "scoreboard players add @s rpg_end_floor 1",
        "scoreboard players operation #floor rpg_end_tmp = @s rpg_end_floor",
        "bossbar set rpg:endless color purple",
        "bossbar set rpg:endless name " + raw(comp("回廊重构｜下一层 ", VIOLET, True), score("#floor", "rpg_end_tmp", PALE, True), comp("　6 秒", "dark_gray")),
        tell("@a[tag=rpg.end.member.current,distance=..%d]" % CFG["active_radius"], comp("[回廊重构] ", VIOLET, True), comp("六秒后开启第 ", GRAY), score("#floor", "rpg_end_tmp", PALE, True), comp(" 层。", GRAY)),
    ]))

    write("endless/member/apply_boons.mcfunction", "\n".join([
        "function rpg:endless/member/clear_boons",
        "execute if score @s rpg_end_vital matches 1..2 run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 4 add_value",
        "execute if score @s rpg_end_vital matches 3..4 run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 8 add_value",
        "execute if score @s rpg_end_vital matches 3..4 run attribute @s minecraft:armor modifier add rpg:endless/vital_armor 2 add_value",
        "execute if score @s rpg_end_vital matches 5..6 run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 12 add_value",
        "execute if score @s rpg_end_vital matches 5..6 run attribute @s minecraft:armor modifier add rpg:endless/vital_armor 4 add_value",
        "execute if score @s rpg_end_vital matches 7.. run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 16 add_value",
        "execute if score @s rpg_end_vital matches 7.. run attribute @s minecraft:armor modifier add rpg:endless/vital_armor 6 add_value",
        "execute if score @s rpg_end_vital matches 7.. run attribute @s minecraft:knockback_resistance modifier add rpg:endless/vital_anchor 0.1 add_value",
        "execute if score @s rpg_end_power matches 1..2 run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 1 add_value",
        "execute if score @s rpg_end_power matches 3..4 run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 2 add_value",
        "execute if score @s rpg_end_power matches 3..4 run attribute @s minecraft:movement_speed modifier add rpg:endless/power_speed 0.02 add_value",
        "execute if score @s rpg_end_power matches 5..6 run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 4 add_value",
        "execute if score @s rpg_end_power matches 5..6 run attribute @s minecraft:movement_speed modifier add rpg:endless/power_speed 0.04 add_value",
        "execute if score @s rpg_end_power matches 7.. run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 6 add_value",
        "execute if score @s rpg_end_power matches 7.. run attribute @s minecraft:movement_speed modifier add rpg:endless/power_speed 0.06 add_value",
    ]))


def build_debug():
    buttons = [
        tell("@s", comp("+------ 七柱回廊 · 调试台 ------+", GOLD, True)),
        tell("@s", comp("[正式开启]", "#B5D957", True, "/function rpg:endless/start"), comp("  "),
             comp("[加入附近]", CYAN, True, "/function rpg:endless/join"), comp("  "),
             comp("[清理副本]", RED, True, "/function rpg:endless/abort")),
    ]
    for floor in (1, 5, 10, 25, 50, 72, 100):
        buttons.append(tell("@s", comp("[跳至 %d 层]" % floor, VIOLET, True,
                                      "/function rpg:endless/debug/floor/%d" % floor),
                            comp("　%s" % ("Boss层" if floor % 5 == 0 else "普通层"), "dark_gray")))
        write("endless/debug/floor/%d.mcfunction" % floor, "\n".join([
            "execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller,distance=..%d,sort=nearest,limit=1] run return run " % CFG["active_radius"] + tell("@s", comp("[需要副本] ", RED, True), comp("先在附近开启七柱回廊。", GRAY)),
            "tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current",
            "tag @e[type=minecraft:marker,tag=rpg.end.controller,distance=..%d,sort=nearest,limit=1] add rpg.end.controller.current" % CFG["active_radius"],
            "tp @e[tag=rpg.end.enemy] ~ -200 ~",
            "kill @e[tag=rpg.end.enemy]",
            "scoreboard players set @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_floor %d" % floor,
            "scoreboard players set @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_state 0",
            "scoreboard players set @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_time 79",
            tell("@s", comp("[调试跳层] ", VIOLET, True), comp("下一刻进入第 %d 层；不会发放被跳过层数的奖励。" % floor, GRAY)),
        ]))
    buttons.append(tell("@s", comp("所有生成位置均读取 _endless_exorcism_config.json。", "dark_gray")))
    write("endless/debug/menu.mcfunction", "\n".join(buttons))


def emit_pack_config():
    target = DP / "data" / "rpg" / "endless_config.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(CFG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    reset_tree()
    patch_load_and_tick()
    patch_competing_mode_and_panel()
    suppress_endless_summon_spam()
    build_entrypoints()
    build_tick()
    build_wandering_summons()
    build_floor_deck()
    build_floor_logic()
    build_bosses()
    build_scaling()
    build_rewards()
    build_debug()
    emit_pack_config()
    print("endless exorcism: all 72 Goetic spirits / 72 formations / boss every 5 floors / 20 scaling tiers / 3 reward paths")


if __name__ == "__main__":
    main()
