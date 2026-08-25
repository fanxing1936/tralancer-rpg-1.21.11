#!/usr/bin/env python3
"""Generate Chapter I: The Vacants / Beelzebub campaign.

One public controller is allowed because the UI has one bossbar, but controller,
participants, scene points, minions, boss and rite all carry rpg_ch1_id. Thus
unrelated nearby players/demons/rites cannot be claimed by the chapter.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
FUN = ROOT / "data" / "rpg" / "function"
CHAPTER, CHURCH, BEEL, BEEL_LIGHT = "#B8A98B", "#D4AF37", "#5A6B1E", "#B5D957"
ASH, DANGER, GRAY, DARK = "#706B5E", "#8B2500", "gray", "dark_gray"


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


def display(text, color, key):
    txt = json.dumps(row(c(text, color, True)), ensure_ascii=False)
    return ("summon minecraft:text_display ~ ~1.15 ~ {Tags:[\"rpg.ch1.scene\",\"rpg.ch1.label\","
            f"\"rpg.ch1.{key}.label\",\"rpg.ch1.new\"],billboard:\"center\",see_through:1b,"
            f"shadow:1b,background:0,view_range:0.65f,text:{txt}}}")


def owned_spawn(local, key, label, color):
    return [
        f"execute positioned {local} run summon minecraft:marker ~ ~ ~ {{Tags:[\"rpg.ch1.scene\",\"rpg.ch1.point\",\"rpg.ch1.{key}\",\"rpg.ch1.new\"]}}",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] rpg_ch1_id = @s rpg_ch1_id",
        "tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] remove rpg.ch1.new",
        f"execute positioned {local} run {display(label, color, key)}",
        "scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] rpg_ch1_id = @s rpg_ch1_id",
        "tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] remove rpg.ch1.new",
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
        hook = (f"execute if entity @s[tag=rpg.ch1.boss] at @s as @a[tag=rpg.ch1.member,tag=rpg.ch1.party,tag=rpg.holy,distance=..18,gamemode=!spectator] "
                f"if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,sort=nearest,limit=1,distance=..18] rpg_ch1_id run function rpg:campaign/beelzebub/witness/skill{n}")
        if hook not in data: data = hook + "\n" + data
        save(rel, data)

    # Existing true-name owners cannot skip this chapter's three-witness gate.
    rel = "inquest/stage1.mcfunction"; data = read(rel)
    old = "execute if score @s rpg_dm_lord matches 4 if entity @a[tag=rpg.name.4,distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] run return run function rpg:inquest/bind/4"
    generic = "execute if entity @s[tag=!rpg.ch1.boss] if score @s rpg_dm_lord matches 4 if entity @a[tag=rpg.name.4,distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] run return run function rpg:inquest/bind/4"
    campaign = "execute if entity @s[tag=rpg.ch1.boss] if score @s rpg_dm_lord matches 4 if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,distance=..72,limit=1] rpg_ch1_id if entity @a[tag=rpg.ch1.member,tag=rpg.name.4,distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] run return run function rpg:inquest/bind/4"
    data = data.replace(generic, old).replace(campaign, old)
    if old not in data: raise RuntimeError("canonical Beelzebub bind line missing")
    save(rel, data.replace(old, generic + "\n" + campaign, 1))

    # Stability collapse must recover the chapter checkpoint instead of marking
    # the soul for a generic eliminate drop. Verdict timeout repeats the choice
    # prompt and never silently chooses banishment for the player.
    rel = "inquest/anchor_collapse.mcfunction"; data = read(rel)
    route = ("execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = "
             "@e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_ch1_id "
             "if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_rite_id "
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
                 "@e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_ch1_id "
                 "if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_rite_id "
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
        "execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run tellraw @s " + row(button("接受后方城市调查令", CHURCH, 12, "以当前位置建立无地形破坏的章节实例")),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] unless entity @s[tag=rpg.ch1.accepted] run tellraw @s " + row(button("加入当前调查", BEEL_LIGHT, 14, "需在控制器 96 格内；裁决开始后关闭加入")),
        "execute if entity @s[tag=rpg.ch1.accepted] run tellraw @s " + row(c("状态：已登记为参与者", BEEL_LIGHT, True)),
        "execute if score @s rpg_ch1_done matches 1.. run tellraw @s " + row(c("身份：教廷边缘者", CHURCH, True)),
        "execute if score @s rpg_ch1_next matches 1.. run tellraw @s " + row(button("高阶档案·失窃王冠", "#C9B5FF", 15, "打开路西法追踪入口")),
        tell("@s", c("异常 → 空缺者 → 罪仆 → 追踪 → 真名 → 器具 → 四阶段 → 裁决 → 救援 → 强化", DARK)),
        tell("@s", button("返回玩家面板", "#8FC7FF", 8, "返回总览")),
    ]))
    write("campaign/beelzebub/join.mcfunction", "\n".join([
        "execute if entity @s[tag=rpg.ch1.accepted] run return run tellraw @s " + row(c("[第一章] 你已经在参与名单中。", GRAY)),
        "execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1] run return run tellraw @s " + row(c("[第一章] 请先抵达调查区域。", DANGER)),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1,scores={rpg_ch1_stage=3..}] run return run tellraw @s " + row(c("[第一章] 罪仆已经封锁街区，成员名单已锁定。", DANGER)),
        "tag @s add rpg.ch1.accepted", "tag @s add rpg.ch1.member",
        "tag @s remove rpg.ch1.kit.issued", "tag @s remove rpg.ch1.career.confirmed",
        "scoreboard players operation @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] rpg_ch1_id",
        "scoreboard players operation @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] rpg_ch1_session",
        "tag @s add rpg.ch1.roster.joiner",
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.roster.joiner,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_roster 1",
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1,scores={rpg_ch1_roster=5..}] run scoreboard players set @s rpg_ch1_roster 4",
        "tag @s remove rpg.ch1.roster.joiner",
        "execute unless items entity @s inventory.* minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] run function rpg:campaign/beelzebub/give/totem",
        tell("@s", c("[参与登记] ", CHURCH, True), c("共享进度；首通奖励仍按个人档案幂等结算。", GRAY)),
    ]))
    write("campaign/beelzebub/next_hunt.mcfunction", "\n".join([
        "execute unless score @s rpg_ch1_next matches 1.. run return run tellraw @s " + row(c("[权限不足] 完成第一章后开放。", DANGER)),
        tell("@s", c("[高阶追踪] ", "#C9B5FF", True), c("第二档案：路西法 · 王冠失窃案", GRAY)),
        tell("@s", c("北部圣库的加冕圣物失踪；现场只留下一根向下坠落的羽毛。", ASH)),
        "function rpg:panel/inquest",
    ]))


def write_start_and_controller():
    write("campaign/beelzebub/start.mcfunction", "\n".join([
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s " + row(c("[第一章] 已有调查实例；请从档案选择加入。", DANGER)),
        "scoreboard players add #next rpg_ch1_id 1", "execute if score #next rpg_ch1_id matches ..0 run scoreboard players set #next rpg_ch1_id 1",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.ch1.controller\",\"rpg.ch1.anchor\",\"rpg.ch1.scene\",\"rpg.ch1.new\"]}",
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
        "execute as @a[tag=rpg.ch1.member,distance=..96,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run tag @s add rpg.ch1.party",
        "execute as @a[tag=rpg.ch1.party] run tag @s add rpg.ch1.current",
        "bossbar set rpg:chapter1 players @a[tag=rpg.ch1.current,distance=..128]",
        "execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/roster/failure_tick",
        "execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/roster/failure_tick",
        "execute unless entity @a[tag=rpg.ch1.current,distance=..128,gamemode=!spectator] as @e[type=minecraft:vindicator,tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run scoreboard players add @s rpg_fall 1",
        "execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss,scores={rpg_fall=12001..}] run scoreboard players set @s rpg_fall 12000",
        "execute unless entity @a[tag=rpg.ch1.current,distance=..128,gamemode=!spectator] run return 0",
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
        "execute if score @s rpg_ch1_empty matches 200.. run function rpg:campaign/beelzebub/roster/failure_recover",
    ]))
    write("campaign/beelzebub/roster/failure_recover.mcfunction", "\n".join([
        "scoreboard players set @s rpg_ch1_empty 0",
        "execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/recover_minions",
        "execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/recover_boss",
    ]))


def write_preflight():
    """Turn the freshly written start into a zero-residue 63+9 sample gate."""
    creation = read("campaign/beelzebub/start.mcfunction")
    write("campaign/beelzebub/start_pass.mcfunction", creation)
    write("campaign/beelzebub/start.mcfunction", "\n".join([
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s " + row(c("[第一章] 已有调查实例；请从档案选择加入。", DANGER)),
        "execute if entity @s[gamemode=spectator] run return run tellraw @s " + row(c("[场地校验] 旁观者不能发起章节。", DANGER)),
        "execute unless dimension minecraft:overworld run return run tellraw @s " + row(c("[场地校验] 第一章只能在主世界展开。", DANGER)),
        "execute if entity @e[type=minecraft:villager,distance=..72,limit=1] run return run tellraw @s " + row(c("[场地校验] 72 格内已有村民；请远离聚落。", DANGER)),
        "execute if entity @e[type=minecraft:iron_golem,distance=..72,limit=1] run return run tellraw @s " + row(c("[场地校验] 72 格内已有聚落守卫。", DANGER)),
        "execute if entity @e[tag=rpg.advent,distance=..72,limit=1] run return run tellraw @s " + row(c("[场地校验] 附近已有恶魔战斗。", DANGER)),
        "execute if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..72,limit=1] run return run tellraw @s " + row(c("[场地校验] 附近已有活动仪式。", DANGER)),
        "execute if entity @s[y_rotation=-45..45] run scoreboard players set @s rpg_ch1_yaw 0",
        "execute if entity @s[y_rotation=-45..45] rotated 0 0 run return run function rpg:campaign/beelzebub/scene/preflight",
        "execute if entity @s[y_rotation=45.01..135] run scoreboard players set @s rpg_ch1_yaw 1",
        "execute if entity @s[y_rotation=45.01..135] rotated 90 0 run return run function rpg:campaign/beelzebub/scene/preflight",
        "execute if entity @s[y_rotation=-135..-45.01] run scoreboard players set @s rpg_ch1_yaw 2",
        "execute if entity @s[y_rotation=-135..-45.01] rotated -90 0 run return run function rpg:campaign/beelzebub/scene/preflight",
        "scoreboard players set @s rpg_ch1_yaw 3",
        "execute rotated 180 0 run function rpg:campaign/beelzebub/scene/preflight",
    ]))
    bad = ("minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:water", "minecraft:lava",
           "minecraft:powder_snow", "minecraft:fire", "minecraft:soul_fire", "minecraft:magma_block",
           "minecraft:campfire", "minecraft:soul_campfire", "minecraft:cactus", "minecraft:sweet_berry_bush",
           "minecraft:wither_rose", "minecraft:pointed_dripstone")
    base = ["scoreboard players set @s rpg_ch1_safe 0"]
    for x in (-18, -12, -6, 0, 6, 12, 18):
        for z in (-6, 2, 10, 18, 26, 34, 42, 50, 58):
            cond = f"execute positioned ^{x} ^ ^{z} if loaded ~ ~ ~ " + " ".join(f"unless block ~ ~-1 ~ {b}" for b in bad)
            base.append(cond + " if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if block ~ ~2 ~ minecraft:air run scoreboard players add @s rpg_ch1_safe 1")
    for x in (-12, 0, 12):
        for z in (32, 44, 56):
            cond = f"execute positioned ^{x} ^ ^{z} if loaded ~ ~ ~ " + " ".join(f"unless block ~ ~-1 ~ {b}" for b in bad)
            base.append(cond + " if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if block ~ ~2 ~ minecraft:air if block ~ ~3 ~ minecraft:air if block ~ ~4 ~ minecraft:air run scoreboard players add @s rpg_ch1_safe 1")
    base += [
        "execute if score @s rpg_ch1_safe matches 72 run return run function rpg:campaign/beelzebub/start_pass",
        tell("@s", c("[场地校验失败] ", DANGER, True), c("需要宽 37、前方 58、后方 6、净空 5 的已加载安全平面；未生成任何章节实体。", GRAY)),
    ]
    write("campaign/beelzebub/scene/preflight.mcfunction", "\n".join(base))


def write_point_probe(key, message, extra=None):
    threshold = 80 if key.startswith("hyp") else 60 if key.startswith("anom") else 40
    write(f"campaign/beelzebub/probe/{key}.mcfunction", "\n".join([
        "scoreboard players set #ch1_point_ok rpg_ch1_seen 0",
        "tag @s add rpg.ch1.point.active",
        "execute as @a[tag=rpg.ch1.current,distance=..2.8,sort=nearest,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players set #ch1_point_ok rpg_ch1_seen 1",
        "execute if score #ch1_point_ok rpg_ch1_seen matches 1 run scoreboard players add @s rpg_ch1_seen 1",
        "execute if score #ch1_point_ok rpg_ch1_seen matches 0 run scoreboard players set @s rpg_ch1_seen 0",
        f"execute if score @s rpg_ch1_seen matches {threshold // 2} run playsound minecraft:block.amethyst_block.chime player @a[tag=rpg.ch1.current,distance=..8] ~ ~ ~ 0.35 1.4",
        f"execute if score @s rpg_ch1_seen matches {threshold}.. as @a[tag=rpg.ch1.current,distance=..2.8,sort=nearest,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run return run function rpg:campaign/beelzebub/point/{key}",
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
        "bossbar set rpg:chapter1 value 2", "bossbar set rpg:chapter1 name " + row(c("序幕｜第十三声钟", CHAPTER, True)),
        "playsound minecraft:ambient.cave master @a[tag=rpg.ch1.current] ~ ~ ~ 0.55 0.72",
        tell("@a[tag=rpg.ch1.current]", c("战争已经打了一百年。前线吃人，后方负责忘记。", ASH)),
        tell("@a[tag=rpg.ch1.current]", c("书记员 伊莱亚：", CHURCH, True), c("教廷说你没有听见第十三声钟。", GRAY)),
    ])); write("campaign/beelzebub/stage/0_tick.mcfunction", "execute if score @s rpg_ch1_time matches 160.. run function rpg:campaign/beelzebub/advance")
    lines = ["bossbar set rpg:chapter1 value 8", "bossbar set rpg:chapter1 name " + row(c("发现异常｜检查后街 3 处痕迹", CHAPTER, True))]
    for args in (("^6 ^ ^5", "anom1", "没有倒影的餐桌", ASH), ("^-7 ^ ^9", "anom2", "明日的死亡名册", CHURCH), ("^1 ^ ^15", "anom3", "第十三声钟灰", BEEL)): lines += owned_spawn(*args)
    write("campaign/beelzebub/stage/1_enter.mcfunction", "\n".join(lines))
    write("campaign/beelzebub/stage/1_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.{k}] at @s run function rpg:campaign/beelzebub/probe/{k}" for k in ("anom1", "anom2", "anom3")] + ["execute if score @s rpg_ch1_obj matches 3.. run function rpg:campaign/beelzebub/advance"]))
    write_point_probe("anom1", "她记得孩子的生日，却不记得为什么要爱他。")
    write_point_probe("anom2", "这不是预言，是明天的处决名单。", ["function rpg:campaign/beelzebub/give/totem"])
    write_point_probe("anom3", "钟灰中的透明虫翅指向慈济所。")
    write("campaign/beelzebub/stage/2_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 13", "bossbar set rpg:chapter1 name " + row(c("会回家的死者｜以圣器照见空缺", CHAPTER, True)),
        "execute positioned ^ ^ ^19 run summon minecraft:villager ~ ~ ~ {Tags:[\"rpg.ch1.scene\",\"rpg.ch1.vacant\",\"rpg.ch1.vacant.safe\",\"rpg.ch1.new\",\"rpg.vac.seen\",\"rpg.vacant\"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,CustomName:" + row(c("回家的母亲", GRAY)) + "}",
        "scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id", "tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new",
        "scoreboard players set @e[type=minecraft:villager,tag=rpg.ch1.vacant,sort=nearest,limit=1,distance=..40] rpg_vac_x -100",
        tell("@a[tag=rpg.ch1.current]", c("目标更新　", CHAPTER, True), c("手持驱魔图腾，靠近‘回家的母亲’。", GRAY)),
    ]))
    write("campaign/beelzebub/stage/2_tick.mcfunction", "\n".join([
        "tag @e[type=minecraft:villager,tag=rpg.ch1.vacant] remove rpg.ch1.vacant.current",
        "execute as @e[type=minecraft:villager,tag=rpg.ch1.vacant] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.vacant.current",
        "execute as @e[type=minecraft:villager,tag=rpg.ch1.vacant.current,limit=1] at @s if entity @a[tag=rpg.ch1.current,tag=rpg.holy,distance=..8,limit=1] run function rpg:vacant/reveal",
        "execute as @e[type=minecraft:villager,tag=rpg.ch1.vacant.current,scores={rpg_vac_x=-80..},limit=1] at @s run function rpg:campaign/beelzebub/vacant_reveal",
        "execute if score @s rpg_ch1_obj matches 1.. run function rpg:campaign/beelzebub/advance",
    ]))
    write("campaign/beelzebub/vacant_reveal.mcfunction", "\n".join([
        "tag @s remove rpg.vacant", "tag @s add rpg.vac.torn", "effect give @s minecraft:glowing 10 0 true", "particle minecraft:sculk_soul ~ ~1.3 ~ 0.35 0.6 0.35 0.03 25 force",
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("空缺者母亲：", ASH, True), c("今天是祷告日。每个人都有一份。", GRAY)),
        tell("@a[tag=rpg.ch1.current,distance=..24]", c("伊莱亚：", CHURCH, True), c("她知道自己是谁，却不知道‘自己’是什么意思。", GRAY)),
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_obj 1",
    ]))


def write_minions():
    roles = [("^8 ^ ^18", "zepar", 1), ("^-8 ^ ^18", "botis", 2),
             ("^12 ^ ^26", "bathin", 3), ("^-12 ^ ^26", "sallos", 4), ("^ ^ ^30", "purson", 5)]
    lines = ["bossbar set rpg:chapter1 value 20", "bossbar set rpg:chapter1 name " + row(c("五席未满｜第一轮 · 封路与追猎", BEEL, True)), "scoreboard players set @s rpg_ch1_obj 0", "scoreboard players set @s rpg_ch1_sub 1", "scoreboard players set @s rpg_ch1_guard 0",
             "execute unless entity @e[type=minecraft:villager,tag=rpg.ch1.mira,distance=..40,limit=1] positioned ^ ^ ^17 run summon minecraft:villager ~ ~ ~ {Tags:[\"rpg.ch1.scene\",\"rpg.ch1.actor\",\"rpg.ch1.mira\",\"rpg.ch1.new\",\"rpg.vac.seen\"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:" + row(c("米拉 · 见证人", "#FFF2A8")) + "}",
             "scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id", "tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new",
             "execute positioned ^ ^ ^17 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira,distance=..72,sort=nearest,limit=1] ~ ~ ~"]
    for local, name, _ in roles[:2]: lines.append(f"execute positioned {local} run function rpg:campaign/beelzebub/spawn/minion/{name}")
    write("campaign/beelzebub/stage/3_enter.mcfunction", "\n".join(lines))
    for _, name, role in roles:
        typ = {1: "vindicator", 2: "pillager", 3: "evoker", 4: "illusioner", 5: "vindicator"}[role]
        write(f"campaign/beelzebub/spawn/minion/{name}.mcfunction", "\n".join([
            f"tag @e[type=minecraft:{typ},tag=rpg.demon.minion.lord4,scores={{rpg_mn_role={role}}},distance=..4] add rpg.ch1.preexisting",
            f"function rpg:minion/summon/beelzebub/{name}",
            f"tag @e[type=minecraft:{typ},tag=rpg.demon.minion.lord4,tag=!rpg.ch1.preexisting,scores={{rpg_mn_role={role}}},distance=..4,sort=nearest,limit=1] add rpg.ch1.minion.new",
            "scoreboard players operation @e[tag=rpg.ch1.minion.new,limit=1] rpg_ch1_id = @s rpg_ch1_id",
            "tag @e[tag=rpg.ch1.minion.new,limit=1] add rpg.ch1.minion", "execute if entity @e[tag=rpg.ch1.minion.new,limit=1] run scoreboard players add @s rpg_ch1_obj 1",
            "execute as @e[tag=rpg.ch1.minion.new,limit=1] run function rpg:campaign/beelzebub/minion/scale",
            "tag @e[tag=rpg.ch1.minion.new] remove rpg.ch1.minion.new", "tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting",
        ]))
    scaled = {
        1: {2: 115, 3: 138, 4: 161},
        2: {2: 83, 3: 99, 4: 116},
        3: {2: 95, 3: 114, 4: 133},
        4: {2: 88, 3: 105, 4: 123},
        5: {2: 135, 3: 162, 4: 189},
    }
    scale_lines = ["# Fixed roster score was locked before Stage 3; disconnects never rescale enemies."]
    for role, by_roster in scaled.items():
        for roster, hp in by_roster.items():
            scale_lines += [
                f"execute if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_mn_role matches {role} if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_roster matches {roster} run attribute @s minecraft:max_health base set {hp}",
                f"execute if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_mn_role matches {role} if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_roster matches {roster} run data merge entity @s {{Health:{hp}f}}",
            ]
    write("campaign/beelzebub/minion/scale.mcfunction", "\n".join(scale_lines))
    write("campaign/beelzebub/stage/3_tick.mcfunction", "\n".join([
        "tag @e[tag=rpg.ch1.minion] remove rpg.ch1.minion.current",
        "execute as @e[tag=rpg.ch1.minion] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.minion.current",
        "tag @e[type=minecraft:villager,tag=rpg.ch1.mira] remove rpg.ch1.mira.current",
        "execute as @e[type=minecraft:villager,tag=rpg.ch1.mira] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.mira.current",
        "execute unless entity @s[tag=rpg.ch1.mira.captured] if entity @e[tag=rpg.ch1.minion.current,distance=..40,limit=1] at @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] if entity @e[tag=rpg.ch1.minion.current,distance=..8,limit=1] unless entity @a[tag=rpg.ch1.current,distance=..10,limit=1] run scoreboard players add @s rpg_ch1_guard 1",
        "execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_guard matches 120.. run function rpg:campaign/beelzebub/mira/capture",
        "execute if entity @s[tag=rpg.ch1.mira.captured] run scoreboard players remove @s rpg_ch1_guard 1",
        "execute if entity @s[tag=rpg.ch1.mira.captured] at @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] if entity @a[tag=rpg.ch1.current,distance=..3,limit=1] run scoreboard players add @s rpg_ch1_rescue 1",
        "execute if entity @s[tag=rpg.ch1.mira.captured] at @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] unless entity @a[tag=rpg.ch1.current,distance=..3,limit=1] run scoreboard players set @s rpg_ch1_rescue 0",
        "execute if entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_rescue matches 40.. run function rpg:campaign/beelzebub/mira/rescue_capture",
        "execute if entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_guard matches ..0 run function rpg:campaign/beelzebub/recover_minions",
        "execute if score @s rpg_ch1_sub matches 1 if score @s rpg_ch1_obj matches ..1 if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_minions",
        "execute if score @s rpg_ch1_sub matches 2 if score @s rpg_ch1_obj matches ..3 if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_minions",
        "execute if score @s rpg_ch1_sub matches 3 if score @s rpg_ch1_obj matches ..4 if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_minions",
        "execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 1 if score @s rpg_ch1_obj matches 2.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] run function rpg:campaign/beelzebub/minion/wave2",
        "execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 2 if score @s rpg_ch1_obj matches 4.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] run function rpg:campaign/beelzebub/minion/wave3",
        "execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 3 if score @s rpg_ch1_obj matches 5.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] run function rpg:campaign/beelzebub/advance",
    ]))
    write("campaign/beelzebub/minion/wave2.mcfunction", "\n".join([
        "scoreboard players set @s rpg_ch1_sub 2", "scoreboard players set @s rpg_ch1_time 0",
        "bossbar set rpg:chapter1 name " + row(c("五席未满｜第二轮 · 转运与伪记忆", BEEL, True)),
        "execute positioned ^12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/bathin",
        "execute positioned ^-12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/sallos",
        tell("@a[tag=rpg.ch1.current]", c("虚假的家人：", ASH, True), c("回来吃饭吧。战争已经结束了。", GRAY)),
    ]))
    write("campaign/beelzebub/minion/wave3.mcfunction", "\n".join([
        "scoreboard players set @s rpg_ch1_sub 3", "scoreboard players set @s rpg_ch1_time 0",
        "bossbar set rpg:chapter1 name " + row(c("五席未满｜第三轮 · 处刑者", BEEL, True)),
        "execute positioned ^ ^ ^30 run function rpg:campaign/beelzebub/spawn/minion/purson",
        tell("@a[tag=rpg.ch1.current]", c("布松：", BEEL, True), c("见证不是事实。活下来的见证才是。", GRAY)),
    ]))
    write("campaign/beelzebub/recover_minions.mcfunction", "\n".join([
        "tag @e[tag=rpg.ch1.minion] remove rpg.ch1.minion.current",
        "execute as @e[tag=rpg.ch1.minion] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.minion.current",
        "kill @e[tag=rpg.ch1.minion.current]", "tag @s remove rpg.ch1.mira.captured", "scoreboard players set @s rpg_ch1_empty 0", "scoreboard players add @s rpg_ch1_fail 1",
        tell("@a[tag=rpg.ch1.current]", c("[章节恢复] ", CHAPTER, True), c("罪仆归属未完整建立，重新展开这一波。", GRAY)),
        "scoreboard players set @s rpg_ch1_time 0", "function rpg:campaign/beelzebub/stage/3_enter",
    ]))
    write("campaign/beelzebub/mira/capture.mcfunction", "\n".join([
        "tag @s add rpg.ch1.mira.captured", "scoreboard players set @s rpg_ch1_guard 3600", "scoreboard players set @s rpg_ch1_rescue 0",
        "execute positioned ^ ^ ^35 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] ~ ~ ~",
        tell("@a[tag=rpg.ch1.current]", c("[见证人被捕] ", DANGER, True), c("在 03:00 内靠近米拉 3 格将她带回，否则整组罪仆重置。", GRAY)),
    ]))
    write("campaign/beelzebub/mira/rescue_capture.mcfunction", "\n".join([
        "tag @s remove rpg.ch1.mira.captured", "scoreboard players set @s rpg_ch1_guard 0", "scoreboard players set @s rpg_ch1_rescue 0",
        "execute at @s positioned ^ ^ ^17 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] ~ ~ ~",
        tell("@a[tag=rpg.ch1.current]", c("[见证人救回] ", "#FFF2A8", True), c("米拉重新回到队伍；街区战继续。", GRAY)),
    ]))


def write_tracking_inquest_prep():
    lines = ["bossbar set rpg:chapter1 value 31", "bossbar set rpg:chapter1 name " + row(c("确认活动区域｜追踪四处腐蝇痕迹", BEEL, True))]
    lines += owned_spawn("^ ^ ^12", "trail1", "腐蝇痕迹 1 / 4", BEEL_LIGHT)
    write("campaign/beelzebub/stage/4_enter.mcfunction", "\n".join(lines))
    write("campaign/beelzebub/stage/4_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.trail{n}] at @s run function rpg:campaign/beelzebub/probe/trail{n}" for n in range(1, 5)] + ["execute if score @s rpg_ch1_obj matches 4.. run function rpg:campaign/beelzebub/advance"]))
    trails = ("空口粮袋里没有谷物，只有透明虫翅。", "带血车辙由慈济所通向第七粮仓。", "配给牌只剩姓名，人的部分被吃掉了。", "满仓封条之后没有粮食，只有一排餐盘。")
    for n, text in enumerate(trails, 1):
        extra = [] if n == 4 else [f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/spawn/trail{n + 1}"]
        write_point_probe(f"trail{n}", text, extra)
        if n > 1: write(f"campaign/beelzebub/spawn/trail{n}.mcfunction", "\n".join(owned_spawn(f"^ ^ ^{(12, 20, 28, 36)[n - 1]}", f"trail{n}", f"腐蝇痕迹 {n} / 4", BEEL_LIGHT)))

    # Environment establishes a hypothesis only. Canonical boss-skill hooks award
    # rpg:inquest/clue/4_1..4_5; three different witnessed powers reveal rpg.name.4.
    lines = ["bossbar set rpg:chapter1 value 41", "bossbar set rpg:chapter1 name " + row(c("调查真名与弱点｜建立 3 项环境假说", BEEL, True))]
    for args in (("^-7 ^ ^31", "hyp1", "余烬不是火", ASH), ("^7 ^ ^33", "hyp2", "蝇群生于胃", BEEL_LIGHT), ("^ ^ ^39", "hyp3", "腐败祭品被拒食", BEEL)): lines += owned_spawn(*args)
    write("campaign/beelzebub/stage/5_enter.mcfunction", "\n".join(lines))
    write("campaign/beelzebub/stage/5_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp{n}] at @s run function rpg:campaign/beelzebub/probe/hyp{n}" for n in range(1, 4)] + ["execute if score @s rpg_ch1_obj matches 3.. run function rpg:campaign/beelzebub/advance"]))
    for n, text in enumerate(("焚尸灰保存着牙印：那是吃剩的余餐。", "搏动蝇茧像永远装不满的胃。", "毒马铃薯被整齐推出餐盘：祂拒食自行腐败之物。"), 1):
        write_point_probe(f"hyp{n}", text, [f"tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.done.hyp.{n}"])
        # Compatibility aliases for presentation patches; they do not bypass the
        # canonical three-skill witness requirement.
        write(f"campaign/beelzebub/point/clue{n}.mcfunction", f"function rpg:campaign/beelzebub/point/hyp{n}")

    lines = ["bossbar set rpg:chapter1 value 49", "bossbar set rpg:chapter1 name " + row(c("被撕去的判词｜准备 3 组仪式器具", CHURCH, True))]
    for args in (("^-10 ^ ^35", "cache1", "封印档案箱", CHURCH), ("^10 ^ ^35", "cache2", "圣器保管箱", "#FFF2A8"), ("^ ^ ^42", "cache3", "裁决器具箱", "#62D9E8")): lines += owned_spawn(*args)
    write("campaign/beelzebub/stage/6_enter.mcfunction", "\n".join(lines + [tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("判词从七直接跳到九。缺的是见证人印。", GRAY))]))
    write("campaign/beelzebub/stage/6_tick.mcfunction", "\n".join([f"execute as @e[type=minecraft:marker,tag=rpg.ch1.cache{n}] at @s run function rpg:campaign/beelzebub/probe/cache{n}" for n in range(1, 4)] + ["execute if score @s rpg_ch1_obj matches 3.. run function rpg:campaign/beelzebub/advance"]))
    pending_name = row(c("[待确证残页] ", CHURCH, True), c("万蝇之王 · 缺页判词", BEEL_LIGHT))
    pending_lore = json.dumps([[c("+------------------+", "white")], [c("环境证物只建立了真名假说", GRAY)],
                               [c("必须亲历三种不同权能才能确证", CHURCH)],
                               [c("此页不能投入正式驱魔法阵", DANGER)], [c("+------------------+", "white")]],
                              ensure_ascii=False, separators=(",", ":"))
    write("campaign/beelzebub/give/pending_page.mcfunction",
          f"give @s minecraft:paper[custom_name={pending_name},lore={pending_lore},enchantment_glint_override=true,max_stack_size=1,item_model=\"minecraft:paper\",custom_data={{rpg_ch1_pending_page:1b}}]")
    cache = {1: ["campaign/beelzebub/give/pending_page", "inquest/give/medium4"], 2: ["campaign/beelzebub/give/totem", "inquest/give/strong_water", "inquest/give/nail"], 3: ["inquest/give/bell", "inquest/give/incense", "inquest/give/chalk1", "inquest/give/lantern"]}
    for n, calls in cache.items(): write_point_probe(f"cache{n}", "封存器具已按参与档案分发。", [f"execute as @a[tag=rpg.ch1.current] run function rpg:{fn}" for fn in calls])


def totem_line():
    for line in read("command/give/item.mcfunction").splitlines():
        if line.startswith("give @a totem_of_undying[") and "totem_tag:1b" in line: return line.replace("give @a ", "give @s ", 1)
    raise RuntimeError("canonical exorcism totem missing")


def write_boss_and_rite():
    write("campaign/beelzebub/give/totem.mcfunction", totem_line())
    write("campaign/beelzebub/cache/reissue_missing.mcfunction", "\n".join([
        "execute if entity @s[tag=rpg.ch1.kit.issued] run return 0", "tag @s add rpg.ch1.kit.issued",
        "execute unless items entity @s inventory.* minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] run function rpg:campaign/beelzebub/give/totem",
        "execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_ch1_pending_page:1b}] unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,limit=1] run function rpg:campaign/beelzebub/give/pending_page",
        "execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_medium:4b}] run function rpg:inquest/give/medium4",
        "execute unless items entity @s inventory.* minecraft:lingering_potion[minecraft:custom_data~{rpg_strong_water:1b}] run function rpg:inquest/give/strong_water",
        "execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_nail:1b}] run function rpg:inquest/give/nail",
        "execute unless items entity @s inventory.* minecraft:goat_horn[minecraft:custom_data~{rpg_bell:1b}] run function rpg:inquest/give/bell",
        "execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_incense:1b}] run function rpg:inquest/give/incense",
        "execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_chalk:1b}] run function rpg:inquest/give/chalk1",
        "execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] run function rpg:inquest/give/lantern",
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,limit=1] run function rpg:campaign/beelzebub/witness/confirm_player",
    ]))
    for n in range(1, 6):
        write(f"campaign/beelzebub/witness/skill{n}.mcfunction", "\n".join([
            "tag @s add rpg.ch1.witness.player",
            f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..72,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.witness.player,limit=1] rpg_ch1_id unless entity @s[tag=rpg.ch1.witness.skill.{n}] run function rpg:campaign/beelzebub/witness/record{n}",
            "tag @s remove rpg.ch1.witness.player",
        ]))
        write(f"campaign/beelzebub/witness/record{n}.mcfunction", "\n".join([
            f"tag @s add rpg.ch1.witness.skill.{n}",
            tell("@a[tag=rpg.ch1.current,distance=..72]", c("[权能见证] ", CHURCH, True), c(f"第 {n} 项不同权能已与粮仓证物吻合。", GRAY)),
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
        tell("@a[tag=rpg.ch1.current,distance=..72]", c("[真名确证] ", CHURCH, True), c("三种不可重复的权能已被见证；现实承认别西卜来过。", BEEL_LIGHT)),
    ]))
    write("campaign/beelzebub/witness/confirm_player.mcfunction", "\n".join([
        "clear @s minecraft:paper[minecraft:custom_data~{rpg_ch1_pending_page:1b}]",
        "execute unless entity @s[tag=rpg.name.4] run function rpg:inquest/reveal/4",
        "execute if entity @s[tag=rpg.name.4] unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:4}] run function rpg:inquest/give/page4",
    ]))
    write("campaign/beelzebub/stage/7_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 58", "bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅰ 镇压 · 见证三种权能", BEEL, True)),
        "scoreboard players set @s rpg_ch1_seen 0", "function rpg:campaign/beelzebub/spawn/boss",
        tell("@a[tag=rpg.ch1.current]", c("别西卜：", BEEL, True), c("可你们的账，一直都是平的。欢迎赴宴。", BEEL_LIGHT)),
    ]))
    write("campaign/beelzebub/spawn/boss.mcfunction", "\n".join([
        "execute positioned ^ ^ ^40 run tag @e[type=minecraft:vindicator,tag=rpg.advent,scores={rpg_dm_lord=4},distance=..8] add rpg.ch1.preexisting",
        "execute positioned ^ ^ ^40 run function rpg:taint/lord4",
        "execute positioned ^ ^ ^40 run tag @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.ch1.preexisting,scores={rpg_dm_lord=4},distance=..8,sort=nearest,limit=1] add rpg.ch1.boss.new",
        "scoreboard players operation @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] rpg_ch1_id = @s rpg_ch1_id",
        "tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] add rpg.ch1.boss", "tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new] remove rpg.ch1.boss.new", "tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting",
    ]))
    write("campaign/beelzebub/claim_rite.mcfunction", "\n".join([
        "tag @s add rpg.ch1.rite", "scoreboard players operation @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,sort=nearest,limit=1,distance=..14] rpg_ch1_id",
        tell("@a[tag=rpg.ch1.current,distance=..20]", c("[Ⅱ · 镇魔] ", CHURCH, True), c("真名与点燃图腾已经将祂绑定。", GRAY)),
    ]))
    write("campaign/beelzebub/stage/7_tick.mcfunction", "\n".join([
        "execute as @a[tag=rpg.ch1.current,tag=!rpg.ch1.kit.issued] run function rpg:campaign/beelzebub/cache/reissue_missing",
        "tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss] remove rpg.ch1.boss.current",
        "execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.boss.current",
        "execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.ch1.rite,distance=..64] at @s if entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,distance=..14,limit=1] run function rpg:campaign/beelzebub/claim_rite",
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,scores={rpg_ex_stage=0},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅰ 镇压 · 亲历三种不同权能", BEEL, True)),
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,scores={rpg_ex_stage=1},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅱ 镇魔 · 真名 + 点燃图腾", CHURCH, True)),
        "execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=2},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅲ 固阵 · 稳定度推进至 100", "#62D9E8", True)),
        "execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] run bossbar set rpg:chapter1 name " + row(c("万蝇腐宴｜Ⅳ 裁决 · 四选一", "#D596F2", True)),
        "execute if score @s rpg_ch1_time matches 140 run tellraw @a[tag=rpg.ch1.current] " + row(c("[见证规则] ", CHURCH, True), c("环境证物只是推论；亲历三种不同招式后，现实才承认真名。", GRAY)),
        "execute unless entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,limit=1] if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_boss",
    ]))
    write("campaign/beelzebub/recover_boss.mcfunction", "\n".join([
        "tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss] remove rpg.ch1.boss.current",
        "execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.boss.current",
        "kill @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current]",
        "scoreboard players set @s rpg_ch1_empty 0", "scoreboard players add @s rpg_ch1_fail 1",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup",
        tell("@a[tag=rpg.ch1.current]", c("[仪式恢复] ", CHAPTER, True), c("稳定归零或躯壳异常消散；从 Boss 入口检查点重开，不重置调查。", GRAY)),
        "scoreboard players set @s rpg_ch1_time 0", "function rpg:campaign/beelzebub/stage/7_enter",
    ]))
    write("campaign/beelzebub/rite/collapse.mcfunction", "\n".join([
        "tag @s add rpg.ch1.rite.active",
        "execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_rite_id run kill @s",
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id at @s run function rpg:campaign/beelzebub/recover_boss",
    ]))
    choice = row(c("[消灭]", "#FF6B5E", True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 1"}), c("  [放逐]", "#FFF2A8", True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 2"}), c("  [封印]", "#62D9E8", True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 3"}), c("  [契约]", "#D596F2", True, click_event={"action":"run_command","command":"/trigger rpg_ex_choice set 4"}))
    write("campaign/beelzebub/rite/stage4.mcfunction", "\n".join([
        "scoreboard players remove @s rpg_ex_time 1", "particle minecraft:end_rod ~ ~0.9 ~ 0.9 0.55 0.9 0.05 4 force",
        "execute if score @s rpg_ex_time matches 200 run tellraw @a[tag=rpg.ch1.current,distance=..14] " + choice,
        "execute if score @s rpg_ex_time matches ..0 run scoreboard players set @s rpg_ex_time 300",
        "execute if score @s rpg_ex_time matches 300 run tellraw @a[tag=rpg.ch1.current,distance=..14] " + row(c("[裁决尚待] ", CHURCH, True), c("缺页正在撕扯法阵；必须由见证人主动落笔。", GRAY)),
        "execute if score @s rpg_ex_time matches 300 run tellraw @a[tag=rpg.ch1.current,distance=..14] " + choice,
    ]))


def reward_item(kind, label, color, lore):
    name = row(c("[裁决残响] ", color, True), c(f"别西卜 · {label}", BEEL_LIGHT))
    lore_json = json.dumps([[c("+------------------+", "white")], [c(lore, GRAY)], [c("别西卜逃脱后留下的未完成判词", ASH)], [c("第一章首通纪念 · 非完整领主掉落", DARK)], [c("+------------------+", "white")]], ensure_ascii=False, separators=(",", ":"))
    model = {"eliminate": "nether_star", "banish": "echo_shard", "seal": "soul_lantern", "pact": "written_book"}[kind]
    write(f"campaign/beelzebub/reward/{kind}.mcfunction", f"give @s minecraft:paper[custom_name={name},lore={lore_json},enchantment_glint_override=true,max_stack_size=1,item_model=\"minecraft:{model}\",custom_data={{rpg_ch1_reward:1b,rpg_ch1_{kind}:1b}}]")


def write_verdict_epilogue():
    specs = {"eliminate": (1, "断刃", "#FF6B5E", "刀锋只斩中饕宴的空壳。"), "banish": (2, "逐影", CHURCH, "完整判词放逐了饥饿投下的影子。"), "seal": (3, "空灯", "#62D9E8", "灯芯里没有领主的灵魂。"), "pact": (4, "伪约", "#D596F2", "契约只留下一个胃的签名。")}
    for kind, (choice, label, color, lore) in specs.items():
        write(f"campaign/beelzebub/verdict/{kind}.mcfunction", "\n".join([
            "tag @s add rpg.ch1.rite.active",
            f"execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_choice {choice}",
            "execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_rite_id at @s run function rpg:campaign/beelzebub/escape_boss",
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
        tell("@a[tag=rpg.ch1.current]", c("米拉：", "#FFF2A8", True), c("它们不是忘了最后一页。是故意撕掉的。", GRAY)),
        tell("@a[tag=rpg.ch1.current]", c("伊莱亚：", CHURCH, True), c("若写回所有姓名，教廷篡改粮册的证据也会显现。", GRAY)),
    ])); write("campaign/beelzebub/stage/8_tick.mcfunction", "execute if score @s rpg_ch1_time matches 140.. run function rpg:campaign/beelzebub/advance")
    write("campaign/beelzebub/stage/9_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 94", "bossbar set rpg:chapter1 name " + row(c("活着的人必须有名字｜救下米拉", DANGER, True)),
        "execute positioned ^ ^ ^8 run summon minecraft:villager ~ ~ ~ {Tags:[\"rpg.ch1.scene\",\"rpg.ch1.witness\",\"rpg.ch1.new\",\"rpg.vac.seen\"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:" + row(c("米拉 · 真实见证人", "#FFF2A8")) + "}",
        "scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..20] rpg_ch1_id = @s rpg_ch1_id", "tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new",
        tell("@a[tag=rpg.ch1.current]", c("审判官 塞维拉：", CHURCH, True), c("所有见证人都是污染源。包括她，也包括你。", GRAY)),
    ]))
    rescue_button = "tellraw @a[tag=rpg.ch1.current] " + row(button("释放未经许可的魔力，救下米拉", DANGER, 13, "靠近米拉 12 格；这会让教廷确认你是边缘者"))
    write("campaign/beelzebub/stage/9_tick.mcfunction", "\n".join([
        "execute if score @s rpg_ch1_time matches 40 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", "#FFF2A8", True), c("我叫米拉 · 维恩，今年二十二岁。", GRAY)),
        "execute if score @s rpg_ch1_time matches 85 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", "#FFF2A8", True), c("我在慈济所学配药；薄荷要最后放，否则会苦。", GRAY)),
        "execute if score @s rpg_ch1_time matches 130 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", "#FFF2A8", True), c("伊莱亚欠我两枚铜币，他总说下次会还。", GRAY)),
        "execute if score @s rpg_ch1_time matches 175 run tellraw @a[tag=rpg.ch1.current] " + row(c("米拉：", "#FFF2A8", True), c("我害怕，也想活下去——所以我不是空壳。", GRAY)),
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
        "tag @e[type=minecraft:villager,tag=rpg.ch1.witness] remove rpg.ch1.witness.current",
        "execute as @e[type=minecraft:villager,tag=rpg.ch1.witness,tag=rpg.ch1.scene] if score @s rpg_ch1_id = @a[tag=rpg.ch1.rescue.player,limit=1] rpg_ch1_id run tag @s add rpg.ch1.witness.current",
        "tag @s remove rpg.ch1.rescue.player",
        "execute unless entity @e[type=minecraft:villager,tag=rpg.ch1.witness.current,distance=..12,limit=1] run return run tellraw @s " + row(c("[第一章] 你必须靠近本章节的米拉（12 格内）。", DANGER)),
        "effect give @e[type=minecraft:villager,tag=rpg.ch1.witness.current,limit=1] minecraft:regeneration 8 2 true", "effect give @e[type=minecraft:villager,tag=rpg.ch1.witness.current,limit=1] minecraft:absorption 60 3 true",
        "particle minecraft:totem_of_undying ~ ~1 ~ 1.1 0.8 1.1 0.08 60 force", "scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_obj 1",
        tell("@a[tag=rpg.ch1.current]", c("[第一次释放] ", DANGER, True), c("圣力与魔化在同一道伤口中回应。", GRAY)),
    ]))


def write_completion_cleanup():
    write("campaign/beelzebub/stage/10_enter.mcfunction", "\n".join([
        "bossbar set rpg:chapter1 value 98", "bossbar set rpg:chapter1 name " + row(c("边缘者登记｜选择驱魔道路后完成归档", CHURCH, True)),
        tell("@a[tag=rpg.ch1.current]", c("塞维拉：", CHURCH, True), c("加入边缘者体系，或者作为污染源被处决。", GRAY)),
        "tellraw @a[tag=rpg.ch1.current] " + row(button("打开驱魔师档案并选择道路", "#FFF2A8", 1, "审判、守护或秘仪")),
        "execute as @a[tag=rpg.ch1.current,scores={rpg_ex_path=0}] run function rpg:inquest/career",
        tell("@a[tag=rpg.ch1.current]", c("[归档规则] ", CHAPTER, True), c("至少保留 30 秒选择窗口；未选择道路时章节不会自动结算。", GRAY)),
    ]))
    career_prompt = "tellraw @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] " + row(button("选择或确认驱魔道路", "#FFF2A8", 1, "选择后才会结算首通奖励"))
    write("campaign/beelzebub/stage/10_tick.mcfunction", "\n".join([
        "tag @a remove rpg.ch1.stage10.player",
        "tag @s add rpg.ch1.stage10.controller",
        "execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.stage10.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.stage10.controller,limit=1] rpg_ch1_session run tag @s add rpg.ch1.stage10.player",
        "tag @s remove rpg.ch1.stage10.controller",
        "execute as @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed,scores={rpg_ex_path=1..}] run function rpg:campaign/beelzebub/career_confirm",
        "execute if score @s rpg_ch1_time matches 200 run " + career_prompt,
        "execute if score @s rpg_ch1_time matches 600 run " + career_prompt,
        "execute if score @s rpg_ch1_time matches 1000.. if entity @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] run scoreboard players set @s rpg_ch1_time 600",
        "execute if score @s rpg_ch1_time matches 600.. unless entity @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] run function rpg:campaign/beelzebub/finish",
    ]))
    write("campaign/beelzebub/career_confirm.mcfunction", "\n".join([
        "function rpg:campaign/beelzebub/complete_player",
        "tag @s add rpg.ch1.career.confirmed",
        tell("@s", c("[道路确认] ", CHURCH, True), c("边缘者档案已归档；首通奖励与裁决记录已写入。", GRAY)),
    ]))
    write("campaign/beelzebub/complete_player.mcfunction", "\n".join([
        "scoreboard players operation @s rpg_ch1_verdict = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice",
        "execute if score @s rpg_ch1_reward matches 1.. run return 0", "scoreboard players set @s rpg_ch1_reward 1", "scoreboard players add @s rpg_ex_xp 60",
        "function rpg:campaign/beelzebub/reward/dossier",
        "execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 1 run function rpg:campaign/beelzebub/reward/eliminate",
        "execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 2 run function rpg:campaign/beelzebub/reward/banish",
        "execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 3 run function rpg:campaign/beelzebub/reward/seal",
        "execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 4 run function rpg:campaign/beelzebub/reward/pact",
        "scoreboard players set @s rpg_ch1_done 1", "scoreboard players set @s rpg_ch1_next 1", "tag @s add rpg.ch1.borderer", "function rpg:inquest/career/sync", "function rpg:inquest/career/claim", "advancement grant @s only rpg:campaign/beelzebub",
    ]))
    name = row(c("[教廷档案] ", CHURCH, True), c("边缘者临时入院令", "#FFF2A8")); lore = json.dumps([[c("+------------------+", "white")], [c("编号：VAC-01-BZB", CHAPTER)], [c("罪名：目击空缺者，并擅自释放魔力", GRAY)], [c("处置：编入驱魔院，终身监视", DANGER)], [c("权限：开启高阶恶魔追踪", BEEL_LIGHT)], [c("+------------------+", "white")]], ensure_ascii=False, separators=(",", ":"))
    write("campaign/beelzebub/reward/dossier.mcfunction", f"give @s minecraft:paper[custom_name={name},lore={lore},enchantment_glint_override=true,max_stack_size=1,item_model=\"minecraft:filled_map\",custom_data={{rpg_ch1_dossier:1b}}]")
    cleanup = [
        "tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.cleanup.controller",
        "tag @a remove rpg.ch1.cleanup.player",
        "execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.cleanup.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup.player",
        "tag @e[tag=rpg.ch1.scene,distance=..72] remove rpg.ch1.cleanup", "execute as @e[tag=rpg.ch1.scene,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup",
        "tag @e[tag=rpg.ch1.minion,distance=..72] remove rpg.ch1.cleanup", "execute as @e[tag=rpg.ch1.minion,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup",
        "tag @e[tag=rpg.ch1.boss,distance=..72] remove rpg.ch1.cleanup", "execute as @e[tag=rpg.ch1.boss,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup",
        "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.accepted", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.member", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.party", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.host", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.current", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.kit.issued", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.career.confirmed", "scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_id 0", "scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_session 0", "tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.cleanup.player",
        "bossbar remove rpg:chapter1", "kill @e[tag=rpg.ch1.cleanup,distance=..72]",
    ]
    write("campaign/beelzebub/finish.mcfunction", "\n".join(cleanup))
    write("campaign/beelzebub/abort.mcfunction", "\n".join(["execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return 0", tell("@a[tag=rpg.ch1.current]", c("[第一章] ", CHAPTER, True), c("实例已按章节 ID 安全清理；永久档案不受影响。", GRAY))] + cleanup))


def advancement():
    p = ROOT / "data" / "rpg" / "advancement" / "campaign" / "beelzebub.json"; p.parent.mkdir(parents=True, exist_ok=True)
    payload = {"display": {"icon": {"id": "minecraft:poisonous_potato"}, "title": [{"text": "第一章 · 空缺者", "color": CHAPTER, "bold": True, "italic": False}], "description": [{"text": "别西卜逃脱，而你被教廷登记为边缘者", "color": "gray", "italic": False}], "frame": "challenge", "show_toast": True, "announce_to_chat": True, "hidden": False}, "criteria": {"story": {"trigger": "minecraft:impossible"}}}
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build():
    setup_objectives(); hook_runtime(); hook_panel(); write_menu_and_membership(); write_start_and_controller(); write_preflight()
    write_stage0_2(); write_minions(); write_tracking_inquest_prep(); write_boss_and_rite(); write_verdict_epilogue(); write_completion_cleanup(); advancement()
    print(f"Beelzebub Chapter I generated: {ROOT}")


if __name__ == "__main__": build()
