# -*- coding: utf-8 -*-
"""把玩家面板从聊天栏换成对话框界面，和契约界面同一种样式。

面板的内容散在五个生成器里，最后还要过 polish_ui，所以这里排在最后，直接转换
写好的 tellraw：正文进 ui.body，带点击的按钮进 ui.actions，页头进 ui.title，
分数变成宏参数。这样以后谁往面板里加一行 tellraw，都不用改这个文件。

按钮命令不变，仍是 /trigger rpg_panel set N，普通玩家可用。

切到面板时不再立刻弹出：对话框会占住键盘，滚轮划过这一格不能打断操作，
所以要在这一格停够 OPEN_DELAY 刻才打开。
"""

import io
import json
import os
import re
import sys

import rpg_ui_style as ui

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
PAGES = ["panel/open", "panel/inquest", "panel/pact", "panel/help", "inquest/career"]
# 页头的哥特小注（ART-STYLE.md §12）。
GLOSS = {"panel/open": "Dossier", "panel/inquest": "True Names", "panel/pact": "Covenant",
         "panel/help": "Handbook", "inquest/career": "Exorcist"}
OPEN_DELAY = 12
TELLRAW = re.compile(r"^(execute .* run )?tellraw @s (\[.*\])\s*$")
HEADER = re.compile(r"^\+[-\s]*(.*?)[-\s]*\+$")
STORE = "storage rpg:panel"


def path_of(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep) + ".mcfunction")


def read(rel):
    with io.open(path_of(rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, lines):
    target = path_of(rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip("\n") + "\n")


def dump(value):
    return json.dumps(ui.darken(value), ensure_ascii=False, separators=(",", ":"))


def plain(comp):
    return comp.get("text", "") if isinstance(comp, dict) else str(comp)


def label_of(comp):
    """按钮文字去掉括号：按钮本身已经是按钮了。"""
    out = {k: v for k, v in comp.items() if k != "click_event"}
    out["text"] = plain(comp).strip().strip("[]〖〗").strip()
    return out


def convert_line(comps, names):
    """返回 (页头文字, 正文, 按钮表)。"""
    parts = []
    actions = []
    for comp in comps:
        if comp == "":
            continue
        if not isinstance(comp, dict):
            comp = {"text": str(comp)}
        if "score" in comp:
            name = comp["score"]["objective"]
            names.add(name)
            comp = {k: v for k, v in comp.items() if k != "score"}
            comp["text"] = "$(%s)" % name
            comp["bold"] = True         # 数值是这一行的主角
        if "click_event" in comp:
            actions.append({"label": label_of(comp),
                            "action": {"type": "minecraft:run_command",
                                       "command": comp["click_event"]["command"]}})
        parts.append({k: v for k, v in comp.items() if k != "click_event"})
    joined = "".join(plain(p) for p in parts).strip()
    match = HEADER.match(joined)
    if match:
        return match.group(1), None, actions
    if actions and not "".join(plain(p) for p in parts if not any(
            plain(p).strip().strip("[]〖〗").strip() == a["label"]["text"] for a in actions)).strip():
        return None, None, actions
    return None, parts, actions


def convert_page(rel):
    src = read(rel).rstrip("\n").splitlines()
    first = next(i for i, line in enumerate(src) if TELLRAW.match(line))
    pre, body = src[:first], src[first:]
    names = set()
    out = []
    has_title = False
    seen_body = False
    for line in body:
        match = TELLRAW.match(line)
        if not match:
            out.append(line)
            continue
        guard = match.group(1) or ""
        head, parts, actions = convert_line(json.loads(match.group(2)), names)
        if head == "":
            continue
        if head is not None and not seen_body:
            colour = next((c for c in json.loads(match.group(2)) if isinstance(c, dict)), {})
            title = {"text": head, "color": colour.get("color", "white"), "bold": True, "italic": False,
                     "extra": [{"text": " " + ui.fraktur(GLOSS[rel]), "color": ui.BROADCAST_GLOSS, "bold": False}]}
            out.append("%sdata modify %s ui.title set value %s" % (guard, STORE, dump(title)))
            has_title = True
            continue
        if head is not None:
            source = next((c for c in json.loads(match.group(2)) if isinstance(c, dict)), {})
            parts = [{"text": "\n"}, {"text": head, "color": source.get("color", "white"), "bold": True, "italic": False}]
        for action in actions:
            out.append("%sdata modify %s ui.actions append value %s" % (guard, STORE, dump(action)))
        if parts:
            seen_body = True
            entry = {"text": "", "extra": parts + [{"text": "\n"}]}
            text = "%sdata modify %s ui.body append value %s" % (guard, STORE, dump(entry))
            out.append("$" + text if "$(" in text else text)
    assert has_title, rel
    slug = rel.replace("/", "_")
    write("panel/pages/" + slug, out)

    head = list(pre)
    head.append("data modify %s ui set value {title:{text:\"\"},body:[],actions:[]}" % STORE)
    for name in sorted(names):
        head.append("scoreboard players add @s %s 0" % name)
        head.append("execute store result %s v.%s int 1 run scoreboard players get @s %s" % (STORE, name, name))
    call = "function rpg:panel/pages/" + slug
    head.append(call + (" with %s v" % STORE if names else ""))
    head.append("function rpg:panel/ui/show with %s ui" % STORE)
    write(rel, head)


def build_show():
    exit_action = {"label": {"text": "合上", "color": "gray", "italic": False}}
    write("panel/ui/show", [
        '$dialog show @s {"type":"minecraft:multi_action","title":$(title),'
        '"body":{"type":"minecraft:plain_message","width":320,"contents":$(body)},'
        '"actions":$(actions),"columns":2,"exit_action":%s,'
        '"can_close_with_escape":true,"pause":false,"after_action":"close"}' % dump(exit_action)])


def tell(*parts):
    return "tellraw @s " + dump([""] + list(parts))


def text(value, color=ui.GRAY, bold=False):
    return {"text": value, "color": color, "bold": bold, "italic": False}


def patch_sources():
    """转换前的小改动：HUD 开关改成回到首页，首页显示当前状态。"""
    lines = read("panel/hud_toggle").rstrip("\n").splitlines()
    lines = [l for l in lines if "tellraw @s" not in l]
    write("panel/hud_toggle", lines + ["function rpg:panel/open"])

    lines = read("panel/open").rstrip("\n").splitlines()
    tip = next(i for i, l in enumerate(lines) if "切走再切回面板" in l)
    lines[tip:tip + 1] = [
        "execute if entity @s[tag=rpg.panel.hud_off] run " + tell(text("HUD：已隐藏", "#8FC7FF")),
        "execute unless entity @s[tag=rpg.panel.hud_off] run " + tell(text("HUD：显示中", ui.READY)),
        tell(text("切走再切回面板，可再次打开此页。", ui.MUTED)),
    ]
    write("panel/open", lines)

    lines = read("panel/help").rstrip("\n").splitlines()
    home = next(i for i, l in enumerate(lines) if "[返回面板]" in l)
    lines[home:home] = [tell(text("契约：长按放力量，潜行长按放魂誓技能，潜行抬头长按化身，潜行低头长按打开契约。"))]
    lines = [l.replace("面板：切换到玩家面板自动打开；切走再切回可重开。",
                       "面板：切到玩家面板并停留片刻就会打开；切走再切回可重开。") for l in lines]
    write("panel/help", lines)

    src = read("panel/tick")
    old = "execute if entity @s[tag=rpg.h.player_tag1,tag=!rpg.panel.open] run function rpg:panel/open\n"
    assert old in src
    src = src.replace(old, (
        "execute if entity @s[tag=rpg.h.player_tag1,tag=!rpg.panel.open] run scoreboard players add @s rpg_panel_h 1\n"
        "execute unless entity @s[tag=rpg.h.player_tag1] run scoreboard players set @s rpg_panel_h 0\n"
        "execute if entity @s[tag=!rpg.panel.open,scores={rpg_panel_h=%d..}] run function rpg:panel/open\n"
        "execute if entity @s[tag=rpg.panel.open] run scoreboard players set @s rpg_panel_h 0\n" % OPEN_DELAY))
    write("panel/tick", src.rstrip("\n").splitlines())

    src = read("command/soreboard")
    if "rpg_panel_h" not in src:
        write("command/soreboard", src.rstrip("\n").splitlines() + ["scoreboard objectives add rpg_panel_h dummy"])


def relight_pact_dialogs():
    """polish_ui 会把含领主名的短文本改回亮色，契约界面要的是暗色板。"""
    for n in range(1, 8):
        p = ui.pillar(n)
        for rel in ("pact/ui/show%d" % n, "pact/ui/terms_show%d" % n):
            write(rel, read(rel).replace(p["lit"], ui.pillar_mid(n)).rstrip("\n").splitlines())


def main():
    relight_pact_dialogs()
    patch_sources()
    build_show()
    for rel in PAGES:
        convert_page(rel)
    print("player panel: %d pages as dialogs" % len(PAGES))


if __name__ == "__main__":
    main()
