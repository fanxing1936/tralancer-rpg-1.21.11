# -*- coding: utf-8 -*-
"""精英首领的位图血条（用户 2026-11-23/24：「要和正规 Boss 的血条一样，风格规范统一」「名字显示在下方」）。

    python add_elite_bar_art.py ../resourcepack

和教皇、雅克、扫罗同一套（add_pope_fx_art）：原版粉色血条贴图本来就是全透明，血条名字换成一整串位图——
  横幅（bar_body，20 档，橙金，中间是首领王冠图标）+ 退格 + 王冠与两枚词缀图标 + 花体英文名 + 进格。
名字和图标挂在横幅下方，字号和位置取正式 Boss 标题的 TITLE_HEIGHT / TITLE_ASCENT，按每种生物名的宽度居中。
花体字母直接取原版 unifont（游戏里其余花体也是它），每种生物的名字烘焙成一个字形。
"""
import glob
import io
import json
import os
import sys
import zipfile

import numpy as np
from PIL import Image

import rpg_ui_style as ui
import world_loot_spec as W
from add_pope_fx_art import BAR_ASCENT, BAR_H, BAR_W, TITLE_ASCENT, TITLE_HEIGHT, _box, bar_body, dump, save, solid, trimmed

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "world_ref", "art")
EMBLEM = os.path.join(ART, "affix_champion.png")
FONT = "rpg:elite_bar"
STEPS = 20
FIRST = 0xE6D0                 # 横幅 21 档
ICON0 = 0xE700                 # 图标：王冠 + 10 枚词缀（编号同 add_elites.AFFIX）
NAME0 = 0xE710                 # 每种生物名一个字形
BACK0 = 0xE740                 # 每种生物名的退格
ON0 = 0xE770                   # 每种生物名的进格
GAP = ""                 # 图标与名字之间的空隙
RAMP = [(0xFF, 0xE7, 0xA0), (0xFF, 0xAA, 0x00), (0x8A, 0x5A, 0x00), (0x2A, 0x1A, 0x00)]
ICONS = {0: "champion", 1: "swift", 2: "iron", 3: "rage", 4: "leech", 5: "frost", 6: "venom", 7: "burst",
         8: "summon", 9: "taint", 10: "holy"}
MOBS = [m for m in W.WORLD_TABLES if m not in ("elder_guardian", "vex", "silverfish", "endermite")]


def char(step):
    return chr(FIRST + step)


def icon(k):
    return chr(ICON0 + k)


def name_char(mob):
    return chr(NAME0 + MOBS.index(mob))


def back_char(mob):
    return chr(BACK0 + MOBS.index(mob))


def on_char(mob):
    return chr(ON0 + MOBS.index(mob))


def unifont():
    """原版 unifont 的 hex 表（资源目录里那份 unifont.zip）。"""
    from mc_env import JAR
    mc = os.path.dirname(os.path.dirname(os.path.dirname(JAR)))
    for idx in sorted(glob.glob(os.path.join(mc, "assets", "indexes", "*.json")), key=os.path.getmtime, reverse=True):
        objs = json.load(io.open(idx, encoding="utf-8"))["objects"]
        if "minecraft/font/unifont.zip" in objs:
            h = objs["minecraft/font/unifont.zip"]["hash"]
            z = zipfile.ZipFile(os.path.join(mc, "assets", "objects", h[:2], h))
            name = next(n for n in z.namelist() if n.endswith(".hex"))
            table = {}
            for line in z.read(name).decode("ascii").splitlines():
                cp, hx = line.split(":")
                table[int(cp, 16)] = hx
            return table
    raise SystemExit("unifont.zip not found next to %s" % JAR)


def glyph(table, ch):
    hx = table[ord(ch)]
    w = len(hx) * 4 // 16
    rows = [int(hx[i * w // 4:(i + 1) * w // 4], 16) for i in range(16)]
    a = np.zeros((16, w), bool)
    for y, r in enumerate(rows):
        for x in range(w):
            a[y, x] = bool(r >> (w - 1 - x) & 1)
    cols = np.flatnonzero(a.any(axis=0))
    return a[:, cols[0]:cols[-1] + 1] if len(cols) else np.zeros((16, 4), bool)


def name_image(table, text):
    parts = []
    for ch in ui.fraktur(text):
        g = np.zeros((16, 6), bool) if ch == " " else glyph(table, ch)
        parts += [g, np.zeros((16, 2), bool)]
    a = np.concatenate(parts[:-1], axis=1)
    img = np.zeros((16, a.shape[1], 4), np.uint8)
    img[a] = (255, 255, 255, 255)
    return Image.fromarray(img, "RGBA")


def banner(step):
    a, shape = bar_body(RAMP)
    columns = np.flatnonzero(shape.any(axis=0))
    split = columns[0] + (columns[-1] + 1 - columns[0]) * step // STEPS
    lost = shape.copy()
    lost[:, :split] = False
    a[lost, :3] = (a[lost, :3] * 0.16).astype(np.uint8) + 12
    out = Image.fromarray(a, "RGBA")
    if os.path.exists(EMBLEM):
        drawn = trimmed(EMBLEM)
        width = max(1, round(drawn.width * float(BAR_H) / drawn.height))
        out.alpha_composite(solid(_box(drawn, width, BAR_H), 12), ((BAR_W - width) // 2, 0))
    return out


def advance(png_w, png_h=16):
    """位图字形的前进宽度（游戏里按 height/png 高缩放，再加 1）"""
    return int(round(png_w * float(TITLE_HEIGHT) / png_h)) + 1


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    rp = os.path.join(pack, "assets", "rpg")
    out = os.path.join(rp, "textures", "font", "elite_bar")
    providers, advances = [], {GAP: 2}
    for step in range(STEPS + 1):
        stem = "bar_%d" % step
        save(banner(step), os.path.join(out, stem + ".png"))
        providers.append({"type": "bitmap", "file": "rpg:font/elite_bar/%s.png" % stem,
                          "height": BAR_H, "ascent": BAR_ASCENT, "chars": [char(step)]})
    icon_w = 0
    for k, v in ICONS.items():
        src = os.path.join(ART, "affix_%s.png" % v)
        Image.open(src).convert("RGBA").save(os.path.join(out, "icon_%s.png" % v))
        providers.append({"type": "bitmap", "file": "rpg:font/elite_bar/icon_%s.png" % v,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [icon(k)]})
        icon_w = advance(16)
    table = unifont()
    for mob in MOBS:
        img = name_image(table, W.MOB_EN[mob])
        save(img, os.path.join(out, "name_%s.png" % mob))
        providers.append({"type": "bitmap", "file": "rpg:font/elite_bar/name_%s.png" % mob,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [name_char(mob)]})
        shown = 3 * icon_w + advances[GAP] + advance(img.width)
        advances[back_char(mob)] = -(BAR_W + 1 + shown) // 2
        advances[on_char(mob)] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "elite_bar.json"), {"providers": providers})
    print("elite bar: %d steps, %d icons, %d names" % (STEPS + 1, len(ICONS), len(MOBS)))


if __name__ == "__main__":
    main()
