# -*- coding: utf-8 -*-
"""把作者给的原图裁成物品图标该有的样子。

两个毛病，作者都在游戏里看出来了：

* **玛门的弓显得小**。原图是 32x32 的画布，可弓只占中间 16x16 ——
  填充率 50%，而原版的弓填到 88%。物品栏里贴图是按槽位拉伸的，
  所以画布留白多少，图标就小多少。裁掉留白即可，不必重绘。
* **图腾是 223x231**。非正方、非二次幂，进不了物品图集。必须重采样。

一条要紧的规矩：**弓的四个拉弓阶段必须共用同一个裁剪框**。
各自按自己的包围盒裁，四张图的原点就对不齐，拉弓时弓会在手里跳。
所以先取四张的**并集**，再用同一个框裁同一个位置。

裁剪不缩放：并集框本来就是 16x16 左右，直接居中放进一张略大的画布，
填充率就落在原版那个区间，而且**一个像素都没有重采样** —— 像素画经不起
非整数倍缩放，1.75 倍会把弓弦上一像素宽的线搓成粗细不匀的锯齿。
"""
import io
import os
import sys

import png_tool as P

SRC = sys.argv[1] if len(sys.argv) > 1 else r"F:/筑梦 MCBE/新建文件夹"
RP = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"
OUT = os.path.join(RP, "assets/rpg/textures/item")

FILL = 0.88          # 原版弓的填充率，量出来是 81~94%，取中间

# 四个拉弓阶段共用一个裁剪框 —— 见模块注释
BOW = [("red_snake", "mammon_bow"),
       ("red_snake_pulling_0", "mammon_bow_pulling_0"),
       ("red_snake_pulling_1", "mammon_bow_pulling_1"),
       ("red_snake_pulling_2", "mammon_bow_pulling_2")]

# 单张的，各自按自己的包围盒缩放到正方画布
SINGLE = [("MCD_Totem_of_Shielding_artifact", "exorcism_totem", 32)]


def crop(w, h, rgba, x0, y0, aw, ah):
    art = bytearray(aw * ah * 4)
    for y in range(ah):
        s = ((y0 + y) * w + x0) * 4
        art[y * aw * 4:(y + 1) * aw * 4] = rgba[s:s + aw * 4]
    return bytes(art)


def centre(aw, ah, art, canvas):
    out = bytearray(canvas * canvas * 4)
    ox, oy = (canvas - aw) // 2, (canvas - ah) // 2
    for y in range(ah):
        d = ((oy + y) * canvas + ox) * 4
        out[d:d + aw * 4] = art[y * aw * 4:(y + 1) * aw * 4]
    return bytes(out)


def do_series(pairs):
    """一组必须互相对齐的图。共用并集裁剪框，不缩放。"""
    imgs, boxes = [], []
    for src, _dst in pairs:
        p = os.path.join(SRC, src + ".png")
        if not os.path.isfile(p):
            print("  缺 %s.png，整组跳过" % src)
            return 0
        w, h, r = P.read(p)
        bb = P.bbox(w, h, r)
        imgs.append((w, h, r))
        boxes.append(bb)
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    aw, ah = x1 - x0 + 1, y1 - y0 + 1
    canvas = int(round(max(aw, ah) / FILL))
    for (w, h, r), (src, dst) in zip(imgs, pairs):
        art = crop(w, h, r, x0, y0, aw, ah)
        P.write(os.path.join(OUT, dst + ".png"), canvas, canvas,
                centre(aw, ah, art, canvas))
    print("  弓 4 张：并集框 %dx%d（原画布 %dx%d）-> %dx%d 画布，填充率 %d%%，未重采样"
          % (aw, ah, imgs[0][0], imgs[0][1], canvas, canvas,
             round(100.0 * max(aw, ah) / canvas)))
    return len(pairs)


def do_single(src, dst, canvas):
    p = os.path.join(SRC, src + ".png")
    if not os.path.isfile(p):
        print("  缺 %s.png，跳过" % src)
        return 0
    w, h, r = P.read(p)
    bb = P.bbox(w, h, r)
    P.write(os.path.join(OUT, dst + ".png"), canvas, canvas,
            P.paste_fit(w, h, r, canvas, FILL))
    print("  %s：%dx%d（内容 %dx%d）-> %dx%d 正方画布"
          % (dst, w, h, bb[2] - bb[0] + 1, bb[3] - bb[1] + 1, canvas, canvas))
    return 1


def main():
    if not os.path.isdir(SRC):
        print("import_art: 找不到原图目录 %s，跳过" % SRC)
        return
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    n = do_series(BOW)
    for src, dst, canvas in SINGLE:
        n += do_single(src, dst, canvas)
    print("import_art: %d 张" % n)


if __name__ == "__main__":
    main()
