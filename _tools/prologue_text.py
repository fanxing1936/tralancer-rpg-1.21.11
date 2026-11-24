# -*- coding: utf-8 -*-
"""序章的文字层：语言文件、双语字幕、配音。

台词原稿是脚本书导出的 `_tools/prologue_ref/lines.json`（prologue_lines.py）。文字写进资源包的语言文件
`assets/rpg/lang/en_us.json`（所有客户端语言都会回落到它），键名 `rpg.prologue.<编号>.zh` / `.en`；
数据包里只引用键名，并带上原文作 fallback，没装资源包也看得到字。

字幕（2026-11-22 技术验证）：两条粉色 Boss 血条。资源包把粉色血条的条本身藏掉了，只剩名字，
于是屏幕顶部是干净的两行：中文在上、英文在下。英文太长的句子按词拆成几段，在这句的显示时间里依次换。
"""
import io
import json
import math
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = os.path.join(HERE, "prologue_ref", "lines.json")
VO_DIR = os.path.join(HERE, "prologue_ref", "vo")

ZH_BAR, EN_BAR = "rpg:prologue_zh", "rpg:prologue_en"
EN_MAX = 78          # 英文一行最多的字符数（guiScale 4 时屏幕约 480 个单位宽）

COLOURS = {"narrator": "#BFB8A8", "lucifer": "#F2E6B8", "michael": "#FFD85A", "beelzebub": "#B5D957",
           "belial": "#D97AD9", "mammon": "#E6A23C", "antichrist": "#8B1A1A"}
WHO = {"narrator": ("", ""), "lucifer": ("路西法", "Lucifer"), "michael": ("米迦勒", "Michael"),
       "beelzebub": ("别西卜", "Beelzebub"), "belial": ("贝利尔", "Belial"), "mammon": ("玛门", "Mammon"),
       "antichrist": ("敌基督", "The Antichrist")}
BODY_ZH, BODY_EN = "#FFFFFF", "#D8D2C4"


def load():
    with io.open(LINES, encoding="utf-8") as fh:
        return {x["id"]: x for x in json.load(fh)["lines"]}


def ogg_seconds(path):
    b = open(path, "rb").read()
    i = b.find(b"\x01vorbis")
    sr = struct.unpack("<I", b[i + 12:i + 16])[0]
    j = b.rfind(b"OggS")
    return struct.unpack("<q", b[j + 6:j + 14])[0] / sr


def picked_vo(lid):
    """用户挑好的 take（vo/picks.json），没有就是 None。"""
    picks = os.path.join(VO_DIR, "picks.json")
    if not os.path.isfile(picks):
        return None
    take = json.load(io.open(picks, encoding="utf-8")).get(lid)
    p = os.path.join(VO_DIR, "takes", "%s_%s.ogg" % (lid, take)) if take else None
    return p if p and os.path.isfile(p) else None


def seconds(line):
    """这句占多久：有配音用配音的真实长度，否则按脚本书的预估，再否则按字数。"""
    vo = picked_vo(line["id"]) if line.get("voiced") else None
    if vo:
        return ogg_seconds(vo)
    est = (line.get("est") or "").replace("秒", "").strip()
    try:
        return float(est)
    except ValueError:
        return 2.0 + 0.12 * len(line["zh"])


def hold_ticks(line):
    return int(math.ceil((seconds(line) + 0.5) * 20))


def split_en(text):
    if len(text) <= EN_MAX:
        return [text]
    words, parts, cur = text.split(" "), [], ""
    n = int(math.ceil(len(text) / float(EN_MAX)))
    target = len(text) / float(n)
    for w in words:
        if cur and len(cur) + 1 + len(w) > target and len(parts) < n - 1:
            parts.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    parts.append(cur)
    return parts


def lang(lines):
    d = {}
    for lid, x in lines.items():
        d["rpg.prologue.%s.zh" % lid] = x["zh"]
        for i, part in enumerate(split_en(x["en"])):
            d["rpg.prologue.%s.en%s" % (lid, "" if i == 0 else "_%d" % (i + 1))] = part
        d["rpg.prologue.%s.en_full" % lid] = x["en"]
    for k, (zh, en) in WHO.items():
        if zh:
            d["rpg.prologue.who.%s.zh" % k] = zh
            d["rpg.prologue.who.%s.en" % k] = en
    return d


def write_lang(rp, lines):
    p = os.path.join(rp, "assets", "rpg", "lang", "en_us.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    cur = {}
    if os.path.isfile(p):
        with io.open(p, encoding="utf-8-sig") as fh:
            cur = json.load(fh)
    cur = {k: v for k, v in cur.items() if not k.startswith("rpg.prologue.")}
    cur.update(lang(lines))
    with io.open(p, "w", encoding="utf-8") as fh:
        json.dump(cur, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    return len(cur)


def tr(key, fallback, colour, **kw):
    c = {"translate": key, "fallback": fallback, "color": colour, "italic": False}
    c.update(kw)
    return c


def bar_names(line, part=0):
    """(中文行, 英文行) 两个 JSON 文本组件。"""
    sp = line.get("speaker")
    col = COLOURS.get(sp, BODY_ZH)
    zh, en = [], []
    if sp in WHO and WHO[sp][0]:
        zh.append(tr("rpg.prologue.who.%s.zh" % sp, WHO[sp][0] + "：", col, bold=True))
        zh[-1]["fallback"] = WHO[sp][0]
        zh.append({"text": "：", "color": col, "bold": True})
        en.append(tr("rpg.prologue.who.%s.en" % sp, WHO[sp][1], col, bold=True))
        en.append({"text": ": ", "color": col, "bold": True})
    body_zh = COLOURS["narrator"] if sp == "narrator" else BODY_ZH
    zh.append(tr("rpg.prologue.%s.zh" % line["id"], line["zh"], body_zh))
    parts = split_en(line["en"])
    key = "rpg.prologue.%s.en%s" % (line["id"], "" if part == 0 else "_%d" % (part + 1))
    en.append(tr(key, parts[part], BODY_EN if sp != "narrator" else COLOURS["narrator"], italic=sp == "narrator"))
    return zh, en


def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def sub_functions(fn, lines, P, O, who_sel):
    """sub/<编号>：换上这句字幕、播配音、开始计时；sub/tick：计时，英文分段，到时清空。"""
    tick = ["execute unless score #sub %s matches 1.. run return 0" % O,
            "scoreboard players remove #sub %s 1" % O]
    for lid, x in sorted(lines.items()):
        total = hold_ticks(x)
        zh, en = bar_names(x)
        body = ["bossbar set %s name %s" % (ZH_BAR, js(zh)), "bossbar set %s name %s" % (EN_BAR, js(en)),
                "scoreboard players set #sub %s %d" % (O, total),
                "scoreboard players set #subn %s %d" % (O, int(lid[1:]) + 100 * "UNTDMLEXR".index(lid[0]))]
        if x.get("voiced") and picked_vo(lid):
            body.append("execute as %s at @s run playsound rpg:vo.prologue.%s voice @s ~ ~ ~ 1 1" % (who_sel, lid.lower()))
        fn("sub/%s" % lid.lower(), body)
        parts = split_en(x["en"])
        if len(parts) > 1:
            code = int(lid[1:]) + 100 * "UNTDMLEXR".index(lid[0])
            for i in range(1, len(parts)):
                at = total - int(total * i / len(parts))   # 剩余刻数到这里时换下一段
                _, en_i = bar_names(x, i)
                tick.append("execute if score #subn %s matches %d if score #sub %s matches %d run bossbar set %s name %s"
                            % (O, code, O, at, EN_BAR, js(en_i)))
    tick += ["execute if score #sub %s matches 0 run bossbar set %s name \"\"" % (O, ZH_BAR),
             "execute if score #sub %s matches 0 run bossbar set %s name \"\"" % (O, EN_BAR)]
    fn("sub/tick", tick)
    fn("sub/clear", ["scoreboard players set #sub %s 0" % O,
                     "bossbar set %s name \"\"" % ZH_BAR, "bossbar set %s name \"\"" % EN_BAR])


VO_GAIN_DB = 4.0     # 用户 2026-11-22「台词声音太小了」：整体抬 4 dB，峰值软限幅到 0.88 以内


def louder(src, dst):
    """配音抬响：增益 VO_GAIN_DB，超过 0.8 的部分用 tanh 软限幅（不削波），写回 Ogg Vorbis。"""
    import numpy as np
    import soundfile as sf
    x, sr = sf.read(src, always_2d=True, dtype="float32")
    y = x * (10 ** (VO_GAIN_DB / 20.0))
    a = np.abs(y)
    knee, room = 0.72, 0.16      # 最高到 0.88，给 Vorbis 编码的过冲留余量
    y = np.where(a > knee, np.sign(y) * (knee + room * np.tanh((a - knee) / room)), y).astype("float32")
    with sf.SoundFile(dst, "w", sr, y.shape[1], format="OGG", subtype="VORBIS", compression_level=0.4) as fh:
        for i in range(0, len(y), 4096):
            fh.write(y[i:i + 4096])


def vo_sounds(rp, lines):
    """登记已挑好的配音：rpg:vo.prologue.<编号>（类别 voice），并把文件拷进资源包。"""
    out = os.path.join(rp, "assets", "rpg", "sounds", "vo", "prologue")
    path = os.path.join(rp, "assets", "rpg", "sounds.json")
    sounds = {}
    if os.path.isfile(path):
        with io.open(path, encoding="utf-8-sig") as fh:
            sounds = json.load(fh)
    sounds = {k: v for k, v in sounds.items() if not k.startswith("vo.prologue.")}
    n = 0
    for lid, x in lines.items():
        src = picked_vo(lid) if x.get("voiced") else None
        if not src:
            continue
        os.makedirs(out, exist_ok=True)
        louder(src, os.path.join(out, lid.lower() + ".ogg"))
        # 过场里镜头一次滑几十格，客户端听者（插值中的镜头）离服务端放音的位置（玩家=镜头的目标点）很远，
        # 默认 16 格衰减会让旁白听不见；放大衰减距离，等于不随距离变小
        sounds["vo.prologue.%s" % lid.lower()] = {"sounds": [{"name": "rpg:vo/prologue/%s" % lid.lower(),
                                                              "attenuation_distance": 1024}],
                                                  "subtitle": "rpg.prologue.%s.en_full" % lid}
        n += 1
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(sounds, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return n
