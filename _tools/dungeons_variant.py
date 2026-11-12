# -*- coding: utf-8 -*-
"""给 display_mob 生成器换上「原作模型」变体（dungeons_models.py 的产物）。

    import dungeons_variant
    dungeons_variant.apply(MOB)          # 在 build() 之前

环境变量 <KEY>_MODEL=legacy 退回原来的手工模型；默认（或 =dungeons）用
_tools/<key>_dungeons_ref/ 里从本体提取的模型。换掉的是模型、部件、发光、
缩放和动作来源；动作名不变，所以技能钩子照常工作。

音效时刻：旧 cues 写的是旧动作里的秒数，这里按新旧动作长度等比换算，
先后顺序不变；之后再按原作事件逐个精调（model_config.json 的 notifies）。
"""

import json
import os

import display_mob as dm

HERE = os.path.dirname(os.path.abspath(__file__))


def choice(key):
    return os.environ.get(key.upper() + "_MODEL", "dungeons").lower()


def ref_dir(key):
    return os.path.join(HERE, key + "_dungeons_ref")


def available(key):
    return os.path.exists(os.path.join(ref_dir(key), key + ".bbmodel"))


def fold(mob, parts, merge):
    """Fold small parts (eyes, brows, nose) into another part's display: fewer entities.

    The merged part is rooted at the lowest common ancestor of the target's root and the folded bones
    (in Dungeons rigs the face bones are siblings of Head under J_Head).  Only where the item model can
    hold it (display_mob.part_model): every bone strictly between that root and a member has no rest
    rotation, a member has a rest rotation on one axis of at most 45 degrees, and the new chain from
    the root down to the target's old root is not animated (otherwise its motion would be lost).
    The folded bones' own motion relative to the root is dropped: eyes and brows stop moving on
    their own, which is the price of the fold.  Anything else stays a part of its own."""
    if not merge:
        return parts
    bones, _png, _res = dm.load_bbmodel(mob)
    clips = dm.load_animations(mob)
    animated = {b for clip in clips.values() for (b, _ch), keys in clip["tracks"].items()
                if any(abs(v) > 1e-2 for _t, value, *_rest in keys for v in value)}   # 0.01 degree / unit
    rows = {p["name"]: p for p in parts}

    def fits(root, members):
        for b in members:
            chain = dm.chain(bones, b)
            if root not in chain:
                return False
            if b == root or not bones[b]["cubes"]:
                continue
            # the whole chain below the root must come to nothing (rotations that cancel, as the
            # J_* joints and their mesh bones do) or to the member's own one-axis turn of <= 45
            rel = dm.bone_matrix(bones, b, stop=root)
            if max(abs(rel[i][j] - (i == j)) for i in range(4) for j in range(4)) < 1e-6:
                continue
            rot = [v for v in bones[b]["rotation"] if abs(v) > 1e-6]
            if len(rot) > 1 or (rot and abs(rot[0]) > 45 + 1e-3):
                return False
            if any(abs(v) > 1e-6 for n in chain[chain.index(root) + 1:-1] for v in bones[n]["rotation"]):
                return False
        return True

    for target, names in merge.items():
        if target not in rows:
            continue
        for name in names:
            row = rows.get(name)
            if row is None:
                continue
            old_root = rows[target]["bones"][0]
            a, b = dm.chain(bones, old_root), dm.chain(bones, row["bones"][0])
            k = 0
            while k < min(len(a), len(b)) and a[k] == b[k]:
                k += 1
            if k == 0:
                print("%s: %s stays a part of its own (no common bone with %s)" % (mob.key, name, target))
                continue
            root = a[k - 1]
            lift = a[k:]                       # bones from the new root down to the old root
            members = [root] * (root != old_root) + lift[:-1] + rows[target]["bones"] + b[k:-1] + row["bones"]
            members = list(dict.fromkeys(members))
            if any(n in animated for n in lift) or not fits(root, members):
                print("%s: %s stays a part of its own (cannot fold into %s)" % (mob.key, name, target))
                continue
            rows[target]["bones"] = members
            del rows[name]
    return [p for p in parts if p["name"] in rows]


def apply(mob, extra_glow=()):
    """Point `mob` at the extracted model. Returns True when the variant is in use."""
    if choice(mob.key) == "legacy" or not available(mob.key):
        return False
    ref = ref_dir(mob.key)
    old_lengths = {}
    try:
        old_lengths = {name: clip["length"] for name, clip in dm.load_animations(mob).items()}
    except Exception:       # noqa: BLE001 - the legacy rig may borrow clips from elsewhere
        pass
    cfg = json.load(open(os.path.join(ref, "model_config.json"), encoding="utf-8"))
    parts = json.load(open(os.path.join(ref, "parts.json"), encoding="utf-8"))
    mob.bbmodel = os.path.join(ref, mob.key + ".bbmodel")
    mob.anim_from = None
    parts = fold(mob, parts, cfg.get("merge", {}))
    mob.parts = [(p["name"], p["bones"]) for p in parts]
    if mob.held:
        # the carrier's own item, held at the original's weapon socket (display_mob.held_matrix)
        if not cfg.get("held_bone"):
            raise SystemExit("%s: the extracted model names no held_bone for the held item" % mob.key)
        mob.parts.append((mob.held, [cfg["held_bone"]]))
        mob.held_ref = ("idle", 0.0)
        # display_mob draws a held item at model_scale x vanilla size; the extracted rigs use tiny
        # units (a large model_scale), so keep the item the size the hand-built model gave it
        mob.held_size = mob.model_scale / cfg["model_scale"]
    mob.glow = set(json.load(open(os.path.join(ref, "glow_bones.json"), encoding="utf-8"))) | set(extra_glow)
    mob.face_rotation = True
    mob.model_scale = cfg["model_scale"]
    mob.turn = cfg.get("turn", 0)
    new_lengths = {c["clip"]: c["seconds"] for c in cfg["clips"]}
    if mob.cues:
        scaled = {}
        for clip, cues in mob.cues.items():
            k = new_lengths.get(clip, 0) / old_lengths[clip] if old_lengths.get(clip) else 1.0
            scaled[clip] = [(round(t * k, 3),) + tuple(rest) for t, *rest in cues]
        mob.cues = scaled
    mob.dungeons_variant = cfg
    return True
