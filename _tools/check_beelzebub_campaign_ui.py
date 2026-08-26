#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Release gate for the non-invasive Chapter I presentation layer."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
RP = Path(sys.argv[2] if len(sys.argv) > 2 else "../resourcepack").resolve()
FUN = DP / "data" / "rpg" / "function"
CAMPAIGN = FUN / "campaign" / "beelzebub"
UI = CAMPAIGN / "ui"
errors: list[str] = []
checks = 0

ALLOWED = {
    "white", "gray", "dark_gray", "#FFFFFF", "#B8A98B", "#706B5E",
    "#D4AF37", "#FFF2A8", "#62D9E8", "#D596F2", "#70DB70",
    "#FF806B", "#8B2500", "#5A6B1E", "#B5D957", "#B7C84B",
    "#E4EA9B", "#FFF6C7", "#FF6B5E", "#8FC7FF", "#C9B5FF",
    # Canonical Lucifer name colour used by the next-case dossier hover.
    "#00491C",
}


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def read(rel: str) -> str:
    target = FUN / rel
    require(target.is_file(), "missing function: " + rel)
    return target.read_text(encoding="utf-8") if target.is_file() else ""


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def parse_text_json() -> int:
    parsed = 0
    for target in CAMPAIGN.rglob("*.mcfunction"):
        for number, line in enumerate(target.read_text(encoding="utf-8").splitlines(), 1):
            if " times " in line and "title " in line:
                continue
            marker = next((token for token in ("tellraw ", " title ",
                                                "bossbar add rpg:chapter1 ",
                                                "bossbar set rpg:chapter1 name ")
                           if token in line), None)
            if not marker:
                continue
            tail = line.split(marker, 1)[1]
            value = None
            for match in re.finditer(r"\[", tail):
                try:
                    value = json.loads(tail[match.start():])
                    break
                except json.JSONDecodeError:
                    pass
            if value is None:
                continue
            parsed += 1
            for component in walk(value):
                if "text" in component:
                    require(component.get("italic") is False,
                            "%s:%d lacks italic:false" %
                            (target.relative_to(FUN), number))
                if "color" in component:
                    require(component["color"] in ALLOWED,
                            "%s:%d off-palette color %s" %
                            (target.relative_to(FUN), number, component["color"]))
    return parsed


def check_item(rel: str, flag: str) -> None:
    body = read(rel).strip()
    require("custom_name=" in body and ",lore=" in body,
            rel + " lacks name/lore")
    if "custom_name=" not in body or ",lore=" not in body:
        return
    try:
        name = json.loads(body.split("custom_name=", 1)[1].split(",lore=", 1)[0])
        lore = json.loads(body.split(",lore=", 1)[1].split(",enchantment_glint_override", 1)[0])
    except json.JSONDecodeError as exc:
        require(False, "%s invalid item JSON: %s" % (rel, exc))
        return
    require(name[1].get("bold") is True, rel + " prefix is not bold")
    require(name[1].get("text", "").startswith("[") and
            name[1].get("text", "").endswith("]"),
            rel + " prefix is not bracketed")
    for component in name[2:]:
        require(component.get("bold") is False,
                rel + " proper name/suffix is bold")
    for component in walk(lore):
        if "text" in component:
            require(component.get("italic") is False,
                    rel + " lore lacks italic:false")
    require(flag in body, rel + " identity flag missing")


def particle_count(line: str) -> int:
    match = re.search(r"\s(\d+)\s+(?:normal|force)$", line)
    return int(match.group(1)) if match else 0


def main() -> None:
    require(UI.is_dir(), "UI function directory missing")
    ui_files = list(UI.rglob("*.mcfunction")) if UI.is_dir() else []
    campaign_files = list(CAMPAIGN.rglob("*.mcfunction")) if CAMPAIGN.is_dir() else []
    ui_text = "\n".join(p.read_text(encoding="utf-8") for p in ui_files)
    campaign_text = "\n".join(p.read_text(encoding="utf-8") for p in campaign_files)

    # Non-invasive contract: stage gameplay ticks are byte-owned by the core
    # generator and never call, embed or get replaced by presentation code.
    for n in range(11):
        stage_tick = read("campaign/beelzebub/stage/%d_tick.mcfunction" % n)
        require("rpg:campaign/beelzebub/ui/" not in stage_tick,
                "UI invades stage %d gameplay tick" % n)
    complete = read("campaign/beelzebub/complete_player.mcfunction")
    require(complete.startswith(
        "scoreboard players operation @s rpg_ch1_verdict = "
        "@e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice\n"
        "execute if score @s rpg_ch1_reward matches 1.. run return 0\n"
        "scoreboard players set @s rpg_ch1_reward 1"),
        "UI changed verdict persistence / reward transaction order")
    for forbidden in ("roster/", "failure_", "minion/scale", "recover_minions",
                      "recover_boss"):
        require(forbidden not in ui_text,
                "UI depends on or mutates frozen core interface: " + forbidden)

    root = read("exorcism.mcfunction")
    hook = ("execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] "
            "run execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] "
            "at @s run function rpg:campaign/beelzebub/ui/tick")
    require(root.count(hook) == 1,
            "presentation hook is missing, duplicated or not controller guarded")
    tick = read("campaign/beelzebub/ui/tick.mcfunction")
    for n in range(11):
        require("rpg_ch1_stage matches %d run function rpg:campaign/beelzebub/ui/stage%d" %
                (n, n) in tick, "UI stage mapping missing: %d" % n)

    # UI may read core objectives; it may only write the upper HUD timer and
    # copy rpg_ch1_id onto a newly spawned display.
    for target in ui_files:
        for line in target.read_text(encoding="utf-8").splitlines():
            if re.search(r"scoreboard players (?:set|add|remove|operation).+ rpg_ch1_(?:stage|sub|time|obj|choice|reward|fail|guard|roster|empty)", line):
                require(False, "%s writes core state: %s" %
                        (target.relative_to(FUN), line))
            if "title @" in line or "tellraw @" in line:
                require("@a[tag=rpg.ch1.member,tag=rpg.ch1.current]" in line and
                        "if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id" in line,
                        "%s player display lacks member+ID isolation" %
                        target.relative_to(FUN))
    require("scoreboard players set @s rpg_hud_dmt 0" in
            read("campaign/beelzebub/ui/stage7.mcfunction"),
            "verdict does not suppress upper demon prompt")
    require("rpg_hud_mt 0" not in ui_text and "rpg_ex_hud_t 0" not in ui_text,
            "UI suppresses lower/status HUD")
    require(not re.findall(r"\btitle\s+[^\n]+\s+actionbar\b", campaign_text),
            "campaign directly writes actionbar")

    # Every physical prop is assigned controller ID immediately; cleanup also
    # compares that ID. Core text labels retain their own generated ID copy.
    scene_files = list((UI / "scene").glob("*.mcfunction")) if (UI / "scene").is_dir() else []
    summon_count = 0
    max_scene_commands = 0
    for target in ui_files:
        body = target.read_text(encoding="utf-8")
        summons = body.count("summon minecraft:item_display") + body.count("summon minecraft:block_display")
        assignments = body.count("scoreboard players operation @e[type=minecraft:item_display,tag=rpg.ch1.ui.new") + body.count("scoreboard players operation @e[type=minecraft:block_display,tag=rpg.ch1.ui.new")
        if summons:
            require(summons == assignments,
                    "%s has %d summons but %d ID assignments" %
                    (target.relative_to(FUN), summons, assignments))
        summon_count += summons
        if target in scene_files:
            max_scene_commands = max(max_scene_commands, summons)
    clear = read("campaign/beelzebub/ui/scene/clear.mcfunction")
    for typ in ("item_display", "block_display"):
        require("type=minecraft:%s" % typ in clear and
                "if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run kill @s" in clear,
                "scene clear is not type+distance+ID scoped for " + typ)
    require(max_scene_commands <= 12,
            "one scene helper emits more than 12 physical displays")
    require(summon_count >= 20,
            "chapter still lacks physical evidence silhouettes")

    for key in ("anom1", "anom2", "anom3", "trail1", "trail2", "trail3",
                "trail4", "hyp1", "hyp2", "hyp3", "cache1", "cache2", "cache3"):
        point = read("campaign/beelzebub/point/%s.mcfunction" % key)
        require("tag=rpg.ch1.%s.prop" % key in point and
                "if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s" in point,
                "point prop cleanup lacks active-point ID: " + key)

    for target in campaign_files:
        body = target.read_text(encoding="utf-8")
        if "summon minecraft:text_display" in body:
            require(body.count("summon minecraft:text_display") <=
                    body.count("scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new"),
                    "%s text display lacks ID inheritance" % target.relative_to(FUN))
            for line_no, line in enumerate(body.splitlines(), 1):
                if "summon minecraft:text_display" not in line:
                    continue
                where = "%s:%d" % (target.relative_to(FUN), line_no)
                require(re.search(r"\btext\s*:\s*\[", line) is not None,
                        where + " text_display is not an inline 1.21.11 component list")
                require(re.search(r"\btext\s*:\s*[\"']\s*[\[{]", line) is None,
                        where + " text_display still wraps JSON/SNBT in a string")
    require("see_through:1b" not in campaign_text,
            "world label leaks through walls")
    ranges = [float(x) for x in re.findall(r"view_range:([0-9.]+)f", campaign_text)]
    require(bool(ranges) and max(ranges) <= 0.30,
            "display view range exceeds local scene budget")

    # UI hierarchy, stage bar semantics and short turning-point titles.
    parsed = parse_text_json()
    required_labels = (
        "发现异常｜痕迹", "辨认空缺者｜以圣器照见异常",
        "罪仆战｜第一轮", "确认活动区域｜痕迹",
        "调查真名与弱点｜假说", "准备仪式｜器具",
        "驱魔·一｜权能见证", "◇ 真名　◇ 图腾",
        "◆ 真名　◇ 图腾", "◇ 真名　◆ 图腾",
        "驱魔·三｜稳定度", "驱魔·四｜选择裁决",
        "裁决落空｜见证人印缺失", "尾声｜救下米拉 · 见证人",
    )
    for label in required_labels:
        require(label in ui_text, "missing actionable UI label: " + label)
    for title in ("第一章", "异常显形", "万蝇腐宴", "真名宣读", "固　阵",
                  "选择裁决", "裁决落空", "第一次释放"):
        require(('"text":"%s"' % title) in ui_text,
                "missing turning-point title: " + title)
    for color in ("green", "yellow", "blue", "purple", "red"):
        require("bossbar set rpg:chapter1 color " + color in ui_text,
                "stage Bossbar never uses " + color)

    for kind in ("eliminate", "banish", "seal", "pact"):
        check_item("campaign/beelzebub/reward/%s.mcfunction" % kind,
                   "rpg_ch1_%s:1b" % kind)
        verdict = read("campaign/beelzebub/verdict/%s.mcfunction" % kind)
        ui_call = "function rpg:campaign/beelzebub/ui/verdict/%s" % kind
        escape_call = "run function rpg:campaign/beelzebub/escape_boss"
        require(ui_call in verdict and verdict.index(ui_call) < verdict.index(escape_call),
                "%s lacks an independent pre-escape presentation entry" % kind)
        route_ui = read("campaign/beelzebub/ui/verdict/%s.mcfunction" % kind)
        require("rpg_ch1_id = @s rpg_ch1_id" in route_ui and
                "@a[tag=rpg.ch1.member,tag=rpg.ch1.current]" in route_ui,
                "%s route presentation lacks display-ID/member isolation" % kind)
    check_item("campaign/beelzebub/reward/dossier.mcfunction",
               "rpg_ch1_dossier:1b")

    # Existing combat font remains the only upper-layer renderer.
    font_path = RP / "assets/rpg/font/combat_prompt.json"
    require(font_path.is_file(), "combat_prompt font missing")
    if font_path.is_file():
        data = json.loads(font_path.read_text(encoding="utf-8"))
        bitmap = next((p for p in data.get("providers", [])
                       if p.get("type") == "bitmap"), {})
        require(bitmap.get("height") == 28 and bitmap.get("ascent") == 27,
                "combat_prompt is not 28/27 clear-size")
    for rel in (
        "assets/rpg/textures/item/pact_beelzebub.png",
        "assets/rpg/models/item/pact_beelzebub.json",
        "assets/rpg/textures/font/combat_prompt.png",
        "assets/rpg/textures/item/exorcism_totem.png",
        "assets/rpg/models/item/chime.json", "assets/rpg/models/item/katana.json",
    ):
        require((RP / rel).is_file(), "canonical reused asset missing: " + rel)

    # Only the scheduled, ID-owned escape marker may add UI particles.
    for target in ui_files:
        if "particle " in target.read_text(encoding="utf-8"):
            require("ui/escape/pulse" in str(target.relative_to(FUN)).replace("\\", "/"),
                    "non-escape UI function adds particles: %s" % target.relative_to(FUN))
    escape_lines = [line for line in read("campaign/beelzebub/escape_boss.mcfunction").splitlines()
                    if line.startswith("particle ")]
    pulse_lines = [line for target in ui_files
                   if target.relative_to(UI).as_posix().startswith("escape/pulse")
                   for line in target.read_text(encoding="utf-8").splitlines()
                   if " run particle " in line]
    escape_particles = (sum(particle_count(line) for line in escape_lines) +
                        sum(particle_count(line) for line in pulse_lines))
    require(escape_particles <= 180,
            "common+sched escape exceeds 180-particle chapter budget")
    require(sum("minecraft:flash" in line for line in escape_lines) <= 1,
            "escape uses more than one flash")
    require("function rpg:campaign/beelzebub/ui/escape/start" in
            read("campaign/beelzebub/escape_boss.mcfunction"),
            "common escape does not start the staged visual tail")
    require(len(pulse_lines) == 3,
            "escape visual tail must contain three timed, ID-owned pulses")

    if errors:
        print("Beelzebub campaign UI FAILED (%d)" % len(errors))
        for error in errors:
            print("- " + error)
        raise SystemExit(1)
    print("Beelzebub campaign UI OK: %d checks, non-invasive, ID-owned, unified HUD" % checks)
    print(json.dumps({
        "escape_particles_total": escape_particles,
        "emitted_prop_commands": summon_count,
        "json_text_commands": parsed,
        "max_scene_prop_commands": max_scene_commands,
        "stages": 11,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
