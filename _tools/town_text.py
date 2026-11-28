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


# ============================================================================ 台词节奏（用户 2026-11-28：「对话一下子把话全说出来了」）
def ogg_seconds(path):
    data = open(path, "rb").read()
    i = data.find(b"\x01vorbis")
    rate = int.from_bytes(data[i + 12:i + 16], "little") if i >= 0 else 48000
    j = data.rfind(b"OggS")
    gran = int.from_bytes(data[j + 6:j + 14], "little") if j >= 0 else 0
    return gran / float(rate or 48000)


def line_ticks(pid):
    """一句台词占多久（刻）：有配音按配音长度，没有按字数。之后留一小段停顿。"""
    secs = len(LINES[pid]["zh"]) * 0.2 + 1.5
    if has_vo(pid):
        picks = json.load(io.open(PICKS, encoding="utf-8"))
        try:
            secs = ogg_seconds(os.path.join(VO_DIR, "takes", "%s_%d.ogg" % (pid, picks[pid])))
        except Exception:
            pass
    return int((secs + 0.8) * 20 + 0.999)


def pace(dp):
    """构建后处理：城镇函数里一口气连说的几句台词，只留第一句当场说，其余按配音长度排进队列，一句一句来。
    队列在 storage rpg:say q（每项：f 第几句、due 到点的游戏刻、sid 说给谁、x/y/z 说话的位置）；每刻到点的播出。
    说给 @s 的台词：排队时给 @s 记上这一串的 sid（rpg_say），播出时说给 sid 对得上的玩家。"""
    import glob
    import re
    func = os.path.join(dp, "data", "rpg", "function")
    root = os.path.join(func, "town")
    outdir = os.path.join(root, "say")
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    by_zh = sorted(((l["zh"], pid) for pid, l in LINES.items()), key=lambda q: -len(q[0]))

    def wf(name, lines):
        with io.open(os.path.join(outdir, name + ".mcfunction"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")

    n = 0
    files = 0
    for path in sorted(glob.glob(os.path.join(root, "**", "*.mcfunction"), recursive=True)):
        if path.startswith(outdir):
            continue
        src = io.open(path, encoding="utf-8").read().split("\n")
        blocks = []
        k = 0
        while k < len(src):
            m = re.match(r"^tellraw (\S+) (\[.*\])$", src[k])
            if m and "〖" in src[k] and "hover_event" in src[k]:
                pid = next((p for zh, p in by_zh if zh in src[k]), None)
                size = 2 if k + 1 < len(src) and src[k + 1].startswith("playsound rpg:vo.town.") else 1
                if pid:
                    blocks.append((k, size, pid, m.group(1)))
                k += size
                continue
            k += 1
        if len(blocks) < 2:
            continue
        files += 1
        out = list(src)
        delay = line_ticks(blocks[0][2])
        sid_done = False
        for k, size, pid, who in reversed(blocks[1:]):
            pass
        # 从后往前替换，下标不乱；延迟先按顺序算好
        delays = []
        for k, size, pid, who in blocks[1:]:
            delays.append(delay)
            delay += line_ticks(pid)
        uses_s = any(who == "@s" for _, _, _, who in blocks[1:])
        for (k, size, pid, who), d in reversed(list(zip(blocks[1:], delays))):
            n += 1
            body = src[k:k + size]
            if who == "@s":
                body = [("execute as @a if score @s rpg_say = #cur rpg_say run " if b.startswith("tellraw") else
                         "execute as @a if score @s rpg_say = #cur rpg_say at @s run ") + b for b in body]
            wf("d%d" % n, ["# %s" % pid] + body)
            out[k:k + size] = ["execute store result score #due rpg_say run time query gametime",
                               "scoreboard players add #due rpg_say %d" % d,
                               "function rpg:town/say/push {f:%d}" % n]
        if uses_s:
            first = blocks[1][0]
            # 第一句排队的位置之前（替换后下标没变：前面的行没动过）
            out[first:first] = ["scoreboard players add #sid rpg_say 1", "scoreboard players operation @s rpg_say = #sid rpg_say"]
        else:
            first = blocks[1][0]
            out[first:first] = ["scoreboard players add #sid rpg_say 1"]
        io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    wf("load", ["scoreboard objectives add rpg_say dummy", "data modify storage rpg:say q set value []"])
    wf("push", ["# 排一句（宏 f）：#due 到点的游戏刻、#sid 说给谁；位置取当前执行位置",
                "data modify storage rpg:say e set value {f:0,due:0,sid:0,x:0,y:0,z:0}",
                "$data modify storage rpg:say e.f set value $(f)",
                "execute store result storage rpg:say e.due int 1 run scoreboard players get #due rpg_say",
                "execute store result storage rpg:say e.sid int 1 run scoreboard players get #sid rpg_say",
                "execute summon minecraft:marker run function rpg:town/say/pos",
                "data modify storage rpg:say q append from storage rpg:say e"])
    wf("pos", ["execute store result storage rpg:say e.x int 1 run data get entity @s Pos[0]",
               "execute store result storage rpg:say e.y int 1 run data get entity @s Pos[1]",
               "execute store result storage rpg:say e.z int 1 run data get entity @s Pos[2]", "kill @s"])
    wf("tick", ["execute if data storage rpg:say q[0] run function rpg:town/say/run"])
    wf("run", ["execute store result score #now rpg_say run time query gametime",
               "data modify storage rpg:say t set from storage rpg:say q", "data modify storage rpg:say q set value []",
               "function rpg:town/say/each"])
    wf("each", ["execute unless data storage rpg:say t[0] run return 0",
                "data modify storage rpg:say e set from storage rpg:say t[0]", "data remove storage rpg:say t[0]",
                "execute store result score #due rpg_say run data get storage rpg:say e.due",
                "execute if score #due rpg_say > #now rpg_say run data modify storage rpg:say q append from storage rpg:say e",
                "execute if score #due rpg_say <= #now rpg_say run function rpg:town/say/fire with storage rpg:say e",
                "function rpg:town/say/each"])
    wf("fire", ["$scoreboard players set #cur rpg_say $(sid)", "$scoreboard players set #f rpg_say $(f)",
                "$execute in minecraft:overworld positioned $(x) $(y) $(z) run function rpg:town/say/dispatch"])
    wf("dispatch", ["execute if score #f rpg_say matches %d run return run function rpg:town/say/d%d" % (i, i) for i in range(1, n + 1)] or ["return 0"])
    return files, n
