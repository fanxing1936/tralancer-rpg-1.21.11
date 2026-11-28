# -*- coding: utf-8 -*-
"""城镇台词：〖说话人〗 + 英文花体注 + 正文（和雅克、扫罗的播报同一格式），有配音时一起播。

台词原稿 town_ref/lines.json（lines_src.py 导出）；配音照 town_ref/vo/VO-BRIEF.md 生成，picks.json 选中的 take
由 install_vo() 拷进资源包，登记成 rpg:vo.town.<编号小写>。没有配音时只显示字幕。
"""
import io
import json
import os
import shutil

import rpg_ui_style as ui

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "town_ref")
DOC = json.load(io.open(os.path.join(REF, "lines.json"), encoding="utf-8"))
LINES = {l["id"]: l for l in DOC["lines"]}
SPK = DOC["speakers"]
COLOURS = {"priest": ui.BROADCAST_HOLY, "elder": "#C9B27A", "inquisitor": "#B8902F", "edgewalker": ui.RITUAL, "witch": "#B48AD8",
           "farmwife": ui.BROADCAST_NAME, "farmer": ui.BROADCAST_NAME, "youth": ui.BROADCAST_NAME, "bard": "#D9B76A", "watchman": "#A8B4C0",
           "child": ui.BROADCAST_NAME, "servant": ui.BROADCAST_VOID}
VO_DIR = os.path.join(REF, "vo")
PICKS = os.path.join(VO_DIR, "picks.json")


def has_vo(pid):
    if not os.path.exists(PICKS):
        return False
    picks = json.load(io.open(PICKS, encoding="utf-8"))
    return pid in picks and os.path.exists(os.path.join(VO_DIR, "takes", "%s_%d.ogg" % (pid, picks[pid])))


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def comp(pid, name=None):
    l = LINES[pid]
    s = SPK[l["speaker"]]
    col = COLOURS.get(l["speaker"], ui.BROADCAST_NAME)
    return ["", {"text": "〖", "color": col, "bold": True, "italic": False}, {"text": name or s["zh"], "color": col, "bold": True, "italic": False},
            {"text": "〗", "color": col, "bold": True, "italic": False}, {"text": " " + ui.fraktur(s["en"]), "color": ui.BROADCAST_GLOSS, "italic": False},
            {"text": ui.GAP + l["zh"], "color": ui.BROADCAST_BODY, "italic": False},
            ]


def say(pid, who="@a[distance=..24]", name=None):
    """一句台词：字幕（中文正文；悬停看英文）+ 配音。返回命令列表。"""
    l = LINES[pid]
    c = comp(pid, name)
    c[-1]["hover_event"] = {"action": "show_text", "value": {"text": l["en"], "color": ui.BROADCAST_GLOSS, "italic": False}}
    out = ["tellraw %s %s" % (who, J(c))]
    if has_vo(pid):
        out.append("playsound rpg:vo.town.%s voice %s ~ ~ ~ 1 1" % (pid.lower(), who))
    return out


def install_vo(rp):
    """把选中的配音拷进资源包、登记声音事件。返回装了几句。"""
    if not os.path.exists(PICKS):
        return 0
    picks = json.load(io.open(PICKS, encoding="utf-8"))
    dst = os.path.join(rp, "assets", "rpg", "sounds", "vo", "town")
    os.makedirs(dst, exist_ok=True)
    sj = os.path.join(rp, "assets", "rpg", "sounds.json")
    doc = json.load(io.open(sj, encoding="utf-8")) if os.path.exists(sj) else {}
    n = 0
    for pid, take in picks.items():
        src = os.path.join(VO_DIR, "takes", "%s_%d.ogg" % (pid, take))
        if pid not in LINES or not os.path.exists(src):
            continue
        shutil.copyfile(src, os.path.join(dst, pid.lower() + ".ogg"))
        doc["vo.town." + pid.lower()] = {"category": "voice", "sounds": [{"name": "rpg:vo/town/" + pid.lower(), "stream": True}]}
        n += 1
    with io.open(sj, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    return n
