# -*- coding: utf-8 -*-
"""图鉴渲染的后备：不经 Blockbench 的小软件渲染器（Blockbench MCP 连不上时用）。

    python guide_renders/soft_render.py          # 在 _tools 下运行；然后 python guide_renders/make_web.py

画 .bbmodel 的静止姿势（或某段动作的一帧）：所有面按远近从后往前叠，半透明照算，背景透明。
贴图可以换成资源包里调过色的图集，和游戏里一致。米迦勒（两段）和守望者的图鉴图就是它画的。
"""
import base64
import io
import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import display_mob as D  # noqa: E402

RP = os.path.join(TOOLS, "..", "resourcepack", "assets", "rpg", "textures", "item")
# 名字: (.bbmodel, 换用的图集（资源包里）, 藏掉的骨（名字里含这些字的）, 动作与时刻, 朝向)
JOBS = {
    "michael": ("michael_dungeons_ref/michael.bbmodel", "michael/atlas.png", ("rib",), ("idle", 0.0), 200),
    "michael_s2": ("michael_dungeons_ref/michael.bbmodel", "michael/atlas.png", ("spine",), ("rib_idle", 0.0), 200),
    "watchling": ("watchling_dungeons_ref/watchling.bbmodel", "watchling/atlas.png", (), ("idle", 0.0), 200),
}

FACES = {
    "north": [(1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0)],
    "south": [(0, 1, 1), (1, 1, 1), (1, 0, 1), (0, 0, 1)],
    "east": [(1, 1, 1), (1, 1, 0), (1, 0, 0), (1, 0, 1)],
    "west": [(0, 1, 0), (0, 1, 1), (0, 0, 1), (0, 0, 0)],
    "up": [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
    "down": [(0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 0, 0)],
}
UV_AT = {0: [(0, 0), (1, 0), (1, 1), (0, 1)], 90: [(0, 1), (0, 0), (1, 0), (1, 1)],
         180: [(1, 1), (0, 1), (0, 0), (1, 0)], 270: [(1, 0), (1, 1), (0, 1), (0, 0)]}
SHADE = {"up": 1.0, "down": 0.5, "north": 0.8, "south": 0.8, "east": 0.6, "west": 0.6}


class _Mob:
    def __init__(self, path):
        self.bbmodel, self.anim_from, self.key = path, None, "soft"


def render(path, out, tex=None, hide=(), pose=None, yaw=200, size=900, pitch=12):
    doc = json.load(io.open(path, encoding="utf-8"))
    if tex:
        texs = [np.array(Image.open(tex).convert("RGBA")).astype(float) / 255.0]
    else:
        texs = [np.array(Image.open(io.BytesIO(base64.b64decode(t["source"].split(",", 1)[1]))).convert("RGBA")).astype(float) / 255.0
                for t in doc["textures"]]
    mob = _Mob(path)
    bones, _, res = D.load_bbmodel(mob)
    clips = D.load_animations(mob) if pose else {}
    rw, rh = res["width"], res["height"]
    polys = []
    for name, b in bones.items():
        if any(h in name for h in hide):
            continue
        W = np.array(D.posed_matrix(bones, name, clips[pose[0]], pose[1]) if pose else D.bone_matrix(bones, name))
        for c in b["cubes"]:
            f, to = c["from"], c["to"]
            R = np.array(D.about(c.get("origin", [0, 0, 0]), c["rotation"])) if any(c.get("rotation", [0, 0, 0])) else np.eye(4)
            for face, data in c["faces"].items():
                if data.get("texture") is None:
                    continue
                ti = data["texture"] if isinstance(data["texture"], int) else 0
                ti = min(ti, len(texs) - 1)
                corners = [(W @ R @ np.array([f[k] if s[k] == 0 else to[k] for k in range(3)] + [1.0]))[:3] for s in FACES[face]]
                u0, v0, u1, v1 = data["uv"]
                cuv = [((u0, u1)[a], (v0, v1)[b_]) for a, b_ in UV_AT[int(data.get("rotation", 0)) % 360]]
                polys.append((np.array(corners), cuv, ti, SHADE[face]))
    allp = np.concatenate([p[0] for p in polys])
    center, span = (allp.min(0) + allp.max(0)) / 2, (allp.max(0) - allp.min(0)).max()
    a, p_ = math.radians(yaw), math.radians(pitch)
    V = (np.array([[1, 0, 0], [0, math.cos(p_), -math.sin(p_)], [0, math.sin(p_), math.cos(p_)]])
         @ np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]]))
    scale = size * 0.9 / span
    rgb, alpha = np.zeros((size, size, 3)), np.zeros((size, size))
    items = sorted(((((c - center) @ V.T)[:, 2].mean(), (c - center) @ V.T, uv, ti, sh) for c, uv, ti, sh in polys), key=lambda x: x[0])
    for _, pc, uv, ti, sh in items:
        sx, sy = size / 2 + pc[:, 0] * scale, size / 2 - pc[:, 1] * scale
        P0, P1, P3 = np.array([sx[0], sy[0]]), np.array([sx[1], sy[1]]), np.array([sx[3], sy[3]])
        A = np.column_stack([P1 - P0, P3 - P0])
        if abs(np.linalg.det(A)) < 1e-6:
            continue
        Ai = np.linalg.inv(A)
        x0, x1 = int(max(0, min(sx))), int(min(size - 1, max(sx)) + 1)
        y0, y1 = int(max(0, min(sy))), int(min(size - 1, max(sy)) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1) + .5, np.arange(y0, y1) + .5)
        d = np.stack([xs - P0[0], ys - P0[1]], -1) @ Ai.T
        s_, t_ = d[..., 0], d[..., 1]
        m = (s_ >= 0) & (s_ <= 1) & (t_ >= 0) & (t_ <= 1)
        if not m.any():
            continue
        tex = texs[ti]
        th, tw = tex.shape[:2]
        c0, c1, c3 = np.array(uv[0]), np.array(uv[1]), np.array(uv[3])
        u = (c0[0] + (c1[0] - c0[0]) * s_ + (c3[0] - c0[0]) * t_) * tw / rw
        v = (c0[1] + (c1[1] - c0[1]) * s_ + (c3[1] - c0[1]) * t_) * th / rh
        col = tex[np.clip(np.floor(v).astype(int), 0, th - 1), np.clip(np.floor(u).astype(int), 0, tw - 1)]
        al = col[..., 3] * m
        sub, sa = rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1]
        sub[:] = sub * (1 - al[..., None]) + col[..., :3] * sh * al[..., None]
        sa[:] = sa * (1 - al) + al
    out_im = np.dstack([np.where(alpha[..., None] > 0, rgb / np.maximum(alpha[..., None], 1e-6), 0), alpha])
    Image.fromarray((out_im.clip(0, 1) * 255).astype(np.uint8), "RGBA").save(out)


def main():
    for name, (bb, tex, hide, pose, yaw) in JOBS.items():
        render(os.path.join(TOOLS, bb), os.path.join(HERE, name + ".png"), os.path.join(RP, tex), hide, pose, yaw)
        print("rendered", name)


if __name__ == "__main__":
    main()
