# -*- coding: utf-8 -*-
"""篡夺者二阶段（篡夺圣灵）的外观：在首席附魔师模型上做两件事（docs/USURPER-DESIGN.md 第 4、9 节）。

    python add_usurper_holy_look.py ../resourcepack

必须在 add_prime_enchanter_model.py（模型、贴图）和 add_usurper_fx_art.py（王冠道具）之后跑。
首席附魔师的生成器不动；这里只改它写出的两样东西：

1. 重着色（设计稿第 9 节第 2 条）：原作的冰蓝、电光（青、蓝、黄的像素）按亮度映射到篡夺白金，
   红袍、灰帽、黑边保留原色。改的是 textures/item/prime_enchanter/atlas.png。
2. 王冠：原作商人的王冠 SM_Crown（add_usurper_fx_art.py 的 crown 道具，已重着色）并进头部模型，
   坐在帽顶，随头部动作一起动。王冠的面带 tintindex 0，头部原有的面去掉 tintindex：
   破绽时只给头部显示实体染一层暗色，就只有王冠暗下去。
   另写一份不带王冠的头部 rpg:usurper_fx/pe_head_bare，击败时换上它，王冠碎裂。

重复运行无副作用：头部模型里已经有王冠（贴图 #1）就跳过。
"""
import colorsys
import json
import os
import sys

import numpy as np
from PIL import Image

import add_usurper_fx_art as art

KEY = "usurper_fx"
CROWN_WIDTH = 8.8          # 模型单位：帽顶 8.24 宽，王冠略宽一点
CROWN_HEIGHT = 3.2
CROWN_SINK = 0.6           # 王冠下沿压进帽顶一点，不露缝


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def recolour(path):
    """Ice blue / electric yellow pixels -> white-gold by luminance; reds, greys and darks kept."""
    im = Image.open(path).convert("RGBA")
    a = np.array(im).astype(float)
    ramp = [np.array(c, float) for c in reversed(art.WHITE_GOLD)]        # deep, mid, light
    changed = 0
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            r, g, b, al = a[y, x]
            if al == 0:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            hue = h * 360
            ice = 150 <= hue <= 230 and s > 0.22
            spark = 40 <= hue <= 70 and s > 0.35
            if not (ice or spark):
                continue
            t = min(1.0, max(0.0, (l - 0.15) / 0.7))
            rgb = ramp[0] + (ramp[1] - ramp[0]) * (t * 2) if t < 0.5 else ramp[1] + (ramp[2] - ramp[1]) * (t * 2 - 1)
            a[y, x, :3] = rgb
            changed += 1
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(path)
    return changed


def crown_elements(crown, top, cx, cz):
    """The crown prop's elements, refitted onto the hat top (x/z centred on cx/cz, base at `top`)."""
    els = crown["elements"]
    lo = [min(min(e["from"][i], e["to"][i]) for e in els) for i in range(3)]
    hi = [max(max(e["from"][i], e["to"][i]) for e in els) for i in range(3)]
    sx = CROWN_WIDTH / (hi[0] - lo[0])
    sz = CROWN_WIDTH / (hi[2] - lo[2])
    sy = CROWN_HEIGHT / (hi[1] - lo[1])
    mid = [(lo[0] + hi[0]) / 2, lo[1], (lo[2] + hi[2]) / 2]

    def fit(p):
        return [round(cx + (p[0] - mid[0]) * sx, 4), round(top - CROWN_SINK + (p[1] - mid[1]) * sy, 4),
                round(cz + (p[2] - mid[2]) * sz, 4)]

    out = []
    for e in els:
        n = {"from": fit(e["from"]), "to": fit(e["to"]), "light_emission": 15, "shade": False, "faces": {}}
        if "rotation" in e:
            r = dict(e["rotation"])
            r["origin"] = fit(r["origin"])
            n["rotation"] = r
        for face, f in e["faces"].items():
            n["faces"][face] = dict(f, texture="#1", tintindex=0)
        out.append(n)
    return out


def main():
    rp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(art.HERE, "..", "resourcepack")
    a = os.path.join(rp, "assets", "rpg")
    head_path = os.path.join(a, "models", "prime_enchanter", "head.json")
    crown_path = os.path.join(a, "models", KEY, "crown.json")
    if not (os.path.exists(head_path) and os.path.exists(crown_path)):
        raise SystemExit("usurper holy look: run add_prime_enchanter_model.py and add_usurper_fx_art.py first")
    head = load(head_path)
    if "1" in head["textures"]:
        print("usurper holy look: already applied")
        return
    # 不带王冠的原样头部，击败时换上
    bare = json.loads(json.dumps(head))
    save(os.path.join(a, "models", KEY, "pe_head_bare.json"), bare)
    save(os.path.join(a, "items", KEY, "pe_head_bare.json"),
         {"model": {"type": "minecraft:model", "model": "rpg:%s/pe_head_bare" % KEY}})
    n = recolour(os.path.join(a, "textures", "item", "prime_enchanter", "atlas.png"))
    # 帽顶：头部方块（最大的那块）的上表面
    box = max(head["elements"], key=lambda e: (e["to"][0] - e["from"][0]) * (e["to"][1] - e["from"][1]))
    top = max(box["to"][1], box["from"][1])
    cx = (box["from"][0] + box["to"][0]) / 2
    cz = (box["from"][2] + box["to"][2]) / 2
    for e in head["elements"]:
        for f in e["faces"].values():
            f.pop("tintindex", None)
    head["elements"] += crown_elements(load(crown_path), top, cx, cz)
    head["textures"]["1"] = "rpg:item/%s/crown" % KEY
    save(head_path, head)
    print("usurper holy look: %d ice/electric texels -> white-gold, crown on the hat (top y %.2f)" % (n, top))


if __name__ == "__main__":
    main()
