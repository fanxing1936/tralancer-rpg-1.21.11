# -*- coding: utf-8 -*-
"""天使长米迦勒的模型（docs/MICHAEL-DESIGN.md）：方块版灵体 + 六翼 + 补充动作。

    python build_michael_model.py extract    # 一次：从 Codex 的六翼工程里取出翼（网格、贴图、每段动作的翼轨道）
    python build_michael_model.py            # 生成 _tools/michael_dungeons_ref/（LordLook 读这里）

来源：
  身体、霜冻甲、脊骨、双肋骨   _tools/michael_spirit_dungeons_ref/（convert_michael_spirit.py 的方块版，全身半透明）
  六翼                        用户批准的 D:\\agent\\codex\\TRA\\outputs\\michael_spirit_cohesive_wings_32\\ 两份 .bbmodel
                              （Blockbench 网格）。extract 把翼存进 _tools/michael_boss_ref/wings.json 和 wings.png，
                              之后不再依赖 Codex 的目录
  补充动作                    扫罗、雅克的模型（同一副 SK_Player_Master 骨架，静止姿势逐骨相同）：升空、落地、高举、
                              英雄姿势、单膝跪地、旋身、炫耀、眩晕、吹号、敲钟

翼的转换：每片翼（12 组：上中下 × 左右 × 翼根/翼尖）有一根翼骨（盒子）和一张翼膜（四边形），两者在翼组里都绕 X 轴
倾斜同一个角度。这里给每组加一个子组 <翼组>_geo，带上这个倾角，翼骨和翼膜在子组里就是轴对齐的方块（翼膜厚度 0）。
每个 _geo 组单独成一个显示部件（多轴旋转不能并进别的部件），正好给「六翼燃尽」逐片隐藏。
六翼工程的单位是这里的 model_scale 倍（J_Shoulders 20.691 对 2.76），位置和位移关键帧都除回来，旋转不变。
"""
import base64
import copy
import io
import json
import math
import os
import sys
import uuid as uuidlib

import numpy as np
from PIL import Image

import display_mob as D

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_REF = os.path.join(HERE, "michael_spirit_dungeons_ref")
OUT = os.path.join(HERE, "michael_dungeons_ref")
BOSS_REF = os.path.join(HERE, "michael_boss_ref")
CODEX = r"D:\agent\codex\TRA\outputs\michael_spirit_cohesive_wings_32"
WINGED = {"spine": "michael_spirit_cohesive_wings_32_spine.bbmodel",
          "rib": "michael_spirit_cohesive_wings_32_dual_rib.bbmodel"}
WING_ATLAS_AT = (0, 128)          # where the 32x32 feather texture goes in the 256x256 atlas

# 补充动作：新名 <- (来源模型, 来源动作名)
EXTRA = {
    "mighty": ("saul", "mighty"), "hero": ("saul", "hero"), "kneel": ("saul", "kneel"), "twirl": ("saul", "twirl"),
    "showoff": ("saul", "showoff"), "rise": ("saul", "vanish"), "land": ("saul", "land"), "stun": ("saul", "stun"),
    "horn": ("jacques", "horn"), "gong": ("jacques", "gong"),
}
FOLD_FROM = ("roll_f", 0.3)       # 六翼掩面：翻滚里翼往背后收拢的那一刻
FOLD_LEN = 2.0
MERGE = {
    "head": ["mouth", "l_eye_pupil", "l_eye_iris", "r_eye_pupil", "r_eye_iris", "michael_spirit_head_000",
             "michael_spirit_head_002", "michael_spirit_head_011", "michael_spirit_head_012"],
    "body": ["body_armor"], "l_arm": ["l_arm_armor"], "r_arm": ["r_arm_armor"],
    "l_leg": ["l_leg_armor"], "r_leg": ["r_leg_armor"],
}
# 六翼燃尽的顺序：一对一对烧（部件名前缀）
WINGS = ["wing_lower_left", "wing_lower_right", "wing_middle_left", "wing_middle_right", "wing_upper_left", "wing_upper_right"]

FACES = {   # Java face -> its 4 corners (0 = from, 1 = to per axis), top-left first, clockwise, seen from outside
    "north": [(1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0)],
    "south": [(0, 1, 1), (1, 1, 1), (1, 0, 1), (0, 0, 1)],
    "east": [(1, 1, 1), (1, 1, 0), (1, 0, 0), (1, 0, 1)],
    "west": [(0, 1, 0), (0, 1, 1), (0, 0, 1), (0, 0, 0)],
    "up": [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
    "down": [(0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 0, 0)],
}
# uv corner (0 = u0/v0, 1 = u1/v1) shown at corners c0..c3 for each face rotation (clockwise)
UV_AT = {0: [(0, 0), (1, 0), (1, 1), (0, 1)], 90: [(0, 1), (0, 0), (1, 0), (1, 1)],
         180: [(1, 1), (0, 1), (0, 0), (1, 0)], 270: [(1, 0), (1, 1), (0, 1), (0, 0)]}


def uid(seed):
    return str(uuidlib.uuid5(uuidlib.NAMESPACE_URL, "tralancer/michael/" + seed))


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write(path, doc, indent=1):
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=indent)
        fh.write("\n")


def png_of(tex):
    return Image.open(io.BytesIO(base64.b64decode(tex["source"].split(",", 1)[1]))).convert("RGBA")


# ---------------------------------------------------------------------------
# extract: Codex's mesh wings -> wings.json + wings.png
# ---------------------------------------------------------------------------

def outliner_parents(doc):
    names = {g["uuid"]: g["name"] for g in doc["groups"]}
    parent, members = {}, {}

    def walk(node, up):
        name = names[node["uuid"]]
        parent[name] = up
        for c in node.get("children", []):
            if isinstance(c, str):
                members.setdefault(name, []).append(c)
            else:
                walk(c, name)

    for n in doc["outliner"]:
        if not isinstance(n, str):
            walk(n, None)
    return parent, members


def extract():
    spine = read(os.path.join(CODEX, WINGED["spine"]))
    scale = read(os.path.join(SRC_REF, "model_config.json"))["model_scale"]
    groups = {g["name"]: g for g in spine["groups"]}
    k = groups["J_Shoulders"]["origin"][2] / 2.76
    if abs(k - scale) > 1e-3:
        raise SystemExit("the winged project is not model_scale (%.4f) times the cube model (%.4f)" % (k, scale))
    parent, members = outliner_parents(spine)
    elements = {e["uuid"]: e for e in spine["elements"]}
    tex = {t["uuid"]: i for i, t in enumerate(spine["textures"])}
    feather = next(t for t in spine["textures"] if t["name"].startswith("Angel_Feather"))
    fi = spine["textures"].index(feather)
    wings = []
    for name, g in groups.items():
        if not name.startswith("DragonWing_"):
            continue
        els = []
        for e_uuid in members.get(name, []):
            e = elements[e_uuid]
            if any(e["rotation"]) or any(e["origin"]):
                raise SystemExit("%s: element with its own origin/rotation" % e["name"])
            verts = {vk: [v / k for v in xyz] for vk, xyz in e["vertices"].items()}
            faces = []
            for f in e["faces"].values():
                ti = f.get("texture")
                ti = ti if isinstance(ti, int) else tex.get(ti)
                if ti != fi:
                    raise SystemExit("%s: a wing face not on the feather texture" % e["name"])
                faces.append({"vertices": f["vertices"], "uv": f["uv"]})
            els.append({"name": e["name"], "vertices": verts, "faces": faces})
        wings.append({"name": name, "parent": parent[name], "origin": [v / k for v in g["origin"]],
                      "rotation": g.get("rotation", [0, 0, 0]), "elements": els})
    # every clip's wing tracks, both projects (the spine project's copy of shared clips wins)
    tracks = {}
    for which in ("rib", "spine"):
        doc = spine if which == "spine" else read(os.path.join(CODEX, WINGED[which]))
        for a in doc["animations"]:
            clip = a["name"].split("animation.", 1)[-1]
            rows = {}
            for an in a["animators"].values():
                if not an["name"].startswith("DragonWing_"):
                    continue
                keys = []
                for kf in an["keyframes"]:
                    p = kf["data_points"][0]
                    val = [float(p[c]) for c in "xyz"]
                    if kf["channel"] == "position":
                        val = [v / k for v in val]
                    keys.append({"channel": kf["channel"], "time": kf["time"], "value": val,
                                 "interpolation": kf["interpolation"]})
                rows[an["name"]] = keys
            tracks[clip] = {"length": a["length"], "loop": a["loop"], "wings": rows}
    os.makedirs(BOSS_REF, exist_ok=True)
    png_of(feather).save(os.path.join(BOSS_REF, "wings.png"))
    write(os.path.join(BOSS_REF, "wings.json"), {"source": CODEX, "scale_divided_by": k, "wings": wings,
                                                 "tracks": tracks}, indent=None)
    print("extracted %d wing groups, %d clips of wing tracks" % (len(wings), len(tracks)))


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def rot_x(deg):
    a = math.radians(deg)
    return np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])


def tilt_of(wing):
    """The X-axis turn that makes the membrane (and the spar) axis-aligned in the wing's frame."""
    mem = next(e for e in wing["elements"] if e["name"].endswith("membrane"))
    V = np.array(list(mem["vertices"].values()))
    n = np.linalg.svd(V - V.mean(0))[2][2]
    best = None
    for target in ((0, 1, 0), (0, 0, 1)):
        base = math.degrees(math.atan2(n[2], n[1])) - math.degrees(math.atan2(target[2], target[1]))
        for phi in (base, base + 180, base - 180):
            phi = (phi + 180) % 360 - 180
            if best is None or abs(phi) < abs(best):
                best = phi
    # local = Rx(-phi) world: the normal must land on an axis
    nl = rot_x(-best) @ n
    if max(abs(nl)) < 1 - 1e-4:
        raise SystemExit("%s: the membrane does not tilt about X alone" % wing["name"])
    return best


def cube_from_mesh(e, origin, phi, uv_off, res_scale):
    """Mesh element (in the wing frame, unrotated) -> one Blockbench cube in the tilted _geo frame."""
    o = np.array(origin)
    R = rot_x(-phi)
    local = {vk: R @ (np.array(v) - o) + o for vk, v in e["vertices"].items()}
    P = np.array(list(local.values()))
    lo, hi = P.min(0), P.max(0)
    for ax in range(3):         # every vertex sits on the box's from or to on every axis
        vals = P[:, ax]
        if not np.all(np.minimum(abs(vals - lo[ax]), abs(vals - hi[ax])) < 1e-4):
            raise SystemExit("%s: not a box in its tilted frame" % e["name"])
    flat = [ax for ax in range(3) if hi[ax] - lo[ax] < 1e-5]
    uv_of = {}
    for f in e["faces"]:
        for vk in f["vertices"]:
            uv_of.setdefault(vk, f["uv"][vk])
    pos_uv = [(local[vk], uv_of[vk]) for vk in local]

    def uv_at(corner):
        q = np.array([lo[a] if corner[a] == 0 else hi[a] for a in range(3)])
        d = [np.linalg.norm(p - q) for p, _ in pos_uv]
        i = int(np.argmin(d))
        return pos_uv[i][1] if d[i] < 1e-4 else None

    faces = {}
    for face, corners in FACES.items():
        normal_axis = {"north": 2, "south": 2, "east": 0, "west": 0, "up": 1, "down": 1}[face]
        if flat and normal_axis not in flat:
            continue                       # a membrane only has its two big faces
        uvs = [uv_at(c) for c in corners]
        if any(u is None for u in uvs):
            continue
        done = None
        for r, at in UV_AT.items():
            # solve u0,u1,v0,v1 from the corners, then check all four agree
            U, V = {}, {}
            ok = True
            for (iu, iv), (u, v) in zip(at, uvs):
                for store, key, val in ((U, iu, u), (V, iv, v)):
                    if key in store and abs(store[key] - val) > 1e-4:
                        ok = False
                    store[key] = val
            if ok and len(U) == 2 and len(V) == 2:
                done = (r, U, V)
                break
        if done is None:
            raise SystemExit("%s %s: the UVs are not a rectangle" % (e["name"], face))
        r, U, V = done
        faces[face] = {"uv": [(U[0] + uv_off[0]) * res_scale, (V[0] + uv_off[1]) * res_scale,
                              (U[1] + uv_off[0]) * res_scale, (V[1] + uv_off[1]) * res_scale],
                       "texture": 0, **({"rotation": r} if r else {})}
    if not faces:
        raise SystemExit("%s: no faces" % e["name"])
    return {"name": e["name"], "box_uv": False, "rescale": False, "locked": False, "render_order": "default",
            "allow_mirror_modeling": True, "from": [round(v, 6) for v in lo], "to": [round(v, 6) for v in hi],
            "autouv": 0, "color": 0, "origin": [round(v, 6) for v in origin], "faces": faces,
            "type": "cube", "uuid": uid("el/" + e["name"])}


def find_node(outliner, uuid):
    for n in outliner:
        if isinstance(n, str):
            continue
        if n["uuid"] == uuid:
            return n
        r = find_node(n.get("children", []), uuid)
        if r:
            return r
    return None


def keyframe(name, clip, kf, i):
    return {"channel": kf["channel"], "data_points": [{c: v for c, v in zip("xyz", kf["value"])}],
            "uuid": uid("kf/%s/%s/%d" % (clip, name, i)), "time": kf["time"], "color": -1,
            "interpolation": kf["interpolation"]}


def wing_animators(wing_uuid, tracks, clip, length):
    """Wing animators for `clip`: its own wing tracks, or the wing_flap loop repeated over `length`."""
    own = tracks.get(clip)
    out = {}
    if own:
        rows = own["wings"]
    else:
        flap = tracks["wing_flap"]
        rows = {}
        for name, keys in flap["wings"].items():
            rep = []
            n = 0
            while n * flap["length"] < length + 1e-6:
                for kf in keys:
                    t = kf["time"] + n * flap["length"]
                    if t <= length + 1e-6 and not (n and kf["time"] == 0):
                        rep.append(dict(kf, time=round(t, 4)))
                n += 1
            rows[name] = rep
    for name, keys in rows.items():
        out[wing_uuid[name]] = {"name": name, "type": "bone", "rotation_global": False,
                                "quaternion_interpolation": False,
                                "keyframes": [keyframe(name, clip, kf, i) for i, kf in enumerate(keys)]}
    return out


def build():
    data = read(os.path.join(BOSS_REF, "wings.json"))
    doc = read(os.path.join(SRC_REF, "michael_spirit.bbmodel"))
    cfg = read(os.path.join(SRC_REF, "model_config.json"))
    parts = read(os.path.join(SRC_REF, "parts.json"))
    res = doc["resolution"]["width"]
    groups = {g["name"]: g for g in doc["groups"]}

    # atlas: the feather texture goes into the free lower half
    atlas = png_of(doc["textures"][0])
    feather = Image.open(os.path.join(BOSS_REF, "wings.png")).convert("RGBA")
    if np.array(atlas)[WING_ATLAS_AT[1]:WING_ATLAS_AT[1] + feather.height,
                       WING_ATLAS_AT[0]:WING_ATLAS_AT[0] + feather.width, 3].any():
        raise SystemExit("the atlas is not free where the wings go")
    atlas.paste(feather, WING_ATLAS_AT)
    buf = io.BytesIO()
    atlas.save(buf, "PNG")
    doc["textures"][0]["source"] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    uv_scale = res / float(doc["textures"][0].get("uv_width", res))

    # wings: groups + a tilted _geo child per group carrying the cubes
    wing_uuid = {}
    new_parts = []
    for w in data["wings"]:
        phi = tilt_of(w)
        g_uuid, geo_uuid = uid("g/" + w["name"]), uid("g/" + w["name"] + "_geo")
        wing_uuid[w["name"]] = g_uuid
        short = "wing_" + w["name"][len("DragonWing_"):]
        doc["groups"].append({"name": w["name"], "origin": w["origin"], "rotation": w["rotation"], "color": 0,
                              "export": True, "mirror_uv": False, "isOpen": False, "locked": False, "visibility": True,
                              "autouv": 0, "uuid": g_uuid})
        doc["groups"].append({"name": short, "origin": w["origin"], "rotation": [phi, 0, 0], "color": 0,
                              "export": True, "mirror_uv": False, "isOpen": False, "locked": False, "visibility": True,
                              "autouv": 0, "uuid": geo_uuid})
        cubes = [cube_from_mesh(e, w["origin"], phi, WING_ATLAS_AT, uv_scale) for e in w["elements"]]
        doc["elements"] += cubes
        parent = find_node(doc["outliner"], groups[w["parent"]]["uuid"]) if w["parent"] in groups else None
        if parent is None:
            parent = find_node(doc["outliner"], wing_uuid.get(w["parent"]))
        if parent is None:
            raise SystemExit("%s: parent %s not found" % (w["name"], w["parent"]))
        parent["children"].append({"uuid": g_uuid, "isOpen": False,
                                   "children": [{"uuid": geo_uuid, "isOpen": False,
                                                 "children": [c["uuid"] for c in cubes]}]})
        new_parts.append({"name": short, "bones": [short]})

    # clips: wing tracks into the existing clips, then the extra clips from Saul / Jacques
    tracks = data["tracks"]
    for a in doc["animations"]:
        clip = a["name"].split("animation.", 1)[-1]
        a["animators"].update(wing_animators(wing_uuid, tracks, clip, a["length"]))
    name_uuid = {g["name"]: g["uuid"] for g in doc["groups"]}
    sources = {}
    clip_rows = list(cfg["clips"])
    for new, (src_key, src_clip) in EXTRA.items():
        if src_key not in sources:
            sources[src_key] = read(os.path.join(HERE, "%s_dungeons_ref" % src_key, src_key + ".bbmodel"))
        src = sources[src_key]
        src_names = {g["uuid"]: g["name"] for g in src["groups"]}
        a = next(x for x in src["animations"] if x["name"].split("animation.", 1)[-1] == src_clip)
        b = copy.deepcopy(a)
        b["name"], b["uuid"] = "animation." + new, uid("anim/" + new)
        b["animators"] = {}
        for an_uuid, an in a["animators"].items():
            nm = src_names.get(an_uuid, an.get("name"))
            if nm in name_uuid and not nm.startswith("DragonWing_"):
                b["animators"][name_uuid[nm]] = copy.deepcopy(an)
        b["animators"].update(wing_animators(wing_uuid, tracks, new, b["length"]))
        doc["animations"].append(b)
        clip_rows.append({"clip": new, "source": "%s:%s" % (src_key, src_clip), "seconds": b["length"],
                          "loop": b["loop"] == "loop"})

    # fold: idle body, wings held where they gather in the forward roll
    idle = next(x for x in doc["animations"] if x["name"] == "animation.idle")
    fold = copy.deepcopy(idle)
    fold["name"], fold["uuid"], fold["length"], fold["loop"] = "animation.fold", uid("anim/fold"), FOLD_LEN, "hold"
    roll_doc = next(x for x in doc["animations"] if x["name"] == "animation." + FOLD_FROM[0])
    for an_uuid, an in roll_doc["animators"].items():
        if not an["name"].startswith("DragonWing_"):
            continue
        rows = {}
        for kf in an["keyframes"]:
            rows.setdefault(kf["channel"], []).append(
                (kf["time"], [float(kf["data_points"][0][c]) for c in "xyz"], kf["interpolation"]))
        keys = []
        for ch, row in rows.items():
            row.sort(key=lambda r: r[0])
            val = D.track_value(row, FOLD_FROM[1], False)
            for i, t in enumerate((0.0, FOLD_LEN)):
                keys.append({"channel": ch, "data_points": [{c: v for c, v in zip("xyz", val)}],
                             "uuid": uid("kf/fold/%s/%s/%d" % (an["name"], ch, i)), "time": t, "color": -1,
                             "interpolation": "linear"})
        fold["animators"][an_uuid] = dict(an, keyframes=keys)
    doc["animations"].append(fold)
    clip_rows.append({"clip": "fold", "source": "idle + roll_f wings at %.2fs" % FOLD_FROM[1], "seconds": FOLD_LEN,
                      "loop": False})

    doc["name"] = "michael"
    os.makedirs(OUT, exist_ok=True)
    write(os.path.join(OUT, "michael.bbmodel"), doc)
    atlas.save(os.path.join(OUT, "atlas.png"))
    write(os.path.join(OUT, "parts.json"), parts + new_parts)
    write(os.path.join(OUT, "glow_bones.json"), [])
    cfg = dict(cfg, merge=MERGE, clips=clip_rows, wings=WINGS,
               wing_parts={w: [p["name"] for p in new_parts if p["name"].startswith(w)] for w in WINGS})
    write(os.path.join(OUT, "model_config.json"), cfg)
    with io.open(os.path.join(OUT, "SOURCES.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# 来源\n\n由 `_tools/build_michael_model.py` 生成，不要手改。\n\n"
                 "- 身体、霜冻甲、脊骨、双肋骨：`_tools/michael_spirit_dungeons_ref/`（见那里的 SOURCES.md）\n"
                 "- 六翼：用户批准的 Codex 工程 `michael_spirit_cohesive_wings_32`，存于 `_tools/michael_boss_ref/wings.json`、`wings.png`\n"
                 "- 补充动作：%s\n" % "、".join("`%s`←%s:%s" % (n, s, c) for n, (s, c) in EXTRA.items()))
    print("michael: %d groups, %d elements, %d parts (+%d wings), %d clips"
          % (len(doc["groups"]), len(doc["elements"]), len(parts) + len(new_parts), len(new_parts), len(doc["animations"])))


if __name__ == "__main__":
    if sys.argv[1:] == ["extract"]:
        extract()
    else:
        build()
