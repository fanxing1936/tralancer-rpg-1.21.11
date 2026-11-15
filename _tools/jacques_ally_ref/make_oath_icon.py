# -*- coding: utf-8 -*-
"""One-off: the 32×32 item sprite of 圣殿誓约 from the original Dungeons Wind Horn (SM_WindHorn + T_Windhorn).

    python jacques_ally_ref/make_oath_icon.py [yaw pitch roll] [--sheet]

The Wind Horn is a box mesh painted with a 32×32 pixel texture, so the sprite is a render of the real mesh, not a
redraw: the texture's flat colours are swapped texel by texel for the Templar palette (ivory horn, gold mouthpiece,
Templar-red bands and strap), the mesh is projected orthographically at the angle of the original inventory icon,
rasterised 8× and each sprite pixel takes the colour most of its samples saw (no blending, so edges stay pixel-crisp).
Faces get three flat light levels by facing; a dark outline closes the silhouette like vanilla items.
Output: jacques_ally_ref/oath.png (copied into the resource pack by add_jacques_ally.py).
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from dungeons_conversion.generic import load_static  # noqa: E402

SRC = "D:/agent/dungeons_extract/upgrade/oath/assets/Dungeons/Content/Actors/Items/WindHorn/"
N, SS = 32, 8


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# original texel colour -> Templar colour
GREY = {149: "#FFF6DC", 140: "#F3E7C6", 132: "#E6D6AE", 126: "#DCC898", 119: "#CDB27E", 100: "#B0905A", 85: "#8C6C3A",
        69: "#E0B848", 52: "#B8902F", 51: "#B8902F", 48: "#9C7A2E", 35: "#6A4A18", 34: "#6A4A18", 21: "#3A2414", 0: "#2A1A10"}
BLUE = {(48, 102, 173): "#C8102E", (41, 88, 149): "#A80E26", (40, 85, 144): "#9A0C22", (35, 73, 124): "#6E0A18"}
OUTLINE = (40, 24, 14, 255)


def recolour(tex):
    out = tex.copy()
    for y in range(tex.shape[0]):
        for x in range(tex.shape[1]):
            r, g, b, a = tex[y, x]
            if a == 0:
                continue
            if (r, g, b) in BLUE:
                out[y, x, :3] = hexc(BLUE[(r, g, b)])
            elif r == g == b:
                k = min(GREY, key=lambda v: abs(v - r))
                out[y, x, :3] = hexc(GREY[k])
    return out


def rot(yaw, pitch, roll):
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    ry = np.array([[cr, 0, sr], [0, 1, 0], [-sr, 0, cr]])
    return ry @ rx @ rz


def render(yaw, pitch, roll, tex):
    m = load_static(SRC + "SM_WindHorn.glb")
    v = m["vertices_ue_cm"] @ rot(yaw, pitch, roll).T     # view space: x right, y depth (into screen), z up
    uv, tris = m["uv"], m["triangles"]
    th, tw = tex.shape[:2]
    lo, hi = v[:, [0, 2]].min(0), v[:, [0, 2]].max(0)
    span = (hi - lo).max()
    R = N * SS
    scale = (N - 2) * SS / span
    off = np.array([R / 2, R / 2]) - (lo + hi) / 2 * scale
    sx = v[:, 0] * scale + off[0]
    sy = R - (v[:, 2] * scale + off[1])
    depth = v[:, 1]
    zbuf = np.full((R, R), np.inf)
    col = np.zeros((R, R, 4), dtype=np.uint8)
    light = np.array([-0.55, -0.45, 0.7])
    light /= np.linalg.norm(light)
    for t in tris:
        p = np.stack([sx[t], sy[t]], 1)
        e1, e2 = v[t[1]] - v[t[0]], v[t[2]] - v[t[0]]
        nrm = np.cross(e1, e2)
        if np.linalg.norm(nrm) == 0:
            continue
        nrm /= np.linalg.norm(nrm)
        if nrm[1] > 0:                                   # facing away (back-face cull; depth axis points into screen)
            nrm = -nrm
        lam = float(np.dot(nrm, light))
        shade = 1.0 if lam > 0.45 else 0.86 if lam > 0.0 else 0.72
        x0, y0 = np.floor(p.min(0)).astype(int)
        x1, y1 = np.ceil(p.max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, R - 1), min(y1, R - 1)
        d = (p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) + (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1])
        if abs(d) < 1e-9:
            continue
        ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        px, py = xs + 0.5, ys + 0.5
        w0 = ((p[1, 1] - p[2, 1]) * (px - p[2, 0]) + (p[2, 0] - p[1, 0]) * (py - p[2, 1])) / d
        w1 = ((p[2, 1] - p[0, 1]) * (px - p[2, 0]) + (p[0, 0] - p[2, 0]) * (py - p[2, 1])) / d
        w2 = 1 - w0 - w1
        inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not inside.any():
            continue
        z = w0 * depth[t[0]] + w1 * depth[t[1]] + w2 * depth[t[2]]
        u = w0 * uv[t[0], 0] + w1 * uv[t[1], 0] + w2 * uv[t[2], 0]
        w = w0 * uv[t[0], 1] + w1 * uv[t[1], 1] + w2 * uv[t[2], 1]
        tx = np.clip((u * tw).astype(int), 0, tw - 1)
        ty = np.clip((w * th).astype(int), 0, th - 1)
        texel = tex[ty, tx]
        ok = inside & (z < zbuf[ys, xs]) & (texel[..., 3] > 0)
        zbuf[ys[ok], xs[ok]] = z[ok]
        c = texel[ok].astype(float)
        c[:, :3] *= shade
        col[ys[ok], xs[ok]] = c.clip(0, 255).astype(np.uint8)
    # majority vote per sprite pixel
    out = np.zeros((N, N, 4), dtype=np.uint8)
    for y in range(N):
        for x in range(N):
            cell = col[y * SS:(y + 1) * SS, x * SS:(x + 1) * SS].reshape(-1, 4)
            solid = cell[cell[:, 3] > 0]
            if len(solid) < SS * SS * 0.4:
                continue
            keys, counts = np.unique(solid[:, :3], axis=0, return_counts=True)
            out[y, x, :3] = keys[counts.argmax()]
            out[y, x, 3] = 255
    a = out[..., 3] > 0
    edge = np.zeros_like(a)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        edge |= np.roll(np.roll(a, dy, 0), dx, 1)
    out[edge & ~a] = OUTLINE
    return out


def main():
    tex = recolour(np.array(Image.open(SRC + "T_Windhorn.png").convert("RGBA")))
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--sheet" in sys.argv:
        cells = []
        for yaw in (-150, -120, -60, -30, 30, 60, 120, 150):
            for pitch in (-25, 20):
                cells.append(((yaw, pitch, 0), render(yaw, pitch, 0, tex)))
        sheet = Image.new("RGBA", (8 * 140, 2 * 140), (70, 70, 80, 255))
        for i, (k, im) in enumerate(cells):
            sheet.alpha_composite(Image.fromarray(im).resize((128, 128), Image.NEAREST), ((i // 2) * 140 + 6, (i % 2) * 140 + 6))
        sheet.save(os.path.join(HERE, "oath_sheet.png"))
        print([k for k, _ in cells])
        return
    yaw, pitch, roll = (float(a) for a in (args or (-60, 20, 0)))
    Image.fromarray(render(yaw, pitch, roll, tex)).save(os.path.join(HERE, "oath.png"))
    print("oath.png written (yaw %g pitch %g roll %g)" % (yaw, pitch, roll))


if __name__ == "__main__":
    main()
