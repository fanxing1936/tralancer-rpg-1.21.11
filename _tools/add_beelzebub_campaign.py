#!/usr/bin/env python3
"""Generate Chapter I: The Vacants / Beelzebub campaign.

One public controller is allowed because the UI has one bossbar, but controller,
participants, scene points, minions, boss and rite all carry rpg_ch1_id. Thus
unrelated nearby players/demons/rites cannot be claimed by the chapter.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

from beelzebub_campaign_config import (
    config_digest,
    item_index,
    iter_positions,
    load_config,
    manifest,
    palette_color,
)

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
FUN = ROOT / "data" / "rpg" / "function"
CONFIG = load_config()
RUNTIME = CONFIG["runtime"]
RECOVERY = RUNTIME["recovery"]
PALETTE = CONFIG["visual"]["palette"]
ACTORS = CONFIG["actors"]
BOSS = ACTORS["boss"]
MINIONS = ACTORS["minions"]
ITEMS = item_index(CONFIG)
SCENE_POINTS = CONFIG["scene_points"]
CHAPTER, CHURCH = PALETTE["chapter"], PALETTE["church"]
BEEL, BEEL_LIGHT = PALETTE["beelzebub"], PALETTE["beelzebub_light"]
ASH, DANGER, GRAY, DARK = PALETTE["ash"], PALETTE["danger"], "gray", "dark_gray"
WITNESS, SEAL, PACT = PALETTE["witness"], PALETTE["seal"], PALETTE["pact"]
ELIMINATE, PANEL, NEXT_HUNT = PALETTE["eliminate"], PALETTE["panel"], PALETTE["next_hunt"]


def actor_position(group, key=None):
    actor = ACTORS[group] if key is None else ACTORS[group][key]
    return actor["spawn"]


def scene(group, key):
    return SCENE_POINTS[group][key]


def function_rel(function_id):
    namespace, rel = function_id.split(":", 1)
    if namespace != "rpg":
        raise ValueError(f"Chapter I can only generate rpg functions: {function_id}")
    return rel + ".mcfunction"


def custom_data_value(item):
    prefix = "minecraft:custom_data~"
    match = item["match"]
    if not match.startswith(prefix):
        raise ValueError(f"Generated Chapter I item needs a custom-data match: {match}")
    return match[len(prefix):]


def write(rel, value):
    p = FUN / rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def read(rel): return (FUN / rel).read_text(encoding="utf-8")
def save(rel, value): (FUN / rel).write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def c(text, color=GRAY, bold=False, **extra):
    out = {"text": text, "color": color, "bold": bold, "italic": False}; out.update(extra); return out


def row(*parts): return json.dumps([""] + list(parts), ensure_ascii=False, separators=(",", ":"))
def tell(target, *parts): return f"tellraw {target} {row(*parts)}"


def button(label, color, value, hover):
    return c(f"[{label}]", color, True,
             click_event={"action": "run_command", "command": f"/trigger rpg_panel set {value}"},
             hover_event={"action": "show_text", "value": c(hover, GRAY)})


def command_button(label, color, command, hover):
    return c(f"[{label}]", color, True,
             click_event={"action": "run_command", "command": command})


def display(text, color, key):
    # Since 1.21.5 text components in entity SNBT are structured values.  row()
    # already returns a valid JSON/SNBT component list; quoting it again turns
    # the list into a literal string and makes the client render the JSON source.
    txt = row(c(text, color, True))
    label_y = CONFIG["visual"]["label_y"]
    view_range = CONFIG["visual"]["label_view_range"]
    return (f"summon minecraft:text_display ~ ~{label_y} ~ {{Tags:[\"rpg.ch1.scene\",\"rpg.ch1.label\","
            f"\"rpg.ch1.{key}.label\",\"rpg.ch1.new\"],billboard:\"center\",see_through:1b,"
            f"shadow:1b,background:0,view_range:{view_range}f,text:{txt}}}")


def owned_spawn(local, key, label, color):
    return [
        f"execute positioned {local} run summon minecraft:marker ~ ~ ~ {{Tags:[\"rpg.ch1.scene\",\"rpg.ch1.point\",\"rpg.ch1.{key}\",\"rpg.ch1.new\"]}}",
        f"scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..{RUNTIME['active_radius']}] rpg_ch1_id = @s rpg_ch1_id",
        f"tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..{RUNTIME['active_radius']}] remove rpg.ch1.new",
        f"execute positioned {local} run {display(label, color, key)}",
        f"scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..{RUNTIME['active_radius']}] rpg_ch1_id = @s rpg_ch1_id",
        f"tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..{RUNTIME['active_radius']}] remove rpg.ch1.new",
    ]


def setup_objectives():
    rel = "command/soreboard.mcfunction"; data = read(rel)
    names = ("rpg_ch1_id", "rpg_ch1_stage", "rpg_ch1_sub", "rpg_ch1_time", "rpg_ch1_obj", "rpg_ch1_choice",
             "rpg_ch1_done", "rpg_ch1_next", "rpg_ch1_replay", "rpg_ch1_reward",
             "rpg_ch1_fail", "rpg_ch1_seen", "rpg_ch1_safe", "rpg_ch1_yaw", "rpg_ch1_guard",
             "rpg_ch1_roster", "rpg_ch1_empty", "rpg_ch1_hp", "rpg_ch1_rescue",
             "rpg_ch1_verdict", "rpg_ch1_session")
    for name in names:
        line = f"scoreboard objectives add {name} dummy"
        if line not in data: data += "\n" + line
    save(rel, data)


def hook_runtime():
    rel = "exorcism.mcfunction"; data = read(rel)
    hook = ("execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run execute as "
            "@e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/tick")
    if hook not in data: data += "\n\n# 第一章：仅在控制器存在时进入一次有界状态机。\n" + hook
    save(rel, data)
    # Campaign actor is a real canonical vacant, but is resolved safely by the
    # story and must never enter the generic tear/transfer/random-lord loop.
    rel = "vacant/vacant.mcfunction"; data = read(rel)
    data = data.replace("tag=rpg.vacant] at @s", "tag=rpg.vacant,tag=!rpg.ch1.vacant.safe] at @s")
    data = data.replace("tag=rpg.vacant,tag=rpg.hurt] at @s", "tag=rpg.vacant,tag=rpg.hurt,tag=!rpg.ch1.vacant.safe] at @s")
    save(rel, data)

    # Record distinct powers only when the caster is the ID-owned chapter boss
    # and the witness is an accepted, present, holy member.
    for n in range(1, 6):
        rel = f"taint/sk4_{n}.mcfunction"; data = read(rel)
        hook = (f"execute if entity @s[tag=rpg.ch1.boss] at @s as @a[tag=rpg.ch1.member,tag=rpg.ch1.party,tag=rpg.holy,distance=..{RUNTIME['witness_radius']},gamemode=!spectator] "
                f"if score @s rpg_ch1_id = @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,sort=nearest,limit=1,distance=..{RUNTIME['witness_radius']}] rpg_ch1_id run function rpg:campaign/beelzebub/witness/skill{n}")
        if hook not in data: data = hook + "\n" + data
        save(rel, data)

    # Existing true-name owners cannot skip this chapter's three-witness gate.
    rel = "inquest/stage1.mcfunction"; data = read(rel)
    lord = BOSS["lord_score"]
    old = f"execute if score @s rpg_dm_lord matches {lord} if entity @a[tag=rpg.name.{lord},distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] run return run function rpg:inquest/bind/{lord}"
    generic = f"execute if entity @s[tag=!rpg.ch1.boss] if score @s rpg_dm_lord matches {lord} if entity @a[tag=rpg.name.{lord},distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] run return run function rpg:inquest/bind/{lord}"
    campaign = f"execute if entity @s[tag=rpg.ch1.boss] if score @s rpg_dm_lord matches {lord} if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,distance=..{RUNTIME['scene_radius']},limit=1] rpg_ch1_id if entity @a[tag=rpg.ch1.member,tag=rpg.name.{lord},distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] run return run function rpg:inquest/bind/{lord}"
    data = data.replace(generic, old).replace(campaign, old)
    if old not in data: raise RuntimeError("canonical Beelzebub bind line missing")
    save(rel, data.replace(old, generic + "\n" + campaign, 1))

    # Stability collapse must recover the chapter checkpoint instead of marking
    # the soul for a generic eliminate drop. Verdict timeout repeats the choice
    # prompt and never silently chooses banishment for the player.
    rel = "inquest/anchor_collapse.mcfunction"; data = read(rel)
    route = ("execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = "
             f"@e[type={BOSS['entity_type']},tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..{RUNTIME['rite_bind_radius']},sort=nearest,limit=1] rpg_ch1_id "
             f"if score @s rpg_rite_id = @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..{RUNTIME['rite_bind_radius']},sort=nearest,limit=1] rpg_rite_id "
             "run return run function rpg:campaign/beelzebub/rite/collapse")
    data = "\n".join(x for x in data.splitlines() if "campaign/beelzebub/rite/collapse" not in x)
    save(rel, route + "\n" + data)
    rel = "inquest/anchor_stage4.mcfunction"; data = read(rel)
    route = "execute if entity @s[tag=rpg.ch1.rite] run return run function rpg:campaign/beelzebub/rite/stage4"
    data = "\n".join(x for x in data.splitlines() if "campaign/beelzebub/rite/stage4" not in x)
    save(rel, route + "\n" + data)
    for kind in ("eliminate", "banish", "seal", "pact"):
        rel = f"inquest/outcome/{kind}.mcfunction"; data = read(rel)
        data = "\n".join(x for x in data.splitlines() if "rpg:campaign/beelzebub/verdict/" not in x)
        route = ("execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = "
                f"@e[type={BOSS['entity_type']},tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..{RUNTIME['rite_bind_radius']},sort=nearest,limit=1] rpg_ch1_id "
                f"if score @s rpg_rite_id = @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..{RUNTIME['rite_bind_radius']},sort=nearest,limit=1] rpg_rite_id "
                 f"run return run function rpg:campaign/beelzebub/verdict/{kind}")
        save(rel, route + "\n" + data)
    rel = "inquest/choice/final.mcfunction"; data = read(rel)
    drop = ("#ch1_choice_ok", "rpg.ch1.choice.player", "campaign/beelzebub/verdict/reject")
    data = "\n".join(x for x in data.splitlines() if not any(token in x for token in drop))
    gate = [
        "scoreboard players set #ch1_choice_ok rpg_ch1_id 0",
        "tag @s add rpg.ch1.choice.player",
        "execute if entity @s[tag=rpg.ch1.member] if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session at @s as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] if score @s rpg_ch1_id = @a[tag=rpg.ch1.choice.player,limit=1] rpg_ch1_id run scoreboard players set #ch1_choice_ok rpg_ch1_id 1",
        "tag @s remove rpg.ch1.choice.player",
        "execute at @s if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..10,limit=1,scores={rpg_ex_stage=4}] if score #ch1_choice_ok rpg_ch1_id matches 0 run return run function rpg:campaign/beelzebub/verdict/reject",
    ]
    save(rel, "\n".join(gate) + "\n" + data)


def hook_panel():
    rel = "panel/open.mcfunction"; data = read(rel)
    line = tell("@s", button("第一章·空缺者", BEEL_LIGHT, 11, "打开别西卜战役档案"), c("  后方城市异常调查", DARK))
    if line not in data:
        footer = next((x for x in data.splitlines() if "切走再切回面板" in x), "")
        if not footer: raise RuntimeError("panel footer anchor missing")
        save(rel, data.replace(footer, line + "\n" + footer, 1))
    rel = "panel/tick.mcfunction"; lines = [x for x in read(rel).splitlines() if "campaign/beelzebub/orphan_scrub" not in x]
    values = {11: "menu", 12: "start", 13: "rescue", 14: "join", 15: "next_hunt"}
    lines = [x for x in lines if not any(f"rpg_panel matches {n}" in x for n in values)]
    reset = "execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0"; out = []
    for line in lines:
        if line == reset:
            out += [f"execute if score @s rpg_panel matches {n} run function rpg:campaign/beelzebub/{fn}" for n, fn in values.items()]
        out.append(line)
    out[1:1] = [
        "execute if entity @s[tag=rpg.ch1.member] unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run function rpg:campaign/beelzebub/orphan_scrub",
        "execute if entity @s[tag=rpg.ch1.member] if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] unless score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run function rpg:campaign/beelzebub/orphan_scrub",
        "execute if entity @s[tag=rpg.ch1.member] if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] unless score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run function rpg:campaign/beelzebub/orphan_scrub",
    ]
    save(rel, "\n".join(out))


def write_menu_and_membership():
    write("campaign/beelzebub/verdict/reject.mcfunction", "\n".join([
        "scoreboard players set @s rpg_ex_choice 0",
        tell("@s", c("[裁决拒绝] ", DANGER, True), c("你不是当前章节的登记成员，或档案编号与法阵不符。", GRAY)),
        "playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.7 0.6",
    ]))
    write("campaign/beelzebub/orphan_scrub.mcfunction", "\n".join([
        "tag @s remove rpg.ch1.accepted", "tag @s remove rpg.ch1.member",
        "tag @s remove rpg.ch1.party", "tag @s remove rpg.ch1.current",
        "tag @s remove rpg.ch1.host", "tag @s remove rpg.ch1.kit.issued",
        "tag @s remove rpg.ch1.career.confirmed", "scoreboard players set @s rpg_ch1_id 0", "scoreboard players set @s rpg_ch1_session 0",
        tell("@s", c("[章节档案整理] ", CHAPTER, True), c("已移除上一次实例遗留的临时参与状态；永久进度保留。", GRAY)),
    ]))
    write("campaign/beelzebub/menu.mcfunction", "\n".join([
        tell("@s", c("+------ 第一章 · 空缺者 ------+", CHAPTER, True)),
        tell("@s", c("别西卜驱魔战役", BEEL_LIGHT, True), c("　30–60 分钟", DARK)),
        "function rpg:campaign/beelzebub/recap/menu",
        "execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run tellraw @s " + row(button("接受后方城市调查令", CHURCH, 12, "以当前位置建立无地形破坏的章节实例")),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] unless entity @s[tag=rpg.ch1.accepted] run tellraw @s " + row(button("加入当前调查", BEEL_LIGHT, 14, f"需在控制器 {RUNTIME['active_radius']} 格内；罪仆战开始后关闭加入")),
        "execute if entity @s[tag=rpg.ch1.accepted] run tellraw @s " + row(c("状态：已登记为参与者", BEEL_LIGHT, True)),
        "execute if score @s rpg_ch1_done matches 1.. run tellraw @s " + row(c("身份：教廷边缘者", CHURCH, True)),
        "execute if score @s rpg_ch1_next matches 1.. run tellraw @s " + row(button("高阶档案·失窃王冠", NEXT_HUNT, 15, "打开路西法追踪入口")),
        tell("@s", c("异常 → 空缺者 → 罪仆 → 追踪 → 真名 → 器具 → 四阶段 → 裁决 → 救援 → 强化", DARK)),
        tell("@s", button("返回玩家面板", PANEL, 8, "返回总览")),
    ]))
    write("campaign/beelzebub/recap/menu.mcfunction", "\n".join([
        "execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("尚未建立调查实例。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=0..1},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("死者回家、粮册满仓、墓地增员；先记录矛盾，不急于定性。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=2..3},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("空缺者保留记忆却失去情感；罪仆在追杀保存名册的米拉。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=4},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("口粮、尸体与见证人三条路线都在第七粮仓交会。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=5},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("卡西安参与清洗，但超自然痕迹指向借制度进食的暴食领主。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=6},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("假说锁定别西卜与腐败弱点；判词却缺少见证人印。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=7},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("以三种权能确证真名，再完成镇魔、固阵与裁决。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=8..9},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("裁决只击中卡西安空壳；别西卜借教廷删去的见证逃脱。", GRAY)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=10},limit=1] run tellraw @s " + row(c("[案件梗概] ", CHAPTER, True), c("你为保住米拉的姓名释放魔力，被迫登记为边缘者。", GRAY)),
    ]))
    write("campaign/beelzebub/join.mcfunction", "\n".join([
        "execute if entity @s[tag=rpg.ch1.accepted] run return run tellraw @s " + row(c("[第一章] 你已经在参与名单中。", GRAY)),
        f"execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},limit=1] run return run tellraw @s " + row(c("[第一章] 请先抵达调查区域。", DANGER)),
        f"execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},limit=1,scores={{rpg_ch1_stage={RUNTIME['join_lock_stage']}..}}] run return run tellraw @s " + row(c("[第一章] 罪仆已经封锁街区，成员名单已锁定。", DANGER)),
        f"execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},limit=1,scores={{rpg_ch1_roster={RUNTIME['max_party_size']}..}}] run return run tellraw @s " + row(c(f"[第一章] 调查队已满（最多 {RUNTIME['max_party_size']} 人）。", DANGER)),
        "tag @s add rpg.ch1.accepted", "tag @s add rpg.ch1.member",
        "tag @s remove rpg.ch1.kit.issued", "tag @s remove rpg.ch1.career.confirmed",
        f"scoreboard players operation @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},sort=nearest,limit=1] rpg_ch1_id",
        f"scoreboard players operation @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},sort=nearest,limit=1] rpg_ch1_session",
        "tag @s add rpg.ch1.roster.joiner",
        f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},sort=nearest,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.roster.joiner,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_roster 1",
        "tag @s remove rpg.ch1.roster.joiner",
        f"execute unless items entity @s inventory.* {ITEMS['exorcism_totem']['base_item']}[{ITEMS['exorcism_totem']['match']}] run function {ITEMS['exorcism_totem']['give_function']}",
        tell("@s", c("[参与登记] ", CHURCH, True), c("共享进度；首通奖励仍按个人档案幂等结算。", GRAY)),
    ]))
    write("campaign/beelzebub/next_hunt.mcfunction", "\n".join([
        "execute unless score @s rpg_ch1_next matches 1.. run return run tellraw @s " + row(c("[权限不足] 完成第一章后开放。", DANGER)),
        tell("@s", c("[高阶追踪] ", NEXT_HUNT, True), c("第二档案：路西法 · 王冠失窃案", GRAY)),
        tell("@s", c("北部圣库的加冕圣物失踪；现场只留下一根向下坠落的羽毛。", ASH)),
        "function rpg:panel/inquest",
    ]))


def write_start_and_controller():
    controller = ACTORS["controller"]
    controller_tags = ",".join(f'"{tag}"' for tag in [*controller["tags"], "rpg.ch1.new"])
    write("campaign/beelzebub/start.mcfunction", "\n".join([
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s " + row(c("[第一章] 已有调查实例；请从档案选择加入。", DANGER)),
        "scoreboard players add #next rpg_ch1_id 1", "execute if score #next rpg_ch1_id matches ..0 run scoreboard players set #next rpg_ch1_id 1",
        f"execute positioned {controller['spawn']} run summon {controller['entity_type']} ~ ~ ~ {{Tags:[{controller_tags}]}}",
        "execute if score @s rpg_ch1_yaw matches 0 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[0f,0f]}",
        "execute if score @s rpg_ch1_yaw matches 1 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[90f,0f]}",
        "execute if score @s rpg_ch1_yaw matches 2 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[-90f,0f]}",
        "execute if score @s rpg_ch1_yaw matches 3 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[180f,0f]}",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_id = #next rpg_ch1_id",
        "execute store result score @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_session run random value 1..2147483647",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_stage 0",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_time 0",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_obj 0",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_roster 1",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_empty 0",
        "tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] remove rpg.ch1.new",
        "tag @s add rpg.ch1.accepted", "tag @s add rpg.ch1.member", "tag @s add rpg.ch1.party", "tag @s add rpg.ch1.current", "tag @s add rpg.ch1.host", "tag @s remove rpg.ch1.kit.issued", "tag @s remove rpg.ch1.career.confirmed", "scoreboard players operation @s rpg_ch1_id = #next rpg_ch1_id", "scoreboard players operation @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session",
        "execute if score @s rpg_ch1_done matches 1.. run scoreboard players set @s rpg_ch1_replay 1",
        "bossbar add rpg:chapter1 " + row(c("第一章 · 空缺者", CHAPTER, True)),
        "bossbar set rpg:chapter1 max 100", "bossbar set rpg:chapter1 color yellow", "bossbar set rpg:chapter1 style progress",
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/stage/0_enter",
    ]))
    dispatch = [f"execute if score @s rpg_ch1_stage matches {n} run function rpg:campaign/beelzebub/stage/{n}_tick" for n in range(11)]
    write("campaign/beelzebub/tick.mcfunction", "\n".join([
        "tag @a[tag=rpg.ch1.party] remove rpg.ch1.party", "tag @a[tag=rpg.ch1.accepted] remove rpg.ch1.current",
        f"execute as @a[tag=rpg.ch1.member,distance=..{RUNTIME['active_radius']},gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run tag @s add rpg.ch1.party",
        "execute as @a[tag=rpg.ch1.party] run tag @s add rpg.ch1.current",
        f"bossbar set rpg:chapter1 players @a[tag=rpg.ch1.current,distance=..{RUNTIME['active_radius'] + 32}]",
        "execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/roster/failure_tick",
        "execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/roster/failure_tick",
        f"execute unless entity @a[tag=rpg.ch1.current,distance=..{RUNTIME['active_radius'] + 32},gamemode=!spectator] as @e[type={BOSS['entity_type']},tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run scoreboard players add @s rpg_fall 1",
        f"execute as @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,scores={{rpg_fall=12001..}}] run scoreboard players set @s rpg_fall 12000",
        f"execute unless entity @a[tag=rpg.ch1.current,distance=..{RUNTIME['active_radius']},gamemode=!spectator] run return 0",
        "scoreboard players add @s rpg_ch1_time 1", "execute if score @s rpg_ch1_time matches 24001.. run scoreboard players set @s rpg_ch1_time 24000",
    ] + dispatch))
    write("campaign/beelzebub/advance.mcfunction", "\n".join(["scoreboard players add @s rpg_ch1_stage 1", "scoreboard players set @s rpg_ch1_time 0", "scoreboard players set @s rpg_ch1_obj 0", "function rpg:campaign/beelzebub/stage/dispatch_enter"]))
    write("campaign/beelzebub/stage/dispatch_enter.mcfunction", "\n".join(f"execute if score @s rpg_ch1_stage matches {n} run function rpg:campaign/beelzebub/stage/{n}_enter" for n in range(11)))
    write("campaign/beelzebub/roster/failure_tick.mcfunction", "\n".join([
        "scoreboard players set #ch1_online rpg_ch1_empty 0",
        "scoreboard players set #ch1_alive rpg_ch1_empty 0",
        "tag @s add rpg.ch1.failure.controller",
        "execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_session run scoreboard players add #ch1_online rpg_ch1_empty 1",
        "execute as @a[tag=rpg.ch1.member,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_session store result score @s rpg_ch1_hp run data get entity @s Health 100",
        "execute as @a[tag=rpg.ch1.member,gamemode=!spectator,scores={rpg_ch1_hp=1..}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_session run scoreboard players set #ch1_alive rpg_ch1_empty 1",
        "tag @s remove rpg.ch1.failure.controller",
        "execute if score #ch1_online rpg_ch1_empty matches 0 run scoreboard players set @s rpg_ch1_empty 0",
        "execute if score #ch1_alive rpg_ch1_empty matches 1.. run scoreboard players set @s rpg_ch1_empty 0",
        "execute if score #ch1_online rpg_ch1_empty matches 1.. if score #ch1_alive rpg_ch1_empty matches 0 run scoreboard players add @s rpg_ch1_empty 1",
        "execute if score @s rpg_ch1_empty matches 1 run tellraw @a[tag=rpg.ch1.member] " + row(c("[检查点] ", DANGER, True), c("全体成员已死亡或进入旁观；持续 10 秒将重置本阶段。", GRAY)),
        f"execute if score @s rpg_ch1_empty matches {RECOVERY['party_wipe_ticks']}.. run function rpg:campaign/beelzebub/roster/failure_recover",
    ]))
    write("campaign/beelzebub/roster/failure_recover.mcfunction", "\n".join([
        "scoreboard players set @s rpg_ch1_empty 0",
        "execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/recover_minions",
        "execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/recover_boss",
    ]))


def write_preflight():
    """Turn the freshly written start into a configurable zero-residue sample gate."""
    creation = read("campaign/beelzebub/start.mcfunction")
    safe = RUNTIME["safe_plane"]
    scene_radius = RUNTIME["scene_radius"]
    write("campaign/beelzebub/start_pass.mcfunction", creation)
    write("campaign/beelzebub/start.mcfunction", "\n".join([
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s " + row(c("[第一章] 已有调查实例；请从档案选择加入。", DANGER)),
        "execute if entity @s[gamemode=spectator] run return run tellraw @s " + row(c("[场地校验] 旁观者不能发起章节。", DANGER)),
        f"execute unless dimension {RUNTIME['dimension']} run return run tellraw @s " + row(c("[场地校验] 第一章只能在配置维度展开。", DANGER)),
        f"execute if entity @e[type=minecraft:villager,distance=..{scene_radius},limit=1] run return run tellraw @s " + row(c(f"[场地校验] {scene_radius} 格内已有村民；请远离聚落。", DANGER)),
        f"execute if entity @e[type=minecraft:iron_golem,distance=..{scene_radius},limit=1] run return run tellraw @s " + row(c(f"[场地校验] {scene_radius} 格内已有聚落守卫。", DANGER)),
        f"execute if entity @e[tag=rpg.advent,distance=..{scene_radius},limit=1] run return run tellraw @s " + row(c("[场地校验] 附近已有恶魔战斗。", DANGER)),
        f"execute if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..{scene_radius},limit=1] run return run tellraw @s " + row(c("[场地校验] 附近已有活动仪式。", DANGER)),
        "execute if entity @s[y_rotation=-45..45] run scoreboard players set @s rpg_ch1_yaw 0",
        "execute if entity @s[y_rotation=-45..45] rotated 0 0 run return run function rpg:campaign/beelzebub/scene/preflight",
        "execute if entity @s[y_rotation=45.01..135] run scoreboard players set @s rpg_ch1_yaw 1",
        "execute if entity @s[y_rotation=45.01..135] rotated 90 0 run return run function rpg:campaign/beelzebub/scene/preflight",
        "execute if entity @s[y_rotation=-135..-45.01] run scoreboard players set @s rpg_ch1_yaw 2",
        "execute if entity @s[y_rotation=-135..-45.01] rotated -90 0 run return run function rpg:campaign/beelzebub/scene/preflight",
        "scoreboard players set @s rpg_ch1_yaw 3",
        "execute rotated 180 0 run function rpg:campaign/beelzebub/scene/preflight",
    ]))
    bad = tuple(safe["forbidden_ground"])
    headroom_checks = " ".join(f"if block ~ ~{height} ~ minecraft:air" for height in range(safe["headroom"]))
    base = ["scoreboard players set @s rpg_ch1_safe 0"]
    for x in safe["ground_sample_x"]:
        for z in safe["ground_sample_z"]:
            cond = f"execute positioned ^{x} ^ ^{z} if loaded ~ ~ ~ " + " ".join(f"unless block ~ ~-1 ~ {b}" for b in bad)
            base.append(cond + f" {headroom_checks} run scoreboard players add @s rpg_ch1_safe 1")
    for x in safe["tall_sample_x"]:
        for z in safe["tall_sample_z"]:
            cond = f"execute positioned ^{x} ^ ^{z} if loaded ~ ~ ~ " + " ".join(f"unless block ~ ~-1 ~ {b}" for b in bad)
            base.append(cond + f" {headroom_checks} run scoreboard players add @s rpg_ch1_safe 1")
    sample_x = [*safe["ground_sample_x"], *safe["tall_sample_x"]]
    sample_z = [*safe["ground_sample_z"], *safe["tall_sample_z"]]
    base += [
        f"execute if score @s rpg_ch1_safe matches {len(safe['ground_sample_x']) * len(safe['ground_sample_z']) + len(safe['tall_sample_x']) * len(safe['tall_sample_z'])} run return run function rpg:campaign/beelzebub/start_pass",
        tell("@s", c("[场地校验失败] ", DANGER, True), c(f"采样覆盖 X {min(sample_x)}..{max(sample_x)}、Z {min(sample_z)}..{max(sample_z)}，每点需净空 {safe['headroom']} 格；未生成任何章节实体。", GRAY)),
    ]
    write("campaign/beelzebub/scene/preflight.mcfunction", "\n".join(base))


def write_point_probe(key, message, extra=None):
    timing = RUNTIME["observation_ticks"]
    threshold = timing["hypothesis"] if key.startswith("hyp") else timing["anomaly"] if key.startswith("anom") else timing["trail"] if key.startswith("trail") else timing["cache"]
    write(f"campaign/beelzebub/probe/{key}.mcfunction", "\n".join([
        "scoreboard players set #ch1_point_ok rpg_ch1_seen 0",
        "tag @s add rpg.ch1.point.active",
        f"execute as @a[tag=rpg.ch1.current,distance=..{RUNTIME['investigate_radius']},sort=nearest,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players set #ch1_point_ok rpg_ch1_seen 1",
        "execute if score #ch1_point_ok rpg_ch1_seen matches 1 run scoreboard players add @s rpg_ch1_seen 1",
        "execute if score #ch1_point_ok rpg_ch1_seen matches 0 run scoreboard players set @s rpg_ch1_seen 0",
        f"execute if score @s rpg_ch1_seen matches {threshold // 2} run playsound minecraft:block.amethyst_block.chime player @a[tag=rpg.ch1.current,distance=..8] ~ ~ ~ 0.35 1.4",
        f"execute if score @s rpg_ch1_seen matches {threshold}.. as @a[tag=rpg.ch1.current,distance=..{RUNTIME['investigate_radius']},sort=nearest,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run return run function rpg:campaign/beelzebub/point/{key}",
        "tag @s remove rpg.ch1.point.active",
    ]))
    commands = [
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1",
        "playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35",
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("[调查] ", CHAPTER, True), c(message, GRAY)),
    ] + (extra or []) + [f"kill @e[type=minecraft:text_display,tag=rpg.ch1.{key}.label,distance=..2]", "kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]"]
    write(f"campaign/beelzebub/point/{key}.mcfunction", "\n".join(commands))


def write_stage0_2():
    write("campaign/beelzebub/stage/0_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 2", "bossbar set rpg:chapter1 name " + row(c("楔子｜第十三声钟", CHAPTER, True)),
        "playsound minecraft:block.bell.use master @a[tag=rpg.ch1.current] ~ ~ ~ 0.7 0.55",
        tell("@a[tag=rpg.ch1.current]", c("[征调令 · 维斯珀后方城]", CHURCH, True), c("　任务：核对粮册与死亡登记。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("战争已经打了一百年。前线吃人，后方负责忘记。", ASH)),
    ]))
    write("campaign/beelzebub/stage/0_tick.mcfunction", "\n".join([
        "execute if score @s rpg_ch1_time matches 45 run playsound minecraft:block.bell.resonate master @a[tag=rpg.ch1.current] ~ ~ ~ 0.8 0.62",
        "execute if score @s rpg_ch1_time matches 45 run tellraw @a[tag=rpg.ch1.current] " + row(c("旁白：", ASH, True), c("粮册写着满仓，街边却摆着无人领取的空碗。", GRAY)),
        "execute if score @s rpg_ch1_time matches 105 run tellraw @a[tag=rpg.ch1.current] " + row(c("旁白：", ASH, True), c("墓地每天添新土；入夜后，死者仍会回家。", GRAY)),
        "execute if score @s rpg_ch1_time matches 165 run playsound minecraft:entity.bee.loop_aggressive master @a[tag=rpg.ch1.current] ~ ~ ~ 0.18 0.45",
        "execute if score @s rpg_ch1_time matches 165 run tellraw @a[tag=rpg.ch1.current] " + row(c("书记员 伊莱亚：", CHURCH, True), c("你听见十三下了吗？司钟人三天前就死了。", GRAY)),
        "execute if score @s rpg_ch1_time matches 225 run tellraw @a[tag=rpg.ch1.current] " + row(c("伊莱亚：", CHURCH, True), c("教廷说绳索自己落下，也说你没有听见。", GRAY)),
        "execute if score @s rpg_ch1_time matches 285 run tellraw @a[tag=rpg.ch1.current] " + row(c("伊莱亚：", CHURCH, True), c("驱魔官处理得太快、太干净。我需要一个还相信自己眼睛的人。", GRAY)),
        "execute if score @s rpg_ch1_time matches 345 run tellraw @a[tag=rpg.ch1.current] " + row(c("[调查原则] ", CHAPTER, True), c("先记录事实，再比较解释。一个异常不能证明恶魔。", GRAY)),
        "execute if score @s rpg_ch1_time matches 400.. run function rpg:campaign/beelzebub/advance",
    ]))
    lines = ["bossbar set rpg:chapter1 value 8", "bossbar set rpg:chapter1 name " + row(c("发现异常｜取得 3 份相互矛盾的记录", CHAPTER, True))]
    for key in ("anom1", "anom2", "anom3"):
        point = scene("anomaly", key)
        lines += owned_spawn(point["spawn"], key, point["label"], palette_color(CONFIG, point["color"]))
    write("campaign/beelzebub/stage/1_enter.mcfunction", "\n".join(lines))
    write("campaign/beelzebub/stage/1_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.{k}] at @s run function rpg:campaign/beelzebub/probe/{k}" for k in ("anom1", "anom2", "anom3")] + [
        "execute if score @s rpg_ch1_obj matches 3.. unless entity @s[tag=rpg.ch1.recap.anomaly] run function rpg:campaign/beelzebub/recap/anomaly",
        f"execute if score @s rpg_ch1_obj matches 3.. if entity @s[tag=rpg.ch1.recap.anomaly] if score @s rpg_ch1_time matches {RUNTIME['recap_hold_ticks']}.. run function rpg:campaign/beelzebub/advance",
    ]))
    write_point_probe("anom1", "观察：面包仍温热，切面却是灰；她准确说出孩子生日。", [
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("伊莱亚：", CHURCH, True), c("若是亡灵，她为何保留全部记忆？若仍活着，她为何不回应哭声？", GRAY)),
    ])
    write_point_probe("anom2", "观察：死亡日期是明天，死因统一写作‘疫病净化’。", [
        f"function {ITEMS['exorcism_totem']['give_function']}",
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("伊莱亚：", CHURCH, True), c("墨水和封印都是真的。这更像命令，不像预言。", GRAY)),
    ])
    write_point_probe("anom3", "观察：钟灰混有透明虫翅，落向慈济所后门。", [
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("陌生女声：", WITNESS, True), c("别顺着翅膀找巢。先问它们替谁带路。", GRAY)),
    ])
    write("campaign/beelzebub/recap/anomaly.mcfunction", "\n".join([
        "tag @s add rpg.ch1.recap.anomaly", "scoreboard players set @s rpg_ch1_time 0",
        tell("@a[tag=rpg.ch1.current]", c("+------ 案情复盘 · 异常 ------+", CHAPTER, True)),
        tell("@a[tag=rpg.ch1.current]", c("◆ 已知　", SEAL, True), c("死者保留记忆外壳，处决日期却写在明天。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("◇ 矛盾　", WITNESS, True), c("疫病解释不了预写命令，亡灵解释不了完整记忆。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("→ 下一步　", BEEL_LIGHT, True), c("找到钟灰指向的活见证人。", GRAY)),
    ]))
    vacant = ACTORS["npcs"]["vacant_mother"]
    vacant_tags = ",".join(f'"{tag}"' for tag in [*vacant["tags"], "rpg.ch1.new"])
    write("campaign/beelzebub/stage/2_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 13", "bossbar set rpg:chapter1 name " + row(c("会回家的死者｜以圣器照见空缺", CHAPTER, True)),
        f"execute positioned {vacant['spawn']} run summon {vacant['entity_type']} ~ ~ ~ {{Tags:[{vacant_tags}],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,CustomName:" + row(c(vacant["display_name"], GRAY)) + "}",
        f"scoreboard players operation @e[type={vacant['entity_type']},tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id", f"tag @e[type={vacant['entity_type']},tag=rpg.ch1.new] remove rpg.ch1.new",
        f"scoreboard players set @e[type={vacant['entity_type']},tag=rpg.ch1.vacant,sort=nearest,limit=1,distance=..40] rpg_vac_x -100",
        tell("@a[tag=rpg.ch1.current]", c("目标更新　", CHAPTER, True), c("手持驱魔图腾，靠近‘回家的母亲’。", GRAY)),
    ]))
    write("campaign/beelzebub/stage/2_tick.mcfunction", "\n".join([
        f"tag @e[type={vacant['entity_type']},tag=rpg.ch1.vacant] remove rpg.ch1.vacant.current",
        f"execute as @e[type={vacant['entity_type']},tag=rpg.ch1.vacant] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.vacant.current",
        f"execute as @e[type={vacant['entity_type']},tag=rpg.ch1.vacant.current,limit=1] at @s if entity @a[tag=rpg.ch1.current,tag=rpg.holy,distance=..8,limit=1] run function rpg:vacant/reveal",
        f"execute as @e[type={vacant['entity_type']},tag=rpg.ch1.vacant.current,scores={{rpg_vac_x=-80..}},limit=1] at @s run function rpg:campaign/beelzebub/vacant_reveal",
        "execute if score @s rpg_ch1_obj matches 1.. run function rpg:campaign/beelzebub/advance",
    ]))
    write("campaign/beelzebub/vacant_reveal.mcfunction", "\n".join([
        "tag @s remove rpg.vacant", "tag @s add rpg.vac.torn", "effect give @s minecraft:glowing 10 0 true", "particle minecraft:sculk_soul ~ ~1.3 ~ 0.35 0.6 0.35 0.03 25 force",
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("空缺者母亲：", ASH, True), c("今天是祷告日。每个人都有一份。", GRAY)),
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("伊莱亚：", CHURCH, True), c("她知道自己是谁，却不知道‘自己’是什么意思。", GRAY)),
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("米拉：", WITNESS, True), c("她昨天把整份口粮送进第七粮仓，却一口也没有吃。", GRAY)),
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("[交叉验证] ", CHAPTER, True), c("不是失忆，也不是普通复生：姓名仍在，人的主体已经空缺。", GRAY)),
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_obj 1",
    ]))


def write_minions():
    roles = [(spec["spawn"], key, spec["role"])
             for key, spec in sorted(MINIONS.items(), key=lambda pair: pair[1]["role"])]
    waves = {}
    for _, key, _ in roles:
        waves.setdefault(MINIONS[key]["wave"], []).append(key)
    wave_ids = sorted(waves)
    first_wave, final_wave = wave_ids[0], wave_ids[-1]

    def wave_label(wave):
        duties = "与".join(MINIONS[key]["duty"] for key in waves[wave])
        return f"五席未满｜第{wave}轮 · {duties}"

    mira = ACTORS["npcs"]["mira_guard"]
    mira_tags = ",".join(f'"{tag}"' for tag in [*mira["tags"], "rpg.ch1.new"])
    lines = ["bossbar set rpg:chapter1 value 20", "bossbar set rpg:chapter1 name " + row(c(wave_label(first_wave), BEEL, True)), "scoreboard players set @s rpg_ch1_obj 0", f"scoreboard players set @s rpg_ch1_sub {first_wave}", "scoreboard players set @s rpg_ch1_guard 0",
             f"execute unless entity @e[type={mira['entity_type']},tag=rpg.ch1.mira,distance=..40,limit=1] positioned {mira['spawn']} run summon {mira['entity_type']} ~ ~ ~ {{Tags:[{mira_tags}],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:" + row(c(mira["display_name"], WITNESS)) + "}",
             f"scoreboard players operation @e[type={mira['entity_type']},tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id", f"tag @e[type={mira['entity_type']},tag=rpg.ch1.new] remove rpg.ch1.new",
             f"execute positioned {mira['spawn']} run tp @e[type={mira['entity_type']},tag=rpg.ch1.mira,distance=..{RUNTIME['scene_radius']},sort=nearest,limit=1] ~ ~ ~",
             tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("我偷下三页名册。它们追的不是我，是还能把死者叫回名字的人。", GRAY))]
    if waves[first_wave]:
        lines.append(tell("@a[tag=rpg.ch1.current]", c(MINIONS[waves[first_wave][0]]["display_name"] + "：", BEEL, True), c("宴席不接待没有登记的客人。", GRAY)))
    if len(waves[first_wave]) > 1:
        lines.append(tell("@a[tag=rpg.ch1.current]", c(MINIONS[waves[first_wave][1]]["display_name"] + "：", BEEL, True), c("名册在他们身上。先封街，再取回。", GRAY)))
    for name in waves[first_wave]:
        lines.append(f"execute positioned {MINIONS[name]['spawn']} run function rpg:campaign/beelzebub/spawn/minion/{name}")
    write("campaign/beelzebub/stage/3_enter.mcfunction", "\n".join(lines))
    for _, name, role in roles:
        spec = MINIONS[name]
        typ = spec["entity_type"]
        write(f"campaign/beelzebub/spawn/minion/{name}.mcfunction", "\n".join([
            f"tag @e[type={typ},tag=rpg.demon.minion.lord{BOSS['lord_score']},scores={{rpg_mn_role={role}}},distance=..4] add rpg.ch1.preexisting",
            f"function {spec['summon_function']}",
            f"tag @e[type={typ},tag=rpg.demon.minion.lord{BOSS['lord_score']},tag=!rpg.ch1.preexisting,scores={{rpg_mn_role={role}}},distance=..4,sort=nearest,limit=1] add rpg.ch1.minion.new",
            "scoreboard players operation @e[tag=rpg.ch1.minion.new,limit=1] rpg_ch1_id = @s rpg_ch1_id",
            "data modify entity @e[tag=rpg.ch1.minion.new,limit=1] CustomName set value " + row(c(spec["display_name"], BEEL_LIGHT, True)),
            "tag @e[tag=rpg.ch1.minion.new,limit=1] add rpg.ch1.minion", "execute if entity @e[tag=rpg.ch1.minion.new,limit=1] run scoreboard players add @s rpg_ch1_obj 1",
            "execute as @e[tag=rpg.ch1.minion.new,limit=1] run function rpg:campaign/beelzebub/minion/scale",
            "tag @e[tag=rpg.ch1.minion.new] remove rpg.ch1.minion.new", "tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting",
        ]))
    scaled = {spec["role"]: {int(roster): hp for roster, hp in spec["health_by_party"].items()}
              for spec in MINIONS.values()}
    scale_lines = ["# Fixed roster score was locked before Stage 3; disconnects never rescale enemies."]
    for role, by_roster in scaled.items():
        for roster, hp in by_roster.items():
            scale_lines += [
                f"execute if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_mn_role matches {role} if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_roster matches {roster} run attribute @s minecraft:max_health base set {hp}",
                f"execute if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_mn_role matches {role} if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_roster matches {roster} run data merge entity @s {{Health:{hp}f}}",
            ]
    write("campaign/beelzebub/minion/scale.mcfunction", "\n".join(scale_lines))
    stage3_tick = [
        "tag @e[tag=rpg.ch1.minion] remove rpg.ch1.minion.current",
        "execute as @e[tag=rpg.ch1.minion] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.minion.current",
        f"tag @e[type={mira['entity_type']},tag=rpg.ch1.mira] remove rpg.ch1.mira.current",
        f"execute as @e[type={mira['entity_type']},tag=rpg.ch1.mira] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.mira.current",
        f"execute unless entity @s[tag=rpg.ch1.mira.captured] if entity @e[tag=rpg.ch1.minion.current,distance=..40,limit=1] at @e[type={mira['entity_type']},tag=rpg.ch1.mira.current,limit=1] if entity @e[tag=rpg.ch1.minion.current,distance=..8,limit=1] unless entity @a[tag=rpg.ch1.current,distance=..10,limit=1] run scoreboard players add @s rpg_ch1_guard 1",
        f"execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_guard matches {RECOVERY['mira_capture_ticks']}.. run function rpg:campaign/beelzebub/mira/capture",
        "execute if entity @s[tag=rpg.ch1.mira.captured] run scoreboard players remove @s rpg_ch1_guard 1",
        f"execute if entity @s[tag=rpg.ch1.mira.captured] at @e[type={mira['entity_type']},tag=rpg.ch1.mira.current,limit=1] if entity @a[tag=rpg.ch1.current,distance=..3,limit=1] run scoreboard players add @s rpg_ch1_rescue 1",
        f"execute if entity @s[tag=rpg.ch1.mira.captured] at @e[type={mira['entity_type']},tag=rpg.ch1.mira.current,limit=1] unless entity @a[tag=rpg.ch1.current,distance=..3,limit=1] run scoreboard players set @s rpg_ch1_rescue 0",
        f"execute if entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_rescue matches {RECOVERY['mira_rescue_ticks']}.. run function rpg:campaign/beelzebub/mira/rescue_capture",
        "execute if entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_guard matches ..0 run function rpg:campaign/beelzebub/recover_minions",
    ]
    cumulative = 0
    for index, wave in enumerate(wave_ids):
        cumulative += len(waves[wave])
        stage3_tick.append(f"execute if score @s rpg_ch1_sub matches {wave} if score @s rpg_ch1_obj matches ..{cumulative - 1} if score @s rpg_ch1_time matches {RECOVERY['boss_missing_ticks']}.. run function rpg:campaign/beelzebub/recover_minions")
        if index + 1 < len(wave_ids):
            next_wave = wave_ids[index + 1]
            stage3_tick.append(f"execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches {wave} if score @s rpg_ch1_obj matches {cumulative}.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] run function rpg:campaign/beelzebub/minion/wave{next_wave}")
    total_minions = len(MINIONS)
    stage3_tick += [
        f"execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches {final_wave} if score @s rpg_ch1_obj matches {total_minions}.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] unless entity @s[tag=rpg.ch1.recap.minions] run function rpg:campaign/beelzebub/recap/minions",
        f"execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches {final_wave} if score @s rpg_ch1_obj matches {total_minions}.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] if entity @s[tag=rpg.ch1.recap.minions] if score @s rpg_ch1_time matches {RUNTIME['recap_hold_ticks']}.. run function rpg:campaign/beelzebub/advance",
    ]
    write("campaign/beelzebub/stage/3_tick.mcfunction", "\n".join(stage3_tick))
    for wave in wave_ids[1:]:
        wave_lines = [
            f"scoreboard players set @s rpg_ch1_sub {wave}", "scoreboard players set @s rpg_ch1_time 0",
            "bossbar set rpg:chapter1 name " + row(c(wave_label(wave), BEEL, True)),
        ]
        for name in waves[wave]:
            wave_lines.append(f"execute positioned {MINIONS[name]['spawn']} run function rpg:campaign/beelzebub/spawn/minion/{name}")
        if wave == final_wave:
            speaker = MINIONS[waves[wave][0]]["display_name"] + "："
            wave_lines += [
                tell("@a[tag=rpg.ch1.current]", c(speaker, BEEL, True), c("见证不是事实。活下来的见证才是。", GRAY)),
                tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("处决令早于所谓疫病。它们不是来止灾，是来让灾情没人能说出口。", GRAY)),
            ]
        else:
            wave_lines += [
                tell("@a[tag=rpg.ch1.current]", c("虚假的家人：", ASH, True), c("回来吃饭吧。战争已经结束了。", GRAY)),
                tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("夺回的转运单盖着卡西安的印。先记作‘参与’，不要急着写成‘源头’。", GRAY)),
            ]
        write(f"campaign/beelzebub/minion/wave{wave}.mcfunction", "\n".join(wave_lines))
    write("campaign/beelzebub/recap/minions.mcfunction", "\n".join([
        "tag @s add rpg.ch1.recap.minions", "scoreboard players set @s rpg_ch1_time 0",
        tell("@a[tag=rpg.ch1.current]", c("+------ 案情复盘 · 五席 ------+", CHAPTER, True)),
        tell("@a[tag=rpg.ch1.current]", c("◆ 已知　", SEAL, True), c("五种职责同属一场追猎，文件都有卡西安签章。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("◇ 矛盾　", WITNESS, True), c("处决令早于疫病公告；签章证明参与，不证明源头。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("→ 下一步　", BEEL_LIGHT, True), c("沿夺回的物证确认行动中心。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("卡西安在摆桌；桌子的主人还没有现身。", GRAY)),
    ]))
    write("campaign/beelzebub/recover_minions.mcfunction", "\n".join([
        "tag @e[tag=rpg.ch1.minion] remove rpg.ch1.minion.current",
        "execute as @e[tag=rpg.ch1.minion] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.minion.current",
        "kill @e[tag=rpg.ch1.minion.current]", "tag @s remove rpg.ch1.mira.captured", "scoreboard players set @s rpg_ch1_empty 0", "scoreboard players add @s rpg_ch1_fail 1",
        tell("@a[tag=rpg.ch1.current]", c("[章节恢复] ", CHAPTER, True), c("罪仆归属未完整建立，重新展开这一波。", GRAY)),
        "scoreboard players set @s rpg_ch1_time 0", "function rpg:campaign/beelzebub/stage/3_enter",
    ]))
    write("campaign/beelzebub/mira/capture.mcfunction", "\n".join([
        "tag @s add rpg.ch1.mira.captured", f"scoreboard players set @s rpg_ch1_guard {RECOVERY['mira_rescue_window_ticks']}", "scoreboard players set @s rpg_ch1_rescue 0",
        f"execute positioned {ACTORS['npcs']['mira_captured']['spawn']} run tp @e[type={mira['entity_type']},tag=rpg.ch1.mira.current,limit=1] ~ ~ ~",
        tell("@a[tag=rpg.ch1.current]", c("[见证人被捕] ", DANGER, True), c("在 03:00 内靠近米拉 3 格将她带回，否则整组罪仆重置。", GRAY)),
    ]))
    write("campaign/beelzebub/mira/rescue_capture.mcfunction", "\n".join([
        "tag @s remove rpg.ch1.mira.captured", "scoreboard players set @s rpg_ch1_guard 0", "scoreboard players set @s rpg_ch1_rescue 0",
        f"execute at @s positioned {mira['spawn']} run tp @e[type={mira['entity_type']},tag=rpg.ch1.mira.current,limit=1] ~ ~ ~",
        tell("@a[tag=rpg.ch1.current]", c("[见证人救回] ", WITNESS, True), c("米拉重新回到队伍；街区战继续。", GRAY)),
    ]))


def write_tracking_inquest_prep():
    lines = ["bossbar set rpg:chapter1 value 31", "bossbar set rpg:chapter1 name " + row(c("确认活动区域｜让三条运输记录彼此指认", BEEL, True)),
             tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("别只跟苍蝇走。把口粮、尸体和见证人的去向叠在一起。", GRAY))]
    first_trail = scene("trail", "trail1")
    lines += owned_spawn(first_trail["spawn"], "trail1", first_trail["label"], palette_color(CONFIG, first_trail["color"]))
    write("campaign/beelzebub/stage/4_enter.mcfunction", "\n".join(lines))
    write("campaign/beelzebub/stage/4_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.trail{n}] at @s run function rpg:campaign/beelzebub/probe/trail{n}" for n in range(1, 5)] + [
        "execute if score @s rpg_ch1_obj matches 4.. unless entity @s[tag=rpg.ch1.recap.area] run function rpg:campaign/beelzebub/recap/area",
        f"execute if score @s rpg_ch1_obj matches 4.. if entity @s[tag=rpg.ch1.recap.area] if score @s rpg_ch1_time matches {RUNTIME['recap_hold_ticks']}.. run function rpg:campaign/beelzebub/advance",
    ]))
    trails = (
        "口粮袋封签完整，袋底只有虫翅；粮食在登记后被取走。",
        "带血车辙由慈济所出发，与军粮车使用同一规格车轮。",
        "配给牌上的姓名与明日处决名单重合，日期却早了两周。",
        "三条路线都停在‘满仓’封条前；门内没有粮食，只有写着姓名的餐盘。",
    )
    for n, text in enumerate(trails, 1):
        extra = [] if n == 4 else [f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/spawn/trail{n + 1}"]
        if n == 1:
            extra.insert(0, tell("@a[tag=rpg.ch1.current,distance=..24]", c("米拉：", WITNESS, True), c("像盗粮，但偷粮的人不会把虫翅封进每一只空袋。", GRAY)))
        elif n == 2:
            extra.insert(0, tell("@a[tag=rpg.ch1.current,distance=..24]", c("伊莱亚：", CHURCH, True), c("运的不是粮，是被登记为尸体的人。", GRAY)))
        elif n == 3:
            extra.insert(0, tell("@a[tag=rpg.ch1.current,distance=..24]", c("伊莱亚：", CHURCH, True), c("这些记录早于卡西安接任。他是执行者，不是全部解释。", GRAY)))
        else:
            extra.append(tell("@a[tag=rpg.ch1.current,distance=..24]", c("米拉：", WITNESS, True), c("仓库从来不是空的。空的是被端上桌的人。", GRAY)))
        write_point_probe(f"trail{n}", text, extra)
        if n > 1:
            point = scene("trail", f"trail{n}")
            write(f"campaign/beelzebub/spawn/trail{n}.mcfunction", "\n".join(owned_spawn(point["spawn"], f"trail{n}", point["label"], palette_color(CONFIG, point["color"]))))
    write("campaign/beelzebub/recap/area.mcfunction", "\n".join([
        "tag @s add rpg.ch1.recap.area", "scoreboard players set @s rpg_ch1_time 0",
        tell("@a[tag=rpg.ch1.current]", c("+------ 案情复盘 · 三线 ------+", CHAPTER, True)),
        tell("@a[tag=rpg.ch1.current]", c("◆ 已知　", SEAL, True), c("口粮、尸体与灭口路线都汇入第七粮仓。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("◇ 矛盾　", WITNESS, True), c("满仓封条后没有粮食，旧记录早于卡西安接任。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("→ 下一步　", BEEL_LIGHT, True), c("进入粮仓，以检材建立真名假说。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("卡西安：", CHURCH, True), c("移交污染档案。我会记录你们曾协助教廷。", ASH)),
        tell("@a[tag=rpg.ch1.current]", c("卡西安：", CHURCH, True), c("拒绝移交，即视为记录错误。", ASH)),
    ]))

    # Environment establishes a hypothesis only. Canonical boss-skill hooks award
    # rpg:inquest/clue/4_1..4_5; three different witnessed powers reveal rpg.name.4.
    lines = ["bossbar set rpg:chapter1 value 41", "bossbar set rpg:chapter1 name " + row(c("调查真名与弱点｜排除 2 个错误答案", BEEL, True)),
             tell("@a[tag=rpg.ch1.current]", c("[待验证假说] ", CHAPTER, True), c("A 疫病复生　B 人为盗粮　C 暴食寄生。每项证物都必须能反驳至少一个解释。", GRAY))]
    for key in ("hyp1", "hyp2", "hyp3"):
        point = scene("hypothesis", key)
        lines += owned_spawn(point["spawn"], key, point["label"], palette_color(CONFIG, point["color"]))
    write("campaign/beelzebub/stage/5_enter.mcfunction", "\n".join(lines))
    write("campaign/beelzebub/stage/5_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp{n}] at @s run function rpg:campaign/beelzebub/probe/hyp{n}" for n in range(1, 4)] + [
        "execute if score @s rpg_ch1_obj matches 3.. unless entity @s[tag=rpg.ch1.recap.hypothesis] run function rpg:campaign/beelzebub/recap/hypothesis",
        f"execute if score @s rpg_ch1_obj matches 3.. if entity @s[tag=rpg.ch1.recap.hypothesis] if score @s rpg_ch1_time matches {RUNTIME['recap_hold_ticks']}.. run function rpg:campaign/beelzebub/advance",
    ]))
    hypotheses = (
        ("炉灰中没有灼烧骨骼，只有带牙印的餐盘灰；排除普通焚尸。", "伊莱亚：火灾说不能成立。灰是‘吃剩后’出现，不是燃烧后。"),
        ("蝇茧每次收缩，都有一名空缺者停止呼吸；排除自然疫病。", "米拉：病会传播，这东西却在统一收取。像一只连着全城的胃。"),
        ("完好食物全部消失，毒马铃薯却被推出餐盘并留下逆向灼痕。", "伊莱亚：人为盗粮解释不了拒食规律；腐败物能让仪式短暂失去胃口。"),
    )
    for n, (text, reply) in enumerate(hypotheses, 1):
        speaker, words = reply.split("：", 1)
        color = WITNESS if speaker == "米拉" else CHURCH
        write_point_probe(f"hyp{n}", text, [
            tell("@a[tag=rpg.ch1.current,distance=..24]", c(speaker + "：", color, True), c(words, GRAY)),
            f"tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.done.hyp.{n}",
        ])
        # Compatibility aliases for presentation patches; they do not bypass the
        # canonical three-skill witness requirement.
        write(f"campaign/beelzebub/point/clue{n}.mcfunction", f"function rpg:campaign/beelzebub/point/hyp{n}")
    write("campaign/beelzebub/recap/hypothesis.mcfunction", "\n".join([
        "tag @s add rpg.ch1.recap.hypothesis", "scoreboard players set @s rpg_ch1_time 0",
        tell("@a[tag=rpg.ch1.current]", c("+------ 案情复盘 · 假说 ------+", CHAPTER, True)),
        tell("@a[tag=rpg.ch1.current]", c("◆ 已知　", SEAL, True), c("余烬、胃囊与拒食腐物共同指向暴食寄生。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("◇ 矛盾　", WITNESS, True), c("环境证据能排除疫病与盗粮，却不能独自确认真名。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("→ 下一步　", BEEL_LIGHT, True), c("备齐器具，在战斗中亲历三种不同权能。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("[假说修正] ", CHAPTER, True), c("疫病与普通亡灵已排除；保留‘别西卜 · 暴食寄生’。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("[弱点假说] ", CHURCH, True), c("已经自行腐败、失去宴席价值之物。", GRAY)),
    ]))

    lines = ["bossbar set rpg:chapter1 value 49", "bossbar set rpg:chapter1 name " + row(c("被撕去的判词｜准备 3 组仪式器具", CHURCH, True))]
    for key in ("cache1", "cache2", "cache3"):
        point = scene("cache", key)
        lines += owned_spawn(point["spawn"], key, point["label"], palette_color(CONFIG, point["color"]))
    write("campaign/beelzebub/stage/6_enter.mcfunction", "\n".join(lines + [
        tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("器具封条都是真的，可判词从七直接跳到九。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("先拿齐东西。等我们知道缺的是什么，再决定要不要相信它。", GRAY)),
    ]))
    write("campaign/beelzebub/stage/6_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.cache{n}] at @s run function rpg:campaign/beelzebub/probe/cache{n}" for n in range(1, 4)] + [
        "execute if score @s rpg_ch1_obj matches 3.. unless entity @s[tag=rpg.ch1.recap.prep] run function rpg:campaign/beelzebub/recap/prep",
        f"execute if score @s rpg_ch1_obj matches 3.. if entity @s[tag=rpg.ch1.recap.prep] if score @s rpg_ch1_time matches {RUNTIME['recap_hold_ticks']}.. run function rpg:campaign/beelzebub/advance",
    ]))
    pending_name = row(c("[待确证残页] ", CHURCH, True), c("万蝇之王 · 缺页判词", BEEL_LIGHT))
    pending_lore = json.dumps([[c("+------------------+", "white")], [c("环境证物只建立了真名假说", GRAY)],
                               [c("必须亲历三种不同权能才能确证", CHURCH)],
                               [c("此页不能投入正式驱魔法阵", DANGER)], [c("+------------------+", "white")]],
                              ensure_ascii=False, separators=(",", ":"))
    pending_item = ITEMS["pending_name_page"]
    write(function_rel(pending_item["give_function"]),
          f"give @s {pending_item['base_item']}[custom_name={pending_name},lore={pending_lore},enchantment_glint_override=true,max_stack_size=1,item_model=\"{pending_item['item_model']}\",custom_data={custom_data_value(pending_item)}]")
    cache = {int(key.removeprefix("cache")): [ITEMS[item_key]["give_function"] for item_key in loadout]
             for key, loadout in CONFIG["cache_loadouts"].items()}
    cache_text = {
        1: "档案箱：真名残页标注‘待确证’，第八页被刀具整齐割走。",
        2: "圣器箱：图腾、水与银钉齐全；配置足以开阵，却不足以补写见证。",
        3: "裁决箱：四种路线器具都在，说明教廷预期你完成一次看似合法的裁决。",
    }
    cache_reply = {
        1: ("伊莱亚：", CHURCH, "正式判词必须有施术者、对象、媒介、见证。缺的是见证人栏。"),
        2: ("米拉：", WITNESS, "腐败媒介阻止吞食，银钉固定边缘；它们能拖住祂，不能替死者作证。"),
        3: ("伊莱亚：", CHURCH, "四种裁决都能启动。也正因为都能启动，缺页才更像故意留下的缺口。"),
    }
    for n, calls in cache.items():
        speaker, color, words = cache_reply[n]
        write_point_probe(f"cache{n}", cache_text[n], [f"execute as @a[tag=rpg.ch1.current] run function {fn}" for fn in calls] + [
            tell("@a[tag=rpg.ch1.current,distance=..24]", c(speaker, color, True), c(words, GRAY)),
        ])
    write("campaign/beelzebub/recap/prep.mcfunction", "\n".join([
        "tag @s add rpg.ch1.recap.prep", "scoreboard players set @s rpg_ch1_time 0",
        tell("@a[tag=rpg.ch1.current]", c("[入场前复盘]", CHAPTER, True)),
        tell("@a[tag=rpg.ch1.current]", c("对象：", CHURCH, True), c("别西卜真名仍是环境假说，需以三种权能完成确证。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("弱点：", BEEL_LIGHT, True), c("腐败残食会中断吞食；圣钉、铃、香与粉笔维持法阵。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("风险：", DANGER, True), c("判词缺失见证人印。裁决可执行，但其对象可能并不完整。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("如果等完整许可，我们会先被写成死人。进去。", GRAY)),
    ]))


def totem_line():
    item = ITEMS["exorcism_totem"]
    base = item["base_item"].split(":", 1)[-1]
    identity = custom_data_value(item).strip("{}")
    for line in read(item["source"]).splitlines():
        if line.startswith(f"give @a {base}[") and identity in line:
            return line.replace("give @a ", "give @s ", 1)
    raise RuntimeError(f"configured exorcism totem missing from {item['source']}")


def write_boss_and_rite():
    write(function_rel(ITEMS["exorcism_totem"]["give_function"]), totem_line())
    kit_keys = [item_key for loadout in CONFIG["cache_loadouts"].values() for item_key in loadout]
    reissue = ["execute if entity @s[tag=rpg.ch1.kit.issued] run return 0", "tag @s add rpg.ch1.kit.issued"]
    for item_key in kit_keys:
        item = ITEMS[item_key]
        witness_gate = " unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,limit=1]" if item_key == "pending_name_page" else ""
        reissue.append(f"execute unless items entity @s inventory.* {item['base_item']}[{item['match']}]{witness_gate} run function {item['give_function']}")
    reissue.append("execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,limit=1] run function rpg:campaign/beelzebub/witness/confirm_player")
    write("campaign/beelzebub/cache/reissue_missing.mcfunction", "\n".join(reissue))
    for n in range(1, 6):
        write(f"campaign/beelzebub/witness/skill{n}.mcfunction", "\n".join([
            "tag @s add rpg.ch1.witness.player",
            f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['scene_radius']},limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.witness.player,limit=1] rpg_ch1_id unless entity @s[tag=rpg.ch1.witness.skill.{n}] run function rpg:campaign/beelzebub/witness/record{n}",
            "tag @s remove rpg.ch1.witness.player",
        ]))
        write(f"campaign/beelzebub/witness/record{n}.mcfunction", "\n".join([
            f"tag @s add rpg.ch1.witness.skill.{n}",
            tell(f"@a[tag=rpg.ch1.current,distance=..{RUNTIME['scene_radius']}]", c("[权能见证] ", CHURCH, True), c(f"第 {n} 项不同权能已与粮仓证物吻合。", GRAY)),
            "function rpg:campaign/beelzebub/witness/recount",
        ]))
    write("campaign/beelzebub/witness/recount.mcfunction", "\n".join([
        "scoreboard players set @s rpg_ch1_seen 0",
    ] + [f"execute if entity @s[tag=rpg.ch1.witness.skill.{n}] run scoreboard players add @s rpg_ch1_seen 1" for n in range(1, 6)] + [
        "execute if score @s rpg_ch1_seen matches 3.. unless entity @s[tag=rpg.ch1.witness.ready] run function rpg:campaign/beelzebub/witness/confirm",
    ]))
    write("campaign/beelzebub/witness/confirm.mcfunction", "\n".join([
        "tag @s add rpg.ch1.witness.ready", "tag @s add rpg.ch1.witness.controller",
        "execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.witness.controller,limit=1] rpg_ch1_id run function rpg:campaign/beelzebub/witness/confirm_player",
        "tag @s remove rpg.ch1.witness.controller",
        tell(f"@a[tag=rpg.ch1.current,distance=..{RUNTIME['scene_radius']}]", c("[真名确证] ", CHURCH, True), c("三种不可重复的权能已被见证；现实承认别西卜来过。", BEEL_LIGHT)),
    ]))
    write("campaign/beelzebub/witness/confirm_player.mcfunction", "\n".join([
        f"clear @s {ITEMS['pending_name_page']['base_item']}[{ITEMS['pending_name_page']['match']}]",
        f"execute unless entity @s[tag=rpg.name.{BOSS['lord_score']}] run function rpg:inquest/reveal/{BOSS['lord_score']}",
        f"execute if entity @s[tag=rpg.name.{BOSS['lord_score']}] unless items entity @s inventory.* {ITEMS['confirmed_name_page']['base_item']}[{ITEMS['confirmed_name_page']['match']}] run function {ITEMS['confirmed_name_page']['give_function']}",
    ]))
    write("campaign/beelzebub/stage/7_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 58", "bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅰ 镇压 · 见证三种权能", BEEL, True)),
        "scoreboard players set @s rpg_ch1_seen 0", "function rpg:campaign/beelzebub/spawn/boss",
        tell("@a[tag=rpg.ch1.current]", c("卡西安：", CHURCH, True), c("登记人口，一万三千四百二十一。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("卡西安：", CHURCH, True), c("应发口粮，一万三千四百二十一。实发口粮，零。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("别西卜：", BEEL, True), c("可你们的账，一直都是平的。欢迎赴宴。", BEEL_LIGHT)),
        tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("先看祂怎样进食。我们需要证据，不只是伤口。", GRAY)),
    ]))
    write("campaign/beelzebub/spawn/boss.mcfunction", "\n".join([
        f"execute positioned {BOSS['spawn']} run tag @e[type={BOSS['entity_type']},tag=rpg.advent,scores={{rpg_dm_lord={BOSS['lord_score']}}},distance=..{RUNTIME['boss_claim_radius']}] add rpg.ch1.preexisting",
        f"execute positioned {BOSS['spawn']} run function {BOSS['summon_function']}",
        f"execute positioned {BOSS['spawn']} run tag @e[type={BOSS['entity_type']},tag=rpg.advent,tag=!rpg.ch1.preexisting,scores={{rpg_dm_lord={BOSS['lord_score']}}},distance=..{RUNTIME['boss_claim_radius']},sort=nearest,limit=1] add rpg.ch1.boss.new",
        f"scoreboard players operation @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.new,limit=1] rpg_ch1_id = @s rpg_ch1_id",
        f"attribute @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.new,limit=1] minecraft:max_health base set {BOSS['health']}",
        f"data merge entity @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.new,limit=1] {{Health:{BOSS['health']}f,CustomName:" + row(c(BOSS["display_name"], BEEL, True)) + "}",
        f"tag @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.new,limit=1] add rpg.ch1.boss", f"tag @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.new] remove rpg.ch1.boss.new", "tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting",
    ]))
    write("campaign/beelzebub/claim_rite.mcfunction", "\n".join([
        "tag @s add rpg.ch1.rite", f"scoreboard players operation @s rpg_ch1_id = @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current,sort=nearest,limit=1,distance=..{RUNTIME['rite_bind_radius']}] rpg_ch1_id",
        tell("@a[tag=rpg.ch1.current,distance=..20]", c("[Ⅱ · 镇魔] ", CHURCH, True), c("真名与点燃图腾已经将祂绑定。", GRAY)),
    ]))
    write("campaign/beelzebub/stage/7_tick.mcfunction", "\n".join([
        "execute as @a[tag=rpg.ch1.current,tag=!rpg.ch1.kit.issued] run function rpg:campaign/beelzebub/cache/reissue_missing",
        f"tag @e[type={BOSS['entity_type']},tag=rpg.ch1.boss] remove rpg.ch1.boss.current",
        f"execute as @e[type={BOSS['entity_type']},tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.boss.current",
        f"execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.ch1.rite,distance=..{RUNTIME['scene_radius'] - 8}] at @s if entity @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current,distance=..{RUNTIME['rite_bind_radius']},limit=1] run function rpg:campaign/beelzebub/claim_rite",
        f"execute if entity @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=0}},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅰ 镇压 · 亲历三种不同权能", BEEL, True)),
        f"execute if entity @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=1}},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅱ 镇魔 · 真名 + 点燃图腾", CHURCH, True)),
        "execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=2},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅲ 固阵 · 稳定度推进至 100", SEAL, True)),
        "execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅳ 裁决 · 四选一", PACT, True)),
        "execute if score @s rpg_ch1_time matches 60 run tellraw @a[tag=rpg.ch1.current] " + row(c("别西卜：", BEEL, True), c("城市教会了我：吃掉一个人前，最好先吃掉他的名字。", BEEL_LIGHT)),
        "execute if score @s rpg_ch1_time matches 140 run tellraw @a[tag=rpg.ch1.current] " + row(c("[见证规则] ", CHURCH, True), c("环境证物只是推论；亲历三种不同招式后，现实才承认真名。", GRAY)),
        "execute if score @s rpg_ch1_time matches 220 run tellraw @a[tag=rpg.ch1.current] " + row(c("伊莱亚：", CHURCH, True), c("重复招式只算一证。看余烬、吞噬、蝇群、腐宴或饥啮的差异。", GRAY)),
        "execute if score @s rpg_ch1_time matches 340 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", WITNESS, True), c("饥饿会逼人求生；祂在劝你放弃自己。别把两者混为一谈。", GRAY)),
        "execute if score @s rpg_ch1_time matches 430 run tellraw @a[tag=rpg.ch1.current] " + row(c("别西卜：", BEEL, True), c("每一只蝇，都记得一顿没有发生过的晚餐。", BEEL_LIGHT)),
        "execute if score @s rpg_ch1_time matches 540 run tellraw @a[tag=rpg.ch1.current] " + row(c("别西卜：", BEEL, True), c("被吃掉以后，就再也不会挨饿。", BEEL_LIGHT)),
        f"execute unless entity @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current,limit=1] if score @s rpg_ch1_time matches {RECOVERY['boss_missing_ticks']}.. run function rpg:campaign/beelzebub/recover_boss",
    ]))
    write("campaign/beelzebub/recover_boss.mcfunction", "\n".join([
        f"tag @e[type={BOSS['entity_type']},tag=rpg.ch1.boss] remove rpg.ch1.boss.current",
        f"execute as @e[type={BOSS['entity_type']},tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.boss.current",
        f"kill @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current]",
        "scoreboard players set @s rpg_ch1_empty 0", "scoreboard players add @s rpg_ch1_fail 1",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup",
        tell("@a[tag=rpg.ch1.current]", c("[仪式恢复] ", CHAPTER, True), c("稳定归零或躯壳异常消散；从 Boss 入口检查点重开，不重置调查。", GRAY)),
        "scoreboard players set @s rpg_ch1_time 0", "function rpg:campaign/beelzebub/stage/7_enter",
    ]))
    write("campaign/beelzebub/rite/collapse.mcfunction", "\n".join([
        "tag @s add rpg.ch1.rite.active",
        f"execute as @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..{RUNTIME['rite_bind_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_rite_id run kill @s",
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id at @s run function rpg:campaign/beelzebub/recover_boss",
    ]))
    choice = row(c("[消灭]", ELIMINATE, True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 1"}), c("  [放逐]", WITNESS, True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 2"}), c("  [封印]", SEAL, True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 3"}), c("  [契约]", PACT, True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 4"}))
    write("campaign/beelzebub/rite/stage4.mcfunction", "\n".join([
        "scoreboard players remove @s rpg_ex_time 1", "particle minecraft:end_rod ~ ~0.9 ~ 0.9 0.55 0.9 0.05 4 force",
        "execute if score @s rpg_ex_time matches 200 run tellraw @a[tag=rpg.ch1.current,distance=..14] " + choice,
        "execute if score @s rpg_ex_time matches ..0 run scoreboard players set @s rpg_ex_time 300",
        "execute if score @s rpg_ex_time matches 300 run tellraw @a[tag=rpg.ch1.current,distance=..14] " + row(c("[裁决尚待] ", CHURCH, True), c("缺页正在撕扯法阵；必须由见证人主动落笔。", GRAY)),
        "execute if score @s rpg_ex_time matches 300 run tellraw @a[tag=rpg.ch1.current,distance=..14] " + choice,
    ]))


def reward_item(kind, label, color, lore):
    item = ITEMS[f"{kind}_resonance"]
    name = row(c("[裁决残响] ", color, True), c(f"别西卜 · {label}", BEEL_LIGHT))
    lore_json = json.dumps([[c("+------------------+", "white")], [c(lore, GRAY)], [c("别西卜逃脱后留下的未完成判词", ASH)], [c("第一章首通纪念 · 非完整领主掉落", DARK)], [c("+------------------+", "white")]], ensure_ascii=False, separators=(",", ":"))
    write(function_rel(item["give_function"]), f"give @s {item['base_item']}[custom_name={name},lore={lore_json},enchantment_glint_override=true,max_stack_size=1,item_model=\"{item['item_model']}\",custom_data={custom_data_value(item)}]")


def write_verdict_epilogue():
    specs = {"eliminate": (1, "断刃", ELIMINATE, "刀锋只斩中饕宴的空壳。"), "banish": (2, "逐影", CHURCH, "完整判词放逐了饥饿投下的影子。"), "seal": (3, "空灯", SEAL, "灯芯里没有领主的灵魂。"), "pact": (4, "伪约", PACT, "契约只留下一个胃的签名。")}
    for kind, (choice, label, color, lore) in specs.items():
        write(f"campaign/beelzebub/verdict/{kind}.mcfunction", "\n".join([
            "tag @s add rpg.ch1.rite.active",
            f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_choice {choice}",
            f"execute as @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..{RUNTIME['rite_bind_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_rite_id at @s run function rpg:campaign/beelzebub/escape_boss",
            "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_stage 8",
            "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_time 0",
            "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id at @s run function rpg:campaign/beelzebub/stage/8_enter",
            "function rpg:inquest/tool/cleanup",
        ])); reward_item(kind, label, color, lore)
    write("campaign/beelzebub/escape_boss.mcfunction", "\n".join([
        "particle minecraft:flash{color:5925662} ~ ~1 ~ 0 0 0 0 1 force", "particle minecraft:spore_blossom_air ~ ~1 ~ 2.8 1.2 2.8 0.08 90 force", "particle minecraft:large_smoke ~ ~1 ~ 1.4 0.8 1.4 0.06 45 force",
        tell("@a[tag=rpg.ch1.current,distance=..48]", c("别西卜：", BEEL, True), c("裁决的是名字，不是饥饿。我们会再见。", BEEL_LIGHT)), "kill @s",
    ]))
    write("campaign/beelzebub/stage/8_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 88", "bossbar set rpg:chapter1 name " + row(c("四种不完整的裁决｜见证人印缺失", DANGER, True)),
        tell("@a[tag=rpg.ch1.current]", c("米拉：", WITNESS, True), c("它们不是忘了最后一页。是故意撕掉的。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("若写回所有姓名，教廷篡改粮册的证据也会显现。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("[真相复盘] ", CHAPTER, True), c("塞维拉下令删证，卡西安执行清洗，别西卜借空缺进食；三者同时成立。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("[裁决结果] ", DANGER, True), c("你裁决了教廷承认存在的容器，却没能裁决被删去姓名的宴席。", GRAY)),
    ])); write("campaign/beelzebub/stage/8_tick.mcfunction", "execute if score @s rpg_ch1_time matches 140.. run function rpg:campaign/beelzebub/advance")
    witness = ACTORS["npcs"]["mira_testimony"]
    witness_tags = ",".join(f'"{tag}"' for tag in [*witness["tags"], "rpg.ch1.new"])
    write("campaign/beelzebub/stage/9_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 94", "bossbar set rpg:chapter1 name " + row(c("活着的人必须有名字｜救下米拉", DANGER, True)),
        f"execute positioned {witness['spawn']} run summon {witness['entity_type']} ~ ~ ~ {{Tags:[{witness_tags}],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:" + row(c(witness["display_name"], WITNESS)) + "}",
        f"scoreboard players operation @e[type={witness['entity_type']},tag=rpg.ch1.new,sort=nearest,limit=1,distance=..20] rpg_ch1_id = @s rpg_ch1_id", f"tag @e[type={witness['entity_type']},tag=rpg.ch1.new] remove rpg.ch1.new",
        tell("@a[tag=rpg.ch1.current]", c("审判官 塞维拉：", CHURCH, True), c("所有见证人都是污染源。包括她，也包括你。", GRAY)),
    ]))
    rescue_button = "tellraw @a[tag=rpg.ch1.current] " + row(button("释放未经许可的魔力，救下米拉", DANGER, 13, "靠近米拉 12 格；这会让教廷确认你是边缘者"))
    write("campaign/beelzebub/stage/9_tick.mcfunction", "\n".join([
        "execute if score @s rpg_ch1_time matches 40 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", WITNESS, True), c("我叫米拉 · 维恩，今年二十二岁。", GRAY)),
        "execute if score @s rpg_ch1_time matches 85 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", WITNESS, True), c("我在慈济所学配药；薄荷要最后放，否则会苦。", GRAY)),
        "execute if score @s rpg_ch1_time matches 130 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", WITNESS, True), c("伊莱亚欠我两枚铜币，他总说下次会还。", GRAY)),
        "execute if score @s rpg_ch1_time matches 175 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", WITNESS, True), c("我害怕，也想活下去——所以我不是空壳。", GRAY)),
        "execute if score @s rpg_ch1_time matches 220 run " + rescue_button,
        "execute if score @s rpg_ch1_time matches 420 run " + rescue_button,
        "execute if score @s rpg_ch1_time matches 620 run " + rescue_button,
        "execute if score @s rpg_ch1_time matches 700.. if score @s rpg_ch1_obj matches 0 run scoreboard players set @s rpg_ch1_time 300",
        "execute if score @s rpg_ch1_obj matches 1.. run function rpg:campaign/beelzebub/advance",
    ]))
    write("campaign/beelzebub/rescue.mcfunction", "\n".join([
        "execute unless entity @s[tag=rpg.ch1.member] run return run tellraw @s " + row(c("[第一章] 你不在本次固定见证名单中。", DANGER)),
        "execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=9},limit=1] run return run tellraw @s " + row(c("[第一章] 现在没有需要救下的见证人。", GRAY)),
        "execute unless score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run return run tellraw @s " + row(c("[第一章] 你的章节编号与当前实例不符。", DANGER)),
        "execute unless score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run return run tellraw @s " + row(c("[第一章] 你的会话凭证已失效，请重新登记。", DANGER)),
        "execute unless score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_time matches 220.. run return run tellraw @s " + row(c("[第一章] 先听完米拉的四项人格见证。", GRAY)),
        "tag @s add rpg.ch1.rescue.player",
        f"tag @e[type={witness['entity_type']},tag=rpg.ch1.witness] remove rpg.ch1.witness.current",
        f"execute as @e[type={witness['entity_type']},tag=rpg.ch1.witness,tag=rpg.ch1.scene] if score @s rpg_ch1_id = @a[tag=rpg.ch1.rescue.player,limit=1] rpg_ch1_id run tag @s add rpg.ch1.witness.current",
        "tag @s remove rpg.ch1.rescue.player",
        f"execute unless entity @e[type={witness['entity_type']},tag=rpg.ch1.witness.current,distance=..12,limit=1] run return run tellraw @s " + row(c("[第一章] 你必须靠近本章节的米拉（12 格内）。", DANGER)),
        f"effect give @e[type={witness['entity_type']},tag=rpg.ch1.witness.current,limit=1] minecraft:regeneration 8 2 true", f"effect give @e[type={witness['entity_type']},tag=rpg.ch1.witness.current,limit=1] minecraft:absorption 60 3 true",
        "particle minecraft:totem_of_undying ~ ~1 ~ 1.1 0.8 1.1 0.08 60 force", "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_obj 1",
        tell("@a[tag=rpg.ch1.current]", c("[第一次释放] ", DANGER, True), c("圣力与魔化在同一道伤口中回应。", GRAY)),
    ]))


def write_completion_cleanup():
    write("campaign/beelzebub/stage/10_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 98", "bossbar set rpg:chapter1 name " + row(c("边缘者登记｜选择驱魔道路后完成归档", CHURCH, True)),
        tell("@a[tag=rpg.ch1.current]", c("塞维拉：", CHURCH, True), c("加入边缘者体系，或者作为污染源被处决。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("这不叫选择。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("塞维拉：", CHURCH, True), c("边缘者从来没有选择。", GRAY)),
        "tellraw @a[tag=rpg.ch1.current] " + row(button("打开驱魔师档案并选择道路", WITNESS, 1, "审判、守护或秘仪")),
        "execute as @a[tag=rpg.ch1.current,scores={rpg_ex_path=0}] run function rpg:inquest/career",
        tell("@a[tag=rpg.ch1.current]", c("[归档规则] ", CHAPTER, True), c("至少保留 30 秒选择窗口；未选择道路时章节不会自动结算。", GRAY)),
    ]))
    career_prompt = "tellraw @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] " + row(button("选择或确认驱魔道路", WITNESS, 1, "选择后才会结算首通奖励"))
    write("campaign/beelzebub/stage/10_tick.mcfunction", "\n".join([
        "tag @a remove rpg.ch1.stage10.player",
        "tag @s add rpg.ch1.stage10.controller",
        "execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.stage10.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.stage10.controller,limit=1] rpg_ch1_session run tag @s add rpg.ch1.stage10.player",
        "tag @s remove rpg.ch1.stage10.controller",
        "execute unless entity @s[tag=rpg.ch1.debug.no_commit] as @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed,scores={rpg_ex_path=1..}] run function rpg:campaign/beelzebub/career_confirm",
        "execute unless entity @s[tag=rpg.ch1.debug.no_commit] if score @s rpg_ch1_time matches 200 run " + career_prompt,
        "execute unless entity @s[tag=rpg.ch1.debug.no_commit] if score @s rpg_ch1_time matches 600 run " + career_prompt,
        "execute unless entity @s[tag=rpg.ch1.debug.no_commit] if score @s rpg_ch1_time matches 1000.. if entity @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] run scoreboard players set @s rpg_ch1_time 600",
        "execute unless entity @s[tag=rpg.ch1.debug.no_commit] if score @s rpg_ch1_time matches 600.. unless entity @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] run function rpg:campaign/beelzebub/finish",
        "execute if entity @s[tag=rpg.ch1.debug.no_commit] if score @s rpg_ch1_time matches 200 run tellraw @a[tag=rpg.ch1.stage10.player] " + row(c("[调试预览] ", CHAPTER, True), c("永久归档、奖励、阅历与成就均已锁止。", GRAY)),
        "execute if entity @s[tag=rpg.ch1.debug.no_commit] if score @s rpg_ch1_time matches 400.. run scoreboard players set @s rpg_ch1_time 0",
    ]))
    write("campaign/beelzebub/career_confirm.mcfunction", "\n".join([
        "function rpg:campaign/beelzebub/complete_player",
        "tag @s add rpg.ch1.career.confirmed",
        tell("@s", c("[道路确认] ", CHURCH, True), c("边缘者档案已归档；首通奖励与裁决记录已写入。", GRAY)),
    ]))
    write("campaign/beelzebub/complete_player.mcfunction", "\n".join([
        "scoreboard players operation @s rpg_ch1_verdict = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice",
        "execute if score @s rpg_ch1_reward matches 1.. run return 0", "scoreboard players set @s rpg_ch1_reward 1", "scoreboard players add @s rpg_ex_xp 60",
        f"function {ITEMS['borderer_dossier']['give_function']}",
        f"execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 1 run function {ITEMS['eliminate_resonance']['give_function']}",
        f"execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 2 run function {ITEMS['banish_resonance']['give_function']}",
        f"execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 3 run function {ITEMS['seal_resonance']['give_function']}",
        f"execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 4 run function {ITEMS['pact_resonance']['give_function']}",
        "scoreboard players set @s rpg_ch1_done 1", "scoreboard players set @s rpg_ch1_next 1", "tag @s add rpg.ch1.borderer", "function rpg:inquest/career/sync", "function rpg:inquest/career/claim", "advancement grant @s only rpg:campaign/beelzebub",
    ]))
    name = row(c("[教廷档案] ", CHURCH, True), c("边缘者临时入院令", WITNESS)); lore = json.dumps([[c("+------------------+", "white")], [c("编号：VAC-01-BZB", CHAPTER)], [c("罪名：目击空缺者，并擅自释放魔力", GRAY)], [c("处置：编入驱魔院，终身监视", DANGER)], [c("权限：开启高阶恶魔追踪", BEEL_LIGHT)], [c("+------------------+", "white")]], ensure_ascii=False, separators=(",", ":"))
    dossier = ITEMS["borderer_dossier"]
    write(function_rel(dossier["give_function"]), f"give @s {dossier['base_item']}[custom_name={name},lore={lore},enchantment_glint_override=true,max_stack_size=1,item_model=\"{dossier['item_model']}\",custom_data={custom_data_value(dossier)}]")
    cleanup = [
        "tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.cleanup.controller",
        "tag @a remove rpg.ch1.cleanup.player",
        "execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.cleanup.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup.player",
        f"tag @e[tag=rpg.ch1.scene,distance=..{RUNTIME['scene_radius']}] remove rpg.ch1.cleanup", f"execute as @e[tag=rpg.ch1.scene,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup",
        f"tag @e[tag=rpg.ch1.minion,distance=..{RUNTIME['scene_radius']}] remove rpg.ch1.cleanup", f"execute as @e[tag=rpg.ch1.minion,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup",
        f"tag @e[tag=rpg.ch1.boss,distance=..{RUNTIME['scene_radius']}] remove rpg.ch1.cleanup", f"execute as @e[tag=rpg.ch1.boss,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup",
        f"execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup",
        "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.accepted", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.member", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.party", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.host", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.current", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.kit.issued", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.career.confirmed", "scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_id 0", "scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_session 0", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.cleanup.player",
        "bossbar remove rpg:chapter1", f"kill @e[tag=rpg.ch1.cleanup,distance=..{RUNTIME['scene_radius']}]",
    ]
    write("campaign/beelzebub/finish.mcfunction", "\n".join(cleanup))
    write("campaign/beelzebub/abort.mcfunction", "\n".join(["execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return 0", tell("@a[tag=rpg.ch1.current]", c("[第一章] ", CHAPTER, True), c("实例已按章节 ID 安全清理；永久档案不受影响。", GRAY))] + cleanup))


def write_debug_tools():
    """Generate operator-invoked QA helpers without touching permanent progress."""
    if not CONFIG["debug"]["enabled"]:
        return
    namespace = CONFIG["debug"]["function_namespace"]
    prefix = namespace.split(":", 1)[1]
    entries = CONFIG["debug"]["entry_points"]
    write(f"{prefix}/start.mcfunction", "\n".join([
        tell("@s", c("[章节调试] ", CHAPTER, True), c("当前位置为原点；朝向仍按正式场地校验吸附。", GRAY)),
        "function rpg:campaign/beelzebub/start",
    ]))
    give_lines = [tell("@s", c("[章节调试] ", CHAPTER, True), c("发放配置中登记的全部第一章物品；不写入完成、奖励或职业进度。", GRAY))]
    for key, item in sorted(ITEMS.items()):
        give_lines += [f"function {item['give_function']}", tell("@s", c(f"  + {key}", DARK))]
    write(f"{prefix}/give_all_items.mcfunction", "\n".join(give_lines))

    write(f"{prefix}/spawn_boss.mcfunction", "\n".join([
        f"execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},limit=1] run return run tellraw @s " + row(c("[章节调试] 当前范围内没有第一章控制器。", DANGER)),
        "tag @s add rpg.ch1.debug.caller",
        f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},sort=nearest,limit=1] at @s unless entity @e[type={BOSS['entity_type']},tag=rpg.ch1.boss,distance=..{RUNTIME['scene_radius']},limit=1] run function rpg:campaign/beelzebub/spawn/boss",
        "tag @s remove rpg.ch1.debug.caller",
    ]))
    worker = ["scoreboard players operation #ch1_debug_obj rpg_ch1_obj = @s rpg_ch1_obj"]
    for key, spec in sorted(MINIONS.items(), key=lambda pair: pair[1]["role"]):
        worker.append(f"execute positioned {spec['spawn']} run function rpg:campaign/beelzebub/spawn/minion/{key}")
    worker.append("scoreboard players operation @s rpg_ch1_obj = #ch1_debug_obj rpg_ch1_obj")
    write(f"{prefix}/spawn_all_minions_worker.mcfunction", "\n".join(worker))
    write(f"{prefix}/spawn_all_minions.mcfunction", "\n".join([
        f"execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},limit=1] run return run tellraw @s " + row(c("[章节调试] 当前范围内没有第一章控制器。", DANGER)),
        f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},sort=nearest,limit=1] at @s run function rpg:{prefix}/spawn_all_minions_worker",
    ]))

    position_lines = [tell("@s", c("+------ 第一章 · 可配置坐标 ------+", CHAPTER, True)),
                      tell("@s", c("原点规则：", CHURCH, True), c(CONFIG["debug"]["origin_policy"], GRAY))]
    for kind, key, position in iter_positions(CONFIG):
        position_lines.append(tell("@s", c(f"{kind}.{key}　", BEEL_LIGHT), c(position, GRAY)))
    write(f"{prefix}/list_positions.mcfunction", "\n".join(position_lines))

    reset_lines = [
        "tag @s add rpg.ch1.debug.controller",
        f"tag @e[tag=rpg.ch1.debug.current,distance=..{RUNTIME['scene_radius']}] remove rpg.ch1.debug.current",
        f"execute as @e[tag=rpg.ch1.scene,tag=!rpg.ch1.controller,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.debug.current",
        f"execute as @e[tag=rpg.ch1.minion,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.debug.current",
        f"execute as @e[tag=rpg.ch1.boss,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.debug.current",
        f"execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup",
        f"kill @e[tag=rpg.ch1.debug.current,distance=..{RUNTIME['scene_radius']}]",
        "tag @s remove rpg.ch1.recap.anomaly", "tag @s remove rpg.ch1.recap.minions",
        "tag @s remove rpg.ch1.recap.area", "tag @s remove rpg.ch1.recap.hypothesis",
        "tag @s remove rpg.ch1.recap.prep", "tag @s remove rpg.ch1.witness.ready",
        "tag @s remove rpg.ch1.debug.no_commit",
        "scoreboard players set @s rpg_ch1_time 0", "scoreboard players set @s rpg_ch1_obj 0",
        "scoreboard players set @s rpg_ch1_sub 0", "scoreboard players set @s rpg_ch1_guard 0",
        "scoreboard players set @s rpg_ch1_rescue 0", "tag @s remove rpg.ch1.debug.controller",
    ]
    write(f"{prefix}/stage_reset.mcfunction", "\n".join(reset_lines))
    for stage in CONFIG["debug"]["stage_jump_targets"]:
        stage_setup = [
            f"function rpg:{prefix}/stage_reset",
            "tag @s add rpg.ch1.debug.no_commit",
        ]
        if stage == 7:
            stage_setup.append("tag @s add rpg.ch1.witness.ready")
        stage_setup += [
            f"scoreboard players set @s rpg_ch1_stage {stage}",
            f"function rpg:campaign/beelzebub/stage/{stage}_enter",
        ]
        write(f"{prefix}/stage/{stage}_worker.mcfunction", "\n".join(stage_setup))
        write(f"{prefix}/stage/{stage}.mcfunction", "\n".join([
            f"execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},limit=1] run return run tellraw @s " + row(c("[章节调试] 当前范围内没有第一章控制器。", DANGER)),
            f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..{RUNTIME['active_radius']},sort=nearest,limit=1] at @s run function rpg:{prefix}/stage/{stage}_worker",
            tell("@s", c("[章节调试] ", CHAPTER, True), c(f"已跳转到 Stage {stage}；未写入永久进度。", GRAY)),
        ]))

    menu = [tell("@s", c("+------ 第一章 · 调试台 ------+", CHAPTER, True)),
            tell("@s", c(f"配置摘要　{config_digest(CONFIG)[:12]}", DARK)),
            tell("@s", command_button("以当前位置开案", CHURCH, f"/function {entries['start']}", "正式预检仍然生效"),
                 command_button("全部物品", WITNESS, f"/function {entries['give_all_items']}", "仅发物品，不写永久进度")),
            tell("@s", command_button("召唤 Boss", BEEL_LIGHT, f"/function {entries['spawn_boss']}", "在当前控制器的配置坐标生成"),
                 command_button("召唤五罪仆", BEEL, f"/function {entries['spawn_all_minions']}", "按配置波次坐标生成，但不推进目标计数")),
            tell("@s", command_button("列出全部坐标", SEAL, f"/function {entries['list_positions']}", "显示配置键与相对坐标")),
            tell("@s", c("阶段跳转　", GRAY))]
    for start in range(0, 11, 4):
        menu.append(tell("@s", *[command_button(str(stage), PACT if stage >= 7 else CHAPTER,
                                                  f"/function {namespace}/stage/{stage}", f"清理临时实体并进入 Stage {stage}")
                                   for stage in range(start, min(start + 4, 11))]))
    write(f"{prefix}/menu.mcfunction", "\n".join(menu))

    manifest_path = ROOT / CONFIG["integration"]["generated_manifest"]
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest(CONFIG), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def advancement():
    p = ROOT / "data" / "rpg" / "advancement" / "campaign" / "beelzebub.json"; p.parent.mkdir(parents=True, exist_ok=True)
    payload = {"display": {"icon": {"id": "minecraft:poisonous_potato"}, "title": [{"text": "第一章 · 空缺者", "color": CHAPTER, "bold": True, "italic": False}], "description": [{"text": "别西卜逃脱，而你被教廷登记为边缘者", "color": "gray", "italic": False}], "frame": "challenge", "show_toast": True, "announce_to_chat": True, "hidden": False}, "criteria": {"story": {"trigger": "minecraft:impossible"}}}
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build():
    setup_objectives(); hook_runtime(); hook_panel(); write_menu_and_membership(); write_start_and_controller(); write_preflight()
    write_stage0_2(); write_minions(); write_tracking_inquest_prep(); write_boss_and_rite(); write_verdict_epilogue(); write_completion_cleanup(); write_debug_tools(); advancement()
    print(f"Beelzebub Chapter I generated: {ROOT}")


if __name__ == "__main__": build()
