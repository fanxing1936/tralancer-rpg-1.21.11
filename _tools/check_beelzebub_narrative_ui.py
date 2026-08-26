#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Narrative text release gate for Chapter I.

This checker focuses on regressions that are easy to miss in code review:
JSON rendered as literal text, inherited bold/italic state, unreadably long
screen copy, direct Actionbar writes, and off-palette narrative components.
It deliberately does not inspect gameplay state or timings.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
STRICT_STORY = "--story-contract" in sys.argv[2:]
ROOT = DP / "data" / "rpg" / "function" / "campaign" / "beelzebub"
ERRORS: list[str] = []
CHECKS = 0

ALLOWED_COLORS = {
    "white", "gray", "dark_gray",
    "#FFFFFF", "#B8A98B", "#706B5E", "#D4AF37", "#FFF2A8",
    "#62D9E8", "#D596F2", "#70DB70", "#FF806B", "#8B2500",
    "#5A6B1E", "#596B18", "#B5D957", "#B7C84B", "#E4EA9B",
    "#FFF6C7", "#FF6B5E", "#8FC7FF", "#C9B5FF", "#00491C",
}

COMMANDS = (
    ("tellraw", re.compile(r"(?:^|\srun\s)tellraw\s+\S+\s+(?P<payload>[\[{].*)$")),
    ("title", re.compile(r"(?:^|\srun\s)title\s+\S+\s+title\s+(?P<payload>[\[{].*)$")),
    ("subtitle", re.compile(r"(?:^|\srun\s)title\s+\S+\s+subtitle\s+(?P<payload>[\[{].*)$")),
    ("bossbar", re.compile(r"(?:^|\srun\s)bossbar\s+(?:add\s+\S+|set\s+\S+\s+name)\s+(?P<payload>[\[{].*)$")),
)


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        ERRORS.append(message)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def visible_text(value) -> str:
    return "".join(
        component.get("text", "")
        for component in walk(value)
        if isinstance(component.get("text"), str)
    )


def has_literal_json(text: str) -> bool:
    compact = text.lstrip()
    return (
        compact.startswith("[{") or compact.startswith('{"text"') or
        compact.startswith("[{\\\"text\\\"") or
        compact.startswith('{\\\"text\\\"')
    )


def check_component_tree(kind: str, value, where: str) -> None:
    require(not isinstance(value, str), where + " root component is a JSON string")
    for component in walk(value):
        if "text" not in component:
            continue
        text = component["text"]
        require(isinstance(text, str), where + " has a non-string text field")
        if not isinstance(text, str):
            continue
        require(not has_literal_json(text), where + " embeds JSON as visible text")
        require(component.get("italic") is False,
                where + " lacks explicit italic:false")
        if "color" in component:
            require(component["color"] in ALLOWED_COLORS,
                    where + " uses off-palette color " + str(component["color"]))

    text = visible_text(value)
    limits = {"title": 10, "subtitle": 18, "bossbar": 24}
    if kind in limits:
        require(len(text) <= limits[kind],
                "%s %s is too long (%d > %d): %s" %
                (where, kind, len(text), limits[kind], text))

    components = [c for c in walk(value)
                  if isinstance(c.get("text"), str) and c.get("text")]
    if kind == "tellraw" and len(components) >= 2:
        # A row made entirely of independent clickable choices uses bold on
        # every short button.  It is navigation, not prefix + prose.
        button_row = all("click_event" in component for component in components)
        prefix = components[0].get("text", "")
        is_prefix = (prefix.endswith("：") or
                     (prefix.startswith("[") and "]" in prefix) or
                     prefix.startswith(("目标更新", "◆ ", "◇ ", "→ ")))
        if is_prefix and not button_row:
            require(components[0].get("bold") is True,
                    where + " narrative prefix is not bold")
            for component in components[1:]:
                require(component.get("bold") is False,
                        where + " narrative body inherits bold")


def main() -> None:
    require(ROOT.is_dir(), "chapter function directory missing: " + str(ROOT))
    parsed = 0
    counts = {kind: 0 for kind, _ in COMMANDS}
    rendered: list[str] = []
    if ROOT.is_dir():
        for target in ROOT.rglob("*.mcfunction"):
            relative = target.relative_to(DP).as_posix()
            for number, line in enumerate(target.read_text(encoding="utf-8").splitlines(), 1):
                require(" actionbar " not in (" " + line + " "),
                        "%s:%d directly writes narrative Actionbar" %
                        (relative, number))
                for kind, pattern in COMMANDS:
                    match = pattern.search(line)
                    if not match:
                        continue
                    where = "%s:%d" % (relative, number)
                    try:
                        value = json.loads(match.group("payload"))
                    except json.JSONDecodeError as exc:
                        require(False, "%s invalid %s JSON: %s" % (where, kind, exc))
                        break
                    parsed += 1
                    counts[kind] += 1
                    rendered.append(visible_text(value))
                    check_component_tree(kind, value, where)
                    break

                if "summon minecraft:text_display" in line:
                    where = "%s:%d" % (relative, number)
                    require(re.search(r"\btext\s*:\s*\[", line) is not None,
                            where + " text_display text is not an inline component list")
                    require(re.search(r"\btext\s*:\s*[\"']\s*[\[{]", line) is None,
                            where + " text_display wraps JSON in an SNBT string")

    require(parsed > 0, "no narrative text commands were parsed")
    require(counts["tellraw"] >= 20, "chapter has too little Tellraw narrative")
    require(counts["title"] >= 4, "chapter lacks turning-point titles")
    require(counts["bossbar"] >= 10, "chapter lacks persistent objective labels")

    if STRICT_STORY:
        story = "\n".join(rendered)
        require("第十三声钟" in story,
                "prologue hook '第十三声钟' is absent from runtime UI")
        speaker_minimums = {
            "伊莱亚：": 6,
            "米拉：": 7,
            "卡西安：": 4,
            "塞维拉：": 3,
            "别西卜：": 5,
        }
        for speaker, minimum in speaker_minimums.items():
            actual = story.count(speaker)
            require(actual >= minimum,
                    "%s has too few runtime dialogue beats (%d < %d)" %
                    (speaker[:-1], actual, minimum))
        require(story.count("案情复盘") >= 4,
                "fewer than four investigation recaps are present")
        for label in ("◆ 已知", "◇ 矛盾", "→ 下一步"):
            require(story.count(label) >= 4,
                    "recap label is missing from one or more beats: " + label)
        require("假说" in story and ("已排除" in story or "假说修正" in story),
                "misdirection is not visibly established and corrected")

    if ERRORS:
        print("Beelzebub narrative UI FAILED (%d)" % len(ERRORS))
        for error in ERRORS:
            print("- " + error)
        raise SystemExit(1)
    mode = "story-contract" if STRICT_STORY else "component"
    print("Beelzebub narrative UI OK: %d checks, %d text commands, %s mode" %
          (CHECKS, parsed, mode))
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
