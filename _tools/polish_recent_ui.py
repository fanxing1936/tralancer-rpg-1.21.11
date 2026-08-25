# -*- coding: utf-8 -*-
"""统一近期驱魔、仪式与玩家面板的原生文本 UI。

只处理聊天/标题 JSON，不改玩法、伤害、计时或物品判定。风格基准取自本包
既有物品 Lore：方括号标签、细分隔线、灰色正文、系统色强调，并显式关闭
斜体以避免不同客户端字体回退造成观感漂移。
"""

import io
import json
import os
import re
import sys


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")


def path(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(path(rel), encoding="utf-8") as f:
        return f.read()


def write(rel, content):
    p = path(rel)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.rstrip("\n") + "\n")


def component(value, colour="white", bold=False, click=None):
    out = {"text": value, "color": colour, "italic": False}
    if bold:
        out["bold"] = True
    if click:
        out["click_event"] = {"action": "run_command", "command": click}
    return out


def raw(*parts):
    return json.dumps([""] + list(parts), ensure_ascii=False,
                      separators=(",", ":"))


def verdict_buttons():
    return raw(
        component("[消灭]", "#FF6B5E", True, "/trigger rpg_ex_choice set 1"),
        component("  "),
        component("[放逐]", "#FFF2A8", True, "/trigger rpg_ex_choice set 2"),
        component("  "),
        component("[封印]", "#62D9E8", True, "/trigger rpg_ex_choice set 3"),
        component("  "),
        component("[契约]", "#D596F2", True, "/trigger rpg_ex_choice set 4"),
    )


def polish_verdict():
    rel = "inquest/start_verdict.mcfunction"
    lines = read(rel).splitlines()
    out = []
    replaced = 0
    for line in lines:
        if line.startswith("tellraw @a[") and "rpg_ex_choice set 1" in line:
            out.append("tellraw @a[distance=..14,gamemode=!spectator] " + raw(
                component("[罪约裁决] ", "#FFF2A8", True),
                component("为祂写下离开此世的结局。", "gray")))
            out.append("tellraw @a[distance=..14,gamemode=!spectator] " + verdict_buttons())
            replaced += 1
        else:
            out.append(line)
    if replaced != 1:
        raise RuntimeError("start verdict UI anchor mismatch: %d" % replaced)
    write(rel, "\n".join(out))

    rel = "inquest/anchor_stage4.mcfunction"
    lines = read(rel).splitlines()
    out = []
    replaced = 0
    prefix = "execute if score @s rpg_ex_time matches 200 run "
    for line in lines:
        if line.startswith(prefix + "tellraw ") and "rpg_ex_choice set 1" in line:
            out.append(prefix + "tellraw @a[distance=..14,gamemode=!spectator] " + raw(
                component("[裁决尚待] ", "#FFF2A8", True),
                component("罪约尚未落笔，请选择结局。", "gray")))
            out.append(prefix + "tellraw @a[distance=..14,gamemode=!spectator] " + verdict_buttons())
            replaced += 1
        else:
            out.append(line)
    if replaced != 1:
        raise RuntimeError("verdict reminder UI anchor mismatch: %d" % replaced)
    write(rel, "\n".join(out))


def add_italic_false(value):
    if isinstance(value, list):
        for x in value:
            add_italic_false(x)
    elif isinstance(value, dict):
        if any(k in value for k in ("text", "score", "selector", "keybind", "nbt")):
            value.setdefault("italic", False)
        for x in value.values():
            add_italic_false(x)


PATTERNS = [
    re.compile(r"^(.*\btellraw\s+\S+\s+)([\[{].*)$"),
    re.compile(r"^(.*\btitle\s+\S+\s+(?:title|subtitle|actionbar)\s+)([\[{].*)$"),
    # 反仪式伪名与妒影同样属于近期屏幕呈现；实体名也必须显式非斜体。
    re.compile(r"^(.*\bCustomName\s+set\s+value\s+)([\[{].*)$"),
]


def normalize_line(line):
    for pattern in PATTERNS:
        m = pattern.match(line)
        if not m:
            continue
        try:
            value = json.loads(m.group(2))
        except ValueError:
            return line, False
        add_italic_false(value)
        return m.group(1) + json.dumps(value, ensure_ascii=False,
                                       separators=(",", ":")), True
    return line, False


def normalize_recent_ui():
    changed_files = 0
    changed_lines = 0
    for folder in ("inquest", "rite", "panel"):
        root = path(folder)
        for current, dirs, files in os.walk(root):
            dirs.sort()
            for name in sorted(files):
                if not name.endswith(".mcfunction"):
                    continue
                p = os.path.join(current, name)
                old = io.open(p, encoding="utf-8").read()
                out = []
                touched = 0
                for line in old.splitlines():
                    new, parsed = normalize_line(line)
                    out.append(new)
                    if parsed and new != line:
                        touched += 1
                if touched:
                    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
                        f.write("\n".join(out).rstrip("\n") + "\n")
                    changed_files += 1
                    changed_lines += touched
    return changed_files, changed_lines


def validate():
    for rel in ("inquest/start_verdict.mcfunction",
                "inquest/anchor_stage4.mcfunction"):
        src = read(rel)
        assert "[消灭]" in src and "[放逐]" in src
        assert "[封印]" in src and "[契约]" in src
        assert '"italic":false' in src
    assert "/function rpg:inquest/career" not in read("inquest/career/level_up.mcfunction")
    for rel in ("inquest/counter/start1.mcfunction",
                "inquest/counter/start2.mcfunction"):
        for line in read(rel).splitlines():
            if "CustomName:[" in line:
                assert '"italic":false' in line, (rel, line)

    # 新增驱魔物品保持数据包既有的金色前缀、灰字与非斜体。
    for rel in ("inquest/give/nail.mcfunction", "inquest/give/bell.mcfunction",
                "inquest/give/incense.mcfunction", "inquest/give/lantern.mcfunction",
                "inquest/give/page1.mcfunction", "inquest/give/relic1.mcfunction",
                "inquest/give/core1.mcfunction"):
        src = read(rel)
        assert '"text":"[驱魔]"' in src, rel
        assert '"italic":false' in src, rel


def main():
    polish_verdict()
    files, lines = normalize_recent_ui()
    validate()
    print("recent UI: verdict=2 screens, explicit non-italic=%d lines/%d files, style=PASS" %
          (lines, files))


if __name__ == "__main__":
    main()
