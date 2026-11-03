# -*- coding: utf-8 -*-
"""把 Bedrock 几何（*.geo.json + 贴图集）画成一张像素图，给宣传片的无实拍版当“模型展示”。

只做宣传片够用的那部分：骨骼父子链、骨骼/方块旋转、box UV 与逐面 UV、mirror、inflate；
正交投影 + 画家算法（按深度排序），面按原版的方向明暗压暗。贴图逐面用透视变换贴上，最近邻采样。

    img = render(geo_path, atlas_path, yaw=30, pitch=-10, px=12)
"""
import json
import math

import numpy as np
from PIL import Image

SHADE = {"up": 1.0, "down": 0.5, "north": 0.8, "south": 0.8, "east": 0.6, "west": 0.6}


def _rot(rx, ry, rz):
    rx, ry, rz = (math.radians(a) for a in (rx, ry, rz))
    X = np.array([[1, 0, 0], [0, math.cos(rx), -math.sin(rx)], [0, math.sin(rx), math.cos(rx)]])
    Y = np.array([[math.cos(ry), 0, math.sin(ry)], [0, 1, 0], [-math.sin(ry), 0, math.cos(ry)]])
    Z = np.array([[math.cos(rz), -math.sin(rz), 0], [math.sin(rz), math.cos(rz), 0], [0, 0, 1]])
    return Z @ Y @ X


def _box_uv(u, v, w, h, d):
    """Bedrock box UV 展开：每个面 → (u, v, 宽, 高)。"""
    return {"up": (u + d, v, w, d), "down": (u + d + w, v, w, d),
            "west": (u, v + d, d, h), "north": (u + d, v + d, w, h),
            "east": (u + d + w, v + d, d, h), "south": (u + 2 * d + w, v + d, w, h)}


def _faces(x0, y0, z0, x1, y1, z1):
    """每个面四角，按贴图的 左上、右上、右下、左下 排列（从面外侧看）。"""
    return {
        "north": [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        "south": [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        "east": [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
        "west": [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        "up": [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)],
        "down": [(x1, y0, z1), (x0, y0, z1), (x0, y0, z0), (x1, y0, z0)],
    }


def _persp_coeffs(dst, src):
    """PIL PERSPECTIVE 系数：输出坐标 dst → 输入坐标 src（各 4 点）。"""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def load(geo_path):
    g = json.load(open(geo_path, encoding="utf-8"))["minecraft:geometry"][0]
    return g, {b["name"]: b for b in g["bones"]}


def _bone_matrix(bones, name):
    """骨骼到模型空间：返回作用在点上的函数（含所有祖先的绕枢轴旋转）。"""
    chain = []
    b = bones.get(name)
    while b:
        chain.append(b)
        b = bones.get(b.get("parent"))

    def apply(p):
        p = np.array(p, float)
        for bone in chain:                     # 先子后父
            if bone.get("rotation"):
                piv = np.array(bone.get("pivot", [0, 0, 0]), float)
                p = _rot(*bone["rotation"]) @ (p - piv) + piv
        return p
    return apply


def render(geo_path, atlas_path, yaw=25.0, pitch=-12.0, px=12, scale_tex=8):
    g, bones = load(geo_path)
    atlas = Image.open(atlas_path).convert("RGBA")
    tw, th = g["description"]["texture_width"], g["description"]["texture_height"]
    sx, sy = atlas.width / tw, atlas.height / th
    view = _rot(pitch, 0, 0) @ _rot(0, yaw, 0)

    polys = []
    for b in g["bones"]:
        to_model = _bone_matrix(bones, b["name"])
        for c in b.get("cubes", []):
            (ox, oy, oz), (w, h, d) = c["origin"], c["size"]
            inf = c.get("inflate", 0)
            box = (ox - inf, oy - inf, oz - inf, ox + w + inf, oy + h + inf, oz + d + inf)
            uv = c.get("uv", [0, 0])
            if isinstance(uv, list):
                fuv = _box_uv(uv[0], uv[1], w, h, d)
                if c.get("mirror"):
                    fuv["east"], fuv["west"] = fuv["west"], fuv["east"]
                    fuv = {k: (u + uw, v, -uw, vh) for k, (u, v, uw, vh) in fuv.items()}
            else:
                fuv = {k: tuple(f["uv"]) + tuple(f["uv_size"]) for k, f in uv.items()}
            crot = c.get("rotation")
            cpiv = np.array(c.get("pivot", [0, 0, 0]), float)
            for face, corners in _faces(*box).items():
                if face not in fuv:
                    continue
                pts = []
                for p in corners:
                    p = np.array(p, float)
                    if crot:
                        p = _rot(*crot) @ (p - cpiv) + cpiv
                    p = to_model(p)
                    p[0] = -p[0]                      # Bedrock 的 X 与屏幕左右相反
                    pts.append(view @ p)
                pts = np.array(pts)
                n = np.cross(pts[1] - pts[0], pts[3] - pts[0])
                if n[2] >= -1e-6 and w and h and d:   # 背面剔除（片状方块两面都画）
                    continue
                polys.append((pts[:, 2].mean(), face, pts, fuv[face]))

    allp = np.concatenate([p[2] for p in polys])
    minx, maxx = allp[:, 0].min(), allp[:, 0].max()
    miny, maxy = allp[:, 1].min(), allp[:, 1].max()
    pad = 2
    W = int((maxx - minx) * px) + pad * 2
    H = int((maxy - miny) * px) + pad * 2
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _z, face, pts, (u, v, uw, vh) in sorted(polys, key=lambda q: -q[0]):
        scr = [((p[0] - minx) * px + pad, (maxy - p[1]) * px + pad) for p in pts]
        x0, y0 = int(min(s[0] for s in scr)), int(min(s[1] for s in scr))
        x1, y1 = int(math.ceil(max(s[0] for s in scr))), int(math.ceil(max(s[1] for s in scr)))
        if x1 - x0 < 1 or y1 - y0 < 1:
            continue
        # 贴图块（负尺寸 = 翻转），放大后再透视贴，边缘更干净
        l, r = sorted((u * sx, (u + uw) * sx))
        t, b = sorted((v * sy, (v + vh) * sy))
        tex = atlas.crop((int(l), int(t), max(int(l) + 1, int(round(r))), max(int(t) + 1, int(round(b)))))
        if uw < 0:
            tex = tex.transpose(Image.FLIP_LEFT_RIGHT)
        if vh < 0:
            tex = tex.transpose(Image.FLIP_TOP_BOTTOM)
        tex = tex.resize((tex.width * scale_tex, tex.height * scale_tex), Image.NEAREST)
        s = SHADE[face]
        if s < 1:
            arr = np.array(tex, float)
            arr[..., :3] *= s
            tex = Image.fromarray(arr.astype(np.uint8))
        src = [(0, 0), (tex.width, 0), (tex.width, tex.height), (0, tex.height)]
        dst = [(x - x0, y - y0) for x, y in scr]
        warped = tex.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, _persp_coeffs(dst, src), Image.NEAREST)
        # 只留四边形内部，避免透视外推出的杂边
        mask = Image.new("L", warped.size, 0)
        from PIL import ImageDraw
        ImageDraw.Draw(mask).polygon(dst, fill=255)
        a = Image.fromarray(np.minimum(np.array(warped.getchannel("A")), np.array(mask)))
        warped.putalpha(a)
        out.alpha_composite(warped, (x0, y0))
    return out
