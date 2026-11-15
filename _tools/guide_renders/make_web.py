# -*- coding: utf-8 -*-
"""Blockbench 渲染图（guide_renders/*.png，900×900 透明）→ 图鉴用的小图 guide_renders/web/*.webp。

    python guide_renders/make_web.py      # 在 _tools 下运行

裁掉透明边，长边缩到 360，存 webp（质量 88）。全部约 400 KB，内嵌进图鉴。
"""
import glob
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs(os.path.join(HERE, "web"), exist_ok=True)
    for f in sorted(glob.glob(os.path.join(HERE, "*.png"))):
        im = Image.open(f).convert("RGBA")
        im = im.crop(im.getbbox())
        s = 360 / max(im.size)
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
        im.save(os.path.join(HERE, "web", os.path.basename(f)[:-4] + ".webp"), "WEBP", quality=88, method=6)
    print("web renders written")


if __name__ == "__main__":
    main()
