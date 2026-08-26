#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Non-invasive final UI/art pass for Chapter I.

Run after add_beelzebub_campaign.py. The core generator exclusively owns all
stage gameplay and every stage tick. This pass only installs a separately
controller-guarded presentation hook, appends scene-enter prop hooks, and
normalises display/reward styling. Every player or display remains isolated by
fixed membership plus rpg_ch1_id.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from beelzebub_campaign_config import item_index, load_config


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
RP = Path(sys.argv[2] if len(sys.argv) > 2 else "../resourcepack").resolve()
FUN = DP / "data" / "rpg" / "function"
CONFIG = load_config()
SCENE_POINTS = CONFIG["scene_points"]
ACTORS = CONFIG["actors"]
PALETTE = CONFIG["visual"]["palette"]
RUNTIME = CONFIG["runtime"]
ITEMS = item_index(CONFIG)
BOSS_TYPE = ACTORS["boss"]["entity_type"]

WHITE, GRAY, DARK = PALETTE["white"], "gray", "dark_gray"
CHAPTER, ASH = PALETTE["chapter"], PALETTE["ash"]
CHURCH, HOLY_LIGHT = PALETTE["church"], PALETTE["witness"]
CYAN, RITUAL = PALETTE["seal"], PALETTE["pact"]
DANGER, SEAL_RED = PALETTE["danger_ui"], PALETTE["danger"]
BEEL, BEEL_LIGHT = PALETTE["beelzebub"], PALETTE["beelzebub_light"]
BEEL_COMBAT, BEEL_SOFT, BEEL_GLINT = PALETTE["beelzebub_combat"], PALETTE["beelzebub_soft"], PALETTE["beelzebub_glint"]


def scene_position(group: str, key: str) -> str:
    return SCENE_POINTS[group][key]["spawn"]


def actor_position(group: str, key: str | None = None) -> str:
    actor = ACTORS[group] if key is None else ACTORS[group][key]
    return actor["spawn"]


def fpath(rel: str) -> Path:
    return FUN / rel


def read(rel: str) -> str:
    return fpath(rel).read_text(encoding="utf-8")


def write(rel: str, body: str) -> None:
    target = fpath(rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def comp(value: str, color: str = GRAY, bold: bool = False, **extra):
    result = {"text": value, "color": color, "bold": bool(bold), "italic": False}
    result.update(extra)
    return result


def score(name: str, objective: str, color: str = WHITE):
    return {"score": {"name": name, "objective": objective},
            "color": color, "bold": False, "italic": False}


def row(*parts) -> str:
    return json.dumps([""] + list(parts), ensure_ascii=False,
                      separators=(",", ":"))


def append_once(rel: str, line: str) -> None:
    body = read(rel)
    if line not in body.splitlines():
        body += "\n" + line
    write(rel, body)


def member_run(command: str) -> str:
    """Run a personal display command only for this controller's members."""
    return ("execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] "
            "if score @s rpg_ch1_id = @e[type=minecraft:marker,"
            "tag=rpg.ch1.controller,limit=1] rpg_ch1_id run " + command)


def title_commands(title: str, title_color: str, subtitle: str,
                   subtitle_color: str, times=(15, 55, 20)) -> list[str]:
    return [
        member_run("title @s times %d %d %d" % times),
        member_run("title @s title " + row(comp(title, title_color, True))),
        member_run("title @s subtitle " + row(comp(subtitle, subtitle_color))),
    ]


def install_presentation_hook() -> None:
    hook = ("execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] "
            "run execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] "
            "at @s run function rpg:campaign/beelzebub/ui/tick")
    append_once("exorcism.mcfunction", hook)


def write_ui_runtime() -> None:
    write("campaign/beelzebub/ui/tick.mcfunction", "\n".join(
        "execute if score @s rpg_ch1_stage matches %d run function rpg:campaign/beelzebub/ui/stage%d" % (n, n)
        for n in range(11)))

    static_stages = {
        0: ("yellow", "楔子｜第十三声钟", CHAPTER),
        2: ("yellow", "辨认空缺者｜以圣器照见异常", CHAPTER),
        8: ("red", "裁决落空｜见证人印缺失", DANGER),
        9: ("red", "尾声｜救下米拉 · 见证人", DANGER),
        10: ("yellow", "第一章完成｜登记为教廷边缘者", CHURCH),
    }
    titles = {
        0: ("楔子", CHAPTER, "第十三声钟", ASH),
        2: ("异常显形", CYAN, "她记得姓名，却失去了自己", ASH),
        7: ("万蝇腐宴", BEEL_COMBAT, "别西卜 · 暴食", BEEL_SOFT),
        9: ("最后的见证人", HOLY_LIGHT, "米拉还记得自己的名字", CHAPTER),
        10: ("第一章", CHAPTER, "边缘者", CHURCH),
    }
    for stage, (bar_color, label, text_color) in static_stages.items():
        lines = ["bossbar set rpg:chapter1 color " + bar_color,
                 "bossbar set rpg:chapter1 name " + row(comp(label, text_color, True))]
        if stage in titles:
            lines.append("execute unless entity @s[tag=rpg.ch1.ui.title.%d] run function rpg:campaign/beelzebub/ui/title/stage%d" % (stage, stage))
        write("campaign/beelzebub/ui/stage%d.mcfunction" % stage, "\n".join(lines))

    exploration = {
        1: (3, "发现异常｜痕迹 %d / 3", CHAPTER),
        4: (4, "确认活动区域｜痕迹 %d / 4", BEEL_LIGHT),
        5: (3, "调查真名与弱点｜假说 %d / 3", BEEL_LIGHT),
        6: (3, "准备仪式｜器具 %d / 3", CHURCH),
    }
    for stage, (total, label, color) in exploration.items():
        lines = ["bossbar set rpg:chapter1 color yellow"]
        for done in range(total + 1):
            sub_gate = " if score @s rpg_ch1_sub matches 0" if stage in (4, 5, 6) else ""
            lines.append("execute if score @s rpg_ch1_obj matches %d%s run bossbar set rpg:chapter1 name %s" %
                         (done, sub_gate, row(comp(label % done, color, True))))
        if stage == 4:
            for step in range(4):
                lines.append("execute if score @s rpg_ch1_sub matches 1 if score @s rpg_ch1_choice matches %d run bossbar set rpg:chapter1 name %s" %
                             (step, row(comp("路线密文｜因果 %d / 3" % step, CHAPTER, True))))
            lines.append("execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name " + row(comp("案情复盘｜三线已经闭合", CHAPTER, True)))
        elif stage == 5:
            lines.append("execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name " + row(comp("假说审判｜排除两个伪解", BEEL_LIGHT, True)))
            lines.append("execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name " + row(comp("案情复盘｜保留暴食寄生", CHAPTER, True)))
        elif stage == 6:
            lines.append("execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name " + row(comp("仪式校准｜器具归入三槽", CHURCH, True)))
            lines.append("execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name " + row(comp("入场复盘｜三环已经闭合", CHAPTER, True)))
        write("campaign/beelzebub/ui/stage%d.mcfunction" % stage, "\n".join(lines))

    write("campaign/beelzebub/ui/stage3.mcfunction", "\n".join([
        "execute if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 color yellow",
        "execute if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name " + row(comp("见证人封锁线｜听完简报后迎战", HOLY_LIGHT, True)),
        "execute if score @s rpg_ch1_sub matches 1..3 run bossbar set rpg:chapter1 color green",
        "execute if score @s rpg_ch1_sub matches 12..13 run bossbar set rpg:chapter1 color yellow",
        "execute if score @s rpg_ch1_sub matches 12..13 run bossbar set rpg:chapter1 name " + row(comp("战间复盘｜敌人暂未入场", CHAPTER, True)),
        "execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name " + row(comp("罪仆战｜第一轮 · 封路与追猎", BEEL_COMBAT, True)),
        "execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name " + row(comp("罪仆战｜第二轮 · 转运与伪记忆", BEEL_COMBAT, True)),
        "execute if score @s rpg_ch1_sub matches 3 run bossbar set rpg:chapter1 name " + row(comp("罪仆战｜第三轮 · 处刑者", BEEL_COMBAT, True)),
        "execute if entity @s[tag=rpg.ch1.mira.captured] run bossbar set rpg:chapter1 color red",
        "execute if entity @s[tag=rpg.ch1.mira.captured] run bossbar set rpg:chapter1 name " + row(comp("⚠ 救回米拉｜倒计时仍在推进", DANGER, True)),
    ]))

    battle = [
        "execute if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 color yellow",
        "execute if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name " + row(comp("粮仓门内｜别西卜尚未现身", CHAPTER, True)),
        "execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 color green",
        f"execute as @e[type={BOSS_TYPE},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=0}},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run bossbar set rpg:chapter1 name " + row(comp("驱魔·一｜权能见证 ", BEEL_COMBAT, True), score("@e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1]", "rpg_ch1_seen", BEEL_GLINT), comp(" / 3", DARK)),
        f"execute as @e[type={BOSS_TYPE},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=1}},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run bossbar set rpg:chapter1 color yellow",
        f"execute as @e[type={BOSS_TYPE},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=1}},limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id unless entity @a[tag=rpg.ch1.member,tag=rpg.ch1.current,tag=rpg.name.4,distance=..10,gamemode=!spectator] unless entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.rite.anchor,distance=..8,limit=1] run bossbar set rpg:chapter1 name " + row(comp("驱魔·二｜◇ 真名　◇ 图腾", CHURCH, True)),
        f"execute as @e[type={BOSS_TYPE},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=1}},limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if entity @a[tag=rpg.ch1.member,tag=rpg.ch1.current,tag=rpg.name.4,distance=..10,gamemode=!spectator] unless entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.rite.anchor,distance=..8,limit=1] run bossbar set rpg:chapter1 name " + row(comp("驱魔·二｜◆ 真名　◇ 图腾", CHURCH, True)),
        f"execute as @e[type={BOSS_TYPE},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=1}},limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id unless entity @a[tag=rpg.ch1.member,tag=rpg.ch1.current,tag=rpg.name.4,distance=..10,gamemode=!spectator] if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.rite.anchor,distance=..8,limit=1] run bossbar set rpg:chapter1 name " + row(comp("驱魔·二｜◇ 真名　◆ 图腾", CHURCH, True)),
        f"execute as @e[type={BOSS_TYPE},tag=rpg.ch1.boss.current,scores={{rpg_ex_stage=1}},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.ui.phase2,limit=1] run function rpg:campaign/beelzebub/ui/title/phase2",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=2},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run bossbar set rpg:chapter1 color blue",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=2},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run bossbar set rpg:chapter1 name " + row(comp("驱魔·三｜稳定度 ", CYAN, True), score("@s", "rpg_ex_stab", CYAN), comp(" / 100", DARK)),
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=2},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.ui.phase3,limit=1] run function rpg:campaign/beelzebub/ui/title/phase3",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run bossbar set rpg:chapter1 color purple",
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run bossbar set rpg:chapter1 name " + row(comp("驱魔·四｜选择裁决", RITUAL, True)),
        "execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.ui.phase4,limit=1] run function rpg:campaign/beelzebub/ui/title/phase4",
        "execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run scoreboard players set @s rpg_hud_dmt 0",
        "execute if score @s rpg_ch1_sub matches 1 unless entity @s[tag=rpg.ch1.ui.title.7] run function rpg:campaign/beelzebub/ui/title/stage7",
    ]
    write("campaign/beelzebub/ui/stage7.mcfunction", "\n".join(battle))

    for stage, args in titles.items():
        t, tc, s, sc = args
        write("campaign/beelzebub/ui/title/stage%d.mcfunction" % stage, "\n".join([
            "tag @s add rpg.ch1.ui.title.%d" % stage,
            *title_commands(t, tc, s, sc, (5, 35, 15) if stage == 7 else (15, 55, 20)),
        ]))
    for phase, title, tc, subtitle, sc in (
        (2, "真名宣读", CYAN, "让现实记住祂确实来过", HOLY_LIGHT),
        (3, "固　阵", CYAN, "让被吞去的名字回来", BEEL_SOFT),
        (4, "选择裁决", RITUAL, "四条判词都将留下代价", CHAPTER),
    ):
        write("campaign/beelzebub/ui/title/phase%d.mcfunction" % phase,
              "\n".join([
                  "tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.ui.phase%d" % phase,
                  *title_commands(title, tc, subtitle, sc, (5, 25, 10)),
              ]))

    stage8 = read("campaign/beelzebub/ui/stage8.mcfunction").splitlines()
    stage8 += [
        "execute if score @s rpg_ch1_time matches 12.. unless entity @s[tag=rpg.ch1.ui.title.8] run function rpg:campaign/beelzebub/ui/title/stage8",
        "execute unless entity @s[tag=rpg.ch1.ui.scene.8] run function rpg:campaign/beelzebub/ui/scene/stage8",
    ]
    write("campaign/beelzebub/ui/stage8.mcfunction", "\n".join(stage8))
    write("campaign/beelzebub/ui/title/stage8.mcfunction", "\n".join([
        "tag @s add rpg.ch1.ui.title.8",
        "execute if score @s rpg_ch1_choice matches 1 run function rpg:campaign/beelzebub/ui/title/verdict_eliminate",
        "execute if score @s rpg_ch1_choice matches 2 run function rpg:campaign/beelzebub/ui/title/verdict_banish",
        "execute if score @s rpg_ch1_choice matches 3 run function rpg:campaign/beelzebub/ui/title/verdict_seal",
        "execute if score @s rpg_ch1_choice matches 4 run function rpg:campaign/beelzebub/ui/title/verdict_pact",
    ]))
    for kind, color in (("eliminate", PALETTE["eliminate"]), ("banish", CHURCH),
                        ("seal", CYAN), ("pact", RITUAL)):
        write("campaign/beelzebub/ui/title/verdict_%s.mcfunction" % kind,
              "\n".join(title_commands("裁决落空", color, "别西卜已离席", ASH)))
    write("campaign/beelzebub/ui/title/rescue.mcfunction",
          "\n".join(title_commands("第一次释放", HOLY_LIGHT,
                                    "让一个人继续拥有自己的名字", CHAPTER)))

    # Four route-specific, presentation-only entries run from the ID-owned rite
    # immediately before the unchanged common escape.  The common result title
    # waits 12 ticks, so these route signatures remain readable.
    verdict_ui = {
        "eliminate": ("判词 · 消灭", PALETTE["eliminate"], "断刃斩入饕宴空壳",
                      "iron_sword", "minecraft:block.anvil.land", "1.25"),
        "banish": ("判词 · 放逐", CHURCH, "金环送走饥饿之影",
                    "echo_shard", "minecraft:entity.enderman.teleport", "0.82"),
        "seal": ("判词 · 封印", CYAN, "空灯收下卡西安回声",
                  "soul_lantern", "minecraft:block.respawn_anchor.set_spawn", "1.35"),
        "pact": ("判词 · 契约", RITUAL, "胃之印冒充领主签名",
                  "writable_book", "minecraft:item.book.page_turn", "0.68"),
    }
    for kind, (title, color, subtitle, item, sound, pitch) in verdict_ui.items():
        write("campaign/beelzebub/ui/verdict/%s.mcfunction" % kind, "\n".join([
            *title_commands(title, color, subtitle, BEEL_SOFT, (5, 18, 8)),
            member_run("playsound %s master @s ~ ~ ~ 0.70 %s" % (sound, pitch)),
            item_display("verdict", item, scale=.62),
            "scoreboard players operation @e[type=minecraft:item_display,tag=rpg.ch1.ui.new,sort=nearest,limit=1,distance=..3] rpg_ch1_id = @s rpg_ch1_id",
            "tag @e[type=minecraft:item_display,tag=rpg.ch1.ui.new,sort=nearest,limit=1,distance=..3] remove rpg.ch1.ui.new",
        ]))
        rel = "campaign/beelzebub/verdict/%s.mcfunction" % kind
        body = read(rel)
        call = "function rpg:campaign/beelzebub/ui/verdict/%s" % kind
        if call not in body:
            anchor = next((line for line in body.splitlines()
                           if "run function rpg:campaign/beelzebub/escape_boss" in line), "")
            if not anchor:
                raise RuntimeError("common escape anchor missing: " + rel)
            write(rel, body.replace(anchor, call + "\n" + anchor, 1))

    write("campaign/beelzebub/ui/escape/start.mcfunction", "\n".join([
        "summon minecraft:marker ~ ~1 ~ {Tags:[\"rpg.ch1.scene\",\"rpg.ch1.ui.escape\",\"rpg.ch1.ui.escape.new\"]}",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.ui.escape.new,sort=nearest,limit=1,distance=..3] rpg_ch1_id = @s rpg_ch1_id",
        "tag @e[type=minecraft:marker,tag=rpg.ch1.ui.escape.new,sort=nearest,limit=1,distance=..3] remove rpg.ch1.ui.escape.new",
        "schedule function rpg:campaign/beelzebub/ui/escape/pulse1 2t replace",
    ]))
    write("campaign/beelzebub/ui/escape/pulse1.mcfunction", "\n".join([
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.ui.escape,limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run particle minecraft:ash ~ ~ ~ 0.9 0.4 0.9 0.03 12 normal",
        "schedule function rpg:campaign/beelzebub/ui/escape/pulse2 2t replace",
    ]))
    write("campaign/beelzebub/ui/escape/pulse2.mcfunction", "\n".join([
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.ui.escape,limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run particle minecraft:spore_blossom_air ~ ~ ~ 1.2 0.5 1.2 0.04 16 normal",
        "schedule function rpg:campaign/beelzebub/ui/escape/pulse3 2t replace",
    ]))
    write("campaign/beelzebub/ui/escape/pulse3.mcfunction", "\n".join([
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.ui.escape,limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run particle minecraft:large_smoke ~ ~ ~ 1.1 0.45 1.1 0.03 16 normal",
        "execute as @e[type=minecraft:marker,tag=rpg.ch1.ui.escape,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run kill @s",
    ]))
    escape_rel = "campaign/beelzebub/escape_boss.mcfunction"
    escape = read(escape_rel)
    escape_call = "function rpg:campaign/beelzebub/ui/escape/start"
    if escape_call not in escape:
        if "kill @s" not in escape:
            raise RuntimeError("escape kill anchor missing")
        write(escape_rel, escape.replace("kill @s", escape_call + "\nkill @s", 1))


def item_display(key: str, item: str, dx=0.0, dy=0.12, dz=0.0,
                 scale=0.52) -> str:
    return ("summon minecraft:item_display ~%.2f ~%.2f ~%.2f "
            "{Tags:[\"rpg.ch1.scene\",\"rpg.ch1.ui.prop\","
            "\"rpg.ch1.%s.prop\",\"rpg.ch1.ui.new\"],"
            "item:{id:\"minecraft:%s\",count:1},item_display:\"fixed\","
            "view_range:0.30f,shadow_radius:0.18f,shadow_strength:0.55f,"
            "transformation:{translation:[0f,0f,0f],scale:[%.2ff,%.2ff,%.2ff],"
            "left_rotation:[0f,0f,0.0872f,0.9962f],right_rotation:[0f,0f,0f,1f]}}") % (
                dx, dy, dz, key, item, scale, scale, scale)


def block_display(key: str, block: str, scale=0.78) -> str:
    return ("summon minecraft:block_display ~ ~ ~ "
            "{Tags:[\"rpg.ch1.scene\",\"rpg.ch1.ui.prop\","
            "\"rpg.ch1.%s.prop\",\"rpg.ch1.ui.new\"],"
            "block_state:{Name:\"minecraft:%s\"},view_range:0.30f,"
            "shadow_radius:0.25f,shadow_strength:0.65f,"
            "transformation:{translation:[-0.39f,0f,-0.39f],"
            "scale:[%.2ff,%.2ff,%.2ff],left_rotation:[0f,0f,0f,1f],"
            "right_rotation:[0f,0f,0f,1f]}}") % (key, block, scale, scale, scale)


def _snbt_quote(value: str) -> str:
    """Quote a string for an inline 1.21.5+ SNBT text component."""
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def _component_snbt(value) -> str:
    """Serialize the JSON text-component subset used by scene labels."""
    if isinstance(value, str):
        return _snbt_quote(value)
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        return "[" + ",".join(_component_snbt(item) for item in value) + "]"
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            snbt_key = key if re.fullmatch(r"[A-Za-z0-9_.+-]+", key) else _snbt_quote(key)
            parts.append(snbt_key + ":" + _component_snbt(item))
        return "{" + ",".join(parts) + "}"
    raise TypeError("unsupported text component value: %r" % (value,))


_WRAPPED_TEXT_COMPONENT = re.compile(
    r'(?P<prefix>\btext\s*:\s*)"(?P<payload>(?:\\.|[^"\\])*)"')


def _inline_text_display_component(line: str) -> str:
    """Migrate JSON-in-a-string text_display NBT to inline component SNBT."""
    if "summon minecraft:text_display" not in line:
        return line

    def replace(match: re.Match) -> str:
        # Decode the outer SNBT double-quoted string, then its JSON payload.
        wrapped = '"' + match.group("payload") + '"'
        try:
            payload = json.loads(wrapped)
        except json.JSONDecodeError as exc:
            raise RuntimeError("invalid wrapped text_display string: %s" % line) from exc
        if not payload.lstrip().startswith(("[", "{")):
            return match.group(0)
        try:
            component = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError("invalid wrapped text_display component: %s" % line) from exc
        return match.group("prefix") + _component_snbt(component)

    return _WRAPPED_TEXT_COMPONENT.sub(replace, line, count=1)


def owned_prop(local: str, command: str, entity_type: str) -> list[str]:
    return [
        "execute positioned %s run %s" % (local, command),
        "scoreboard players operation @e[type=minecraft:%s,tag=rpg.ch1.ui.new,sort=nearest,limit=1,distance=..%s] rpg_ch1_id = @s rpg_ch1_id" % (entity_type, RUNTIME["scene_radius"]),
        "tag @e[type=minecraft:%s,tag=rpg.ch1.ui.new,sort=nearest,limit=1,distance=..%s] remove rpg.ch1.ui.new" % (entity_type, RUNTIME["scene_radius"]),
    ]


def write_scene_props() -> None:
    write("campaign/beelzebub/ui/scene/clear.mcfunction", "\n".join([
        f"tag @e[type=minecraft:item_display,tag=rpg.ch1.ui.prop,distance=..{RUNTIME['scene_radius']}] remove rpg.ch1.ui.current",
        f"execute as @e[type=minecraft:item_display,tag=rpg.ch1.ui.prop,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.ui.current",
        f"execute as @e[type=minecraft:item_display,tag=rpg.ch1.ui.current,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run kill @s",
        f"tag @e[type=minecraft:block_display,tag=rpg.ch1.ui.prop,distance=..{RUNTIME['scene_radius']}] remove rpg.ch1.ui.current",
        f"execute as @e[type=minecraft:block_display,tag=rpg.ch1.ui.prop,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.ui.current",
        f"execute as @e[type=minecraft:block_display,tag=rpg.ch1.ui.current,distance=..{RUNTIME['scene_radius']}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run kill @s",
    ]))

    stage1 = ["function rpg:campaign/beelzebub/ui/scene/clear"]
    stage1 += owned_prop(scene_position("anomaly", "anom1"), item_display("anom1", "bowl"), "item_display")
    stage1 += owned_prop(scene_position("anomaly", "anom1"), item_display("anom1", "bread", .34, .11, .08, .40), "item_display")
    stage1 += owned_prop(scene_position("anomaly", "anom2"), item_display("anom2", "paper", scale=.70), "item_display")
    stage1 += owned_prop(scene_position("anomaly", "anom3"), item_display("anom3", "gunpowder"), "item_display")
    stage1 += owned_prop(scene_position("anomaly", "anom3"), item_display("anom3", "phantom_membrane", .28, .10, .03, .34), "item_display")
    write("campaign/beelzebub/ui/scene/stage1.mcfunction", "\n".join(stage1))

    trail_items = {1: "wheat_seeds", 2: "gray_dye", 3: "name_tag", 4: "bowl"}
    trail_pos = {n: scene_position("trail", "trail%d" % n) for n in range(1, 5)}
    for n in range(1, 5):
        lines = ["function rpg:campaign/beelzebub/ui/scene/clear"] if n == 1 else []
        lines += owned_prop(trail_pos[n], item_display("trail%d" % n,
                                                       trail_items[n], scale=.38),
                            "item_display")
        write("campaign/beelzebub/ui/scene/trail%d.mcfunction" % n, "\n".join(lines))

    stage5 = ["function rpg:campaign/beelzebub/ui/scene/clear"]
    for local, key, items in (
        (scene_position("hypothesis", "hyp1"), "hyp1", ("gunpowder", "paper")),
        (scene_position("hypothesis", "hyp2"), "hyp2", ("slime_ball", "phantom_membrane")),
        (scene_position("hypothesis", "hyp3"), "hyp3", ("poisonous_potato",)),
    ):
        for index, item in enumerate(items):
            stage5 += owned_prop(local, item_display(key, item, .27 * index,
                                                      .12 - .03 * index, 0,
                                                      .52 if index == 0 else .36),
                                 "item_display")
    write("campaign/beelzebub/ui/scene/stage5.mcfunction", "\n".join(stage5))

    stage6 = ["function rpg:campaign/beelzebub/ui/scene/clear"]
    for local, key, item in ((scene_position("cache", "cache1"), "cache1", "paper"),
                             (scene_position("cache", "cache2"), "cache2", "totem_of_undying"),
                             (scene_position("cache", "cache3"), "cache3", "bell")):
        stage6 += owned_prop(local, block_display(key, "barrel"), "block_display")
        stage6 += owned_prop(local, item_display(key, item, 0, .90, 0, .34), "item_display")
    write("campaign/beelzebub/ui/scene/stage6.mcfunction", "\n".join(stage6))

    stage8 = ["tag @s add rpg.ch1.ui.scene.8",
              "function rpg:campaign/beelzebub/ui/scene/clear"]
    for choice, item in {1: "iron_sword", 2: "echo_shard", 3: "soul_lantern", 4: "writable_book"}.items():
        stage8 += ["execute if score @s rpg_ch1_choice matches %d run %s" %
                   (choice, line) for line in owned_prop(
                       actor_position("boss"), item_display("verdict", item, scale=.62), "item_display")]
    write("campaign/beelzebub/ui/scene/stage8.mcfunction", "\n".join(stage8))

    hooks = {
        "campaign/beelzebub/stage/1_enter.mcfunction": "function rpg:campaign/beelzebub/ui/scene/stage1",
        "campaign/beelzebub/stage/4_enter.mcfunction": "function rpg:campaign/beelzebub/ui/scene/trail1",
        "campaign/beelzebub/stage/5_enter.mcfunction": "function rpg:campaign/beelzebub/ui/scene/stage5",
        "campaign/beelzebub/stage/6_enter.mcfunction": "function rpg:campaign/beelzebub/ui/scene/stage6",
        "campaign/beelzebub/stage/9_enter.mcfunction": "function rpg:campaign/beelzebub/ui/scene/clear",
    }
    for rel, hook in hooks.items():
        append_once(rel, hook)
    for n in range(2, 5):
        append_once("campaign/beelzebub/spawn/trail%d.mcfunction" % n,
                    "function rpg:campaign/beelzebub/ui/scene/trail%d" % n)

    keys = ("anom1", "anom2", "anom3", "trail1", "trail2", "trail3", "trail4",
            "hyp1", "hyp2", "hyp3", "cache1", "cache2", "cache3")
    for key in keys:
        rel = "campaign/beelzebub/point/%s.mcfunction" % key
        body = read(rel)
        cleanup = ("execute as @e[type=minecraft:item_display,tag=rpg.ch1.%s.prop,"
                   "distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,"
                   "limit=1] rpg_ch1_id run kill @s") % key
        if cleanup not in body:
            anchor = "kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]"
            if anchor not in body:
                raise RuntimeError("point cleanup anchor missing: " + rel)
            write(rel, body.replace(anchor, cleanup + "\n" + anchor, 1))


def normalise_existing_displays() -> None:
    for target in fpath("campaign/beelzebub").rglob("*.mcfunction"):
        body = target.read_text(encoding="utf-8")
        body = body.replace("see_through:1b", "see_through:0b")
        body = re.sub(r"view_range:[0-9.]+f", f"view_range:{CONFIG['visual']['label_view_range']}f", body)
        lines = []
        for line in body.splitlines():
            if "summon minecraft:text_display" in line:
                line = line.replace(f'\\"color\\":\\"{BEEL}\\"',
                                    f'\\"color\\":\\"{BEEL_LIGHT}\\"')
                line = line.replace(f'color:"{BEEL}"', f'color:"{BEEL_LIGHT}"')
                line = line.replace(f"color:'{BEEL}'", f"color:'{BEEL_LIGHT}'")
                line = _inline_text_display_component(line)
            lines.append(line)
        target.write_text("\n".join(lines).rstrip("\n") + "\n",
                          encoding="utf-8", newline="\n")


def reward_name(prefix: str, prefix_color: str, proper: str,
                proper_color: str) -> str:
    return row(comp(prefix, prefix_color, True), comp(proper, proper_color))


def lore_value(lines: list[tuple[str, str]]) -> str:
    rows = [[comp("+------------------+", WHITE)]]
    rows += [[comp(value, color)] for value, color in lines]
    rows += [[comp("+------------------+", WHITE)]]
    return json.dumps(rows, ensure_ascii=False, separators=(",", ":"))


def generated_rel(item: dict) -> str:
    namespace, rel = item["give_function"].split(":", 1)
    if namespace != "rpg":
        raise RuntimeError("Chapter I generated item functions must use the rpg namespace")
    return rel + ".mcfunction"


def custom_data_value(item: dict) -> str:
    prefix = "minecraft:custom_data~"
    if not item["match"].startswith(prefix):
        raise RuntimeError("Chapter I generated items require a custom-data match")
    return item["match"][len(prefix):]


def polish_items_and_true_name() -> None:
    verdicts = {
        "eliminate": ("断刃", PALETTE["eliminate"],
                      [("你选择了消灭。", GRAY), ("刀锋只斩中腐宴空壳", ASH)]),
        "banish": ("逐影", CHURCH,
                    [("你选择了放逐。", GRAY), ("归去的只是饥饿之影", ASH)]),
        "seal": ("空灯", CYAN,
                  [("你选择了封印。", GRAY), ("灯芯未收下领主灵魂", ASH)]),
        "pact": ("伪约", RITUAL,
                  [("你选择了契约。", GRAY), ("胃之印冒充领主签名", ASH)]),
    }
    for kind, (label, color, specific) in verdicts.items():
        item = ITEMS[f"{kind}_resonance"]
        name = reward_name("[裁决残响]", color, "别西卜 · " + label, BEEL_LIGHT)
        lore = lore_value(specific + [
            ("裁决未完成 · 领主逃脱", BEEL_LIGHT),
            ("第一章首通纪念", CHAPTER), ("非完整领主掉落", DARK)])
        write(generated_rel(item),
              "give @s %s[custom_name=%s,lore=%s,"
              "enchantment_glint_override=true,max_stack_size=1,"
              "item_model=\"%s\",custom_data=%s]" %
              (item["base_item"], name, lore, item["item_model"], custom_data_value(item)))

    dossier = reward_name("[教廷档案]", CHURCH,
                          "边缘者临时入院令", HOLY_LIGHT)
    dossier_lore = lore_value([
        ("编号 · VAC-01-BZB", CHAPTER), ("对象 · 未许可施术者", GRAY),
        ("事由 · 救援真实见证人", GRAY), ("处置 · 编入驱魔院", SEAL_RED),
        ("状态 · 终身监视", SEAL_RED), ("权限 · 高阶预调查", BEEL_LIGHT)])
    dossier_item = ITEMS["borderer_dossier"]
    write(generated_rel(dossier_item),
          "give @s %s[custom_name=%s,lore=%s,"
          "enchantment_glint_override=true,max_stack_size=1,"
          "item_model=\"%s\",custom_data=%s]" %
          (dossier_item["base_item"], dossier, dossier_lore,
           dossier_item["item_model"], custom_data_value(dossier_item)))

    write("inquest/reveal/4.mcfunction", "\n".join([
        "tag @s add rpg.name.4", "scoreboard players set @s rpg_case4 3",
        "title @s times 15 55 20",
        "title @s title " + row(comp("真名确证", CYAN, True)),
        "title @s subtitle " + row(comp("别西卜 · 暴食", BEEL)),
        "tellraw @s " + row(comp("[真名确证] ", CYAN, True),
                             comp("别西卜 · 暴食", BEEL), comp("　弱点：", GRAY),
                             comp("腐败的宴席", HOLY_LIGHT)),
        "tellraw @s " + row(comp("◆ ", CYAN),
                             comp("暴食无法吞下已经腐败的宴席。", GRAY)),
        "playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35",
        "scoreboard players add @s rpg_ex_xp 8", f"function {ITEMS['confirmed_name_page']['give_function']}",
    ]))
    for n in range(1, 6):
        rel = "inquest/clue/4_%d.mcfunction" % n
        if fpath(rel).is_file():
            body = read(rel)
            body = re.sub(rf'("text":"别西卜 · ","color":"{re.escape(BEEL)}",)"bold":true,',
                          r'\1"bold":false,', body)
            write(rel, body)

    rescue_hook = ("execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] "
                   "if score @s rpg_ch1_id = @a[tag=rpg.ch1.member,"
                   "tag=rpg.ch1.current,sort=nearest,limit=1] rpg_ch1_id at @s "
                   "run function rpg:campaign/beelzebub/ui/title/rescue")
    append_once("campaign/beelzebub/rescue.mcfunction", rescue_hook)


def require_assets() -> None:
    required = (
        "assets/rpg/textures/item/pact_beelzebub.png",
        "assets/rpg/models/item/pact_beelzebub.json",
        "assets/rpg/textures/font/combat_prompt.png",
        "assets/rpg/font/combat_prompt.json",
        "assets/rpg/textures/item/exorcism_totem.png",
        "assets/rpg/models/item/chime.json", "assets/rpg/models/item/katana.json",
    )
    missing = [rel for rel in required if not (RP / rel).is_file()]
    if missing:
        raise RuntimeError("canonical reused assets missing: " + ", ".join(missing))


def main() -> None:
    if not fpath("campaign/beelzebub/stage/10_tick.mcfunction").is_file():
        raise SystemExit("final 0..10 campaign must be generated before UI polish")
    require_assets()
    install_presentation_hook()
    write_ui_runtime()
    write_scene_props()
    normalise_existing_displays()
    polish_items_and_true_name()
    print("Beelzebub campaign UI: non-invasive 0..10 / ID-owned displays / unified HUD PASS")


if __name__ == "__main__":
    main()
