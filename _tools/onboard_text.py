# -*- coding: utf-8 -*-
"""新手开局的世界观旁白：台词、双语字幕、配音（用户 2026-11-23「起名之前先做一个世界观介绍，
类似序章开头的旁白，要有配音、双语字幕」）。

台词在 `_tools/onboard_ref/lines.json`；配音由 GPT 生成（`onboard_ref/vo/VO-BRIEF.md`），用户在
`vo/picks.json` 里挑 take。做法照抄序章（prologue_text.py）：文字进资源包语言文件，键名
`rpg.onboard.<编号>.zh` / `.en`；有配音的句子用配音的真实长度，没有就按预估时长只显示字幕。
"""
import io
import json
import math
import os

import prologue_text as PT

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = os.path.join(HERE, "onboard_ref", "lines.json")
VO_DIR = os.path.join(HERE, "onboard_ref", "vo")
ZH_COLOUR = PT.COLOURS["narrator"]
EN_COLOUR = PT.COLOURS["narrator"]
GAP = 12                 # 两句之间的停顿（刻）
LEAD = 30                # 开场先黑一会儿再出第一句（刻）


def load():
    with io.open(LINES, encoding="utf-8") as fh:
        return [x for x in json.load(fh)["lines"]]


def picked_vo(lid):
    picks = os.path.join(VO_DIR, "picks.json")
    if not os.path.isfile(picks):
        return None
    take = json.load(io.open(picks, encoding="utf-8")).get(lid)
    p = os.path.join(VO_DIR, "takes", "%s_%s.ogg" % (lid, take)) if take else None
    return p if p and os.path.isfile(p) else None


def seconds(line):
    vo = picked_vo(line["id"]) if line.get("voiced") else None
    if vo:
        return PT.ogg_seconds(vo)
    est = (line.get("est") or "").replace("秒", "").strip()
    try:
        return float(est)
    except ValueError:
        return 2.0 + 0.12 * len(line["zh"])


def hold_ticks(line):
    return int(math.ceil((seconds(line) + 0.6) * 20))


def timeline():
    """[(开始刻, 台词, 显示刻数)]，以及总长（刻）。"""
    at, out = LEAD, []
    for x in load():
        n = hold_ticks(x)
        out.append((at, x, n))
        at += n + GAP
    return out, at + 20


def key(lid, part=None):
    base = "rpg.onboard.%s" % lid.lower()
    return base + (".zh" if part is None else ".en" + ("" if part == 0 else "_%d" % (part + 1)))


def bar_names(line, part=0):
    zh = [PT.tr(key(line["id"]), line["zh"], ZH_COLOUR)]
    parts = PT.split_en(line["en"])
    en = [PT.tr(key(line["id"], part), parts[part], EN_COLOUR, italic=True)]
    return zh, en


def write_lang(rp):
    p = os.path.join(rp, "assets", "rpg", "lang", "en_us.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    cur = {}
    if os.path.isfile(p):
        with io.open(p, encoding="utf-8-sig") as fh:
            cur = json.load(fh)
    cur = {k: v for k, v in cur.items() if not k.startswith("rpg.onboard.")}
    for x in load():
        cur[key(x["id"])] = x["zh"]
        for i, part in enumerate(PT.split_en(x["en"])):
            cur[key(x["id"], i)] = part
        cur["rpg.onboard.%s.en_full" % x["id"].lower()] = x["en"]
    with io.open(p, "w", encoding="utf-8") as fh:
        json.dump(cur, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")


def vo_sounds(rp):
    """登记挑好的配音：rpg:vo.onboard.<编号>（类别 voice）。返回登记了几句。"""
    out = os.path.join(rp, "assets", "rpg", "sounds", "vo", "onboard")
    path = os.path.join(rp, "assets", "rpg", "sounds.json")
    sounds = {}
    if os.path.isfile(path):
        with io.open(path, encoding="utf-8-sig") as fh:
            sounds = json.load(fh)
    sounds = {k: v for k, v in sounds.items() if not k.startswith("vo.onboard.")}
    n = 0
    for x in load():
        src = picked_vo(x["id"]) if x.get("voiced") else None
        if not src:
            continue
        os.makedirs(out, exist_ok=True)
        PT.louder(src, os.path.join(out, x["id"].lower() + ".ogg"))
        sounds["vo.onboard.%s" % x["id"].lower()] = {
            "sounds": [{"name": "rpg:vo/onboard/%s" % x["id"].lower(), "attenuation_distance": 1024}],
            "subtitle": "rpg.onboard.%s.en_full" % x["id"].lower()}
        n += 1
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(sounds, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return n


def voiced(line):
    return bool(line.get("voiced") and picked_vo(line["id"]))
