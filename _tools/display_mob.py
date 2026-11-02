# -*- coding: utf-8 -*-
"""Display-entity mobs: a Blockbench rig drawn by item_display passengers
riding an invisible carrier.  Shared by add_tower_guard.py (圣卫) and
add_beelzebub.py (别西卜); each of those owns its carrier and gameplay hooks,
this module owns the rig -> display maths, the baked animations and the
sound events.

Rig -> display maths
--------------------
The .bbmodel is in Java model space (Blockbench flips x and the rotation
signs when it imports Bedrock geometry): +y up, the mob faces -z.  Bones
are merged into rigid parts.  A part's elements are written relative to
its own bounding box so they stay inside the -16..32 limit, and its rest
placement goes into the display `transformation`.

An item display draws model point m at  T . R180 . (m - 8) / 16  in the
entity's frame: the renderer turns the item half a turn about y, and
yaw 0 faces +z.  Rig point c should land at  R180 . W . s c / 16 - h,
where W is the part's bone matrix (identity at rest), s the model scale
and h the height of the carrier's passenger seat.  So T = G . W . F^-1,
with F(c) = R180 . (c - K - 8) / 16 and G(r) = R180 . s r / 16 - h.

Glow: elements of a glow bone carry `light_emission: 15` inside their
part's model instead of a second, full-bright display.

Animations
----------
Clips are authored in the .bbmodel (Blockbench animation tab) and baked
here into per-part display transforms.  Checked against the live editor:
a keyframe's rotation is added to the bone's rest Euler angles as-is and
its position is added to the bone's offset as-is (no Bedrock sign flips
on the stored values).

Sounds
------
`Mob.sounds` maps an event (`rpg:<key>.<event>`) to source .ogg files in
the mob's reference folder.  Resource paths must be lowercase, so the
files are copied under lowercased names into `assets/rpg/sounds/<key>/`.
`Mob.cues` fires events from the baked frames, so a sound stays on the
frame it belongs to whenever the clips are re-timed.
"""

import base64
import io
import json
import math
import os
import shutil

NS = "rpg"
TICK = 0.05


# ---------------------------------------------------------------------------
# 4x4 affine helpers, row-major nested lists
# ---------------------------------------------------------------------------

def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def ident():
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def translate(x, y, z):
    m = ident()
    m[0][3], m[1][3], m[2][3] = x, y, z
    return m


def scale(s):
    m = ident()
    for i in range(3):
        m[i][i] = s
    return m


def rot_x(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]


def rot_y(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]


def rot_z(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def euler(rot):
    """Blockbench group rotation: three.js order ZYX, i.e. Rz . Ry . Rx."""
    x, y, z = rot or (0, 0, 0)
    return mat_mul(rot_z(z), mat_mul(rot_y(y), rot_x(x)))


def about(pivot, rot):
    px, py, pz = pivot
    return mat_mul(translate(px, py, pz), mat_mul(euler(rot), translate(-px, -py, -pz)))


def inverse_affine(m):
    r = [[m[i][j] for j in range(3)] for i in range(3)]
    det = (r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
           - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
           + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0]))
    inv = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            a = [[r[x][y] for y in range(3) if y != i] for x in range(3) if x != j]
            cof = a[0][0] * a[1][1] - a[0][1] * a[1][0]
            inv[i][j] = (-1) ** (i + j) * cof / det
    t = [-sum(inv[i][k] * m[k][3] for k in range(3)) for i in range(3)]
    return [inv[0] + [t[0]], inv[1] + [t[1]], inv[2] + [t[2]], [0.0, 0.0, 0.0, 1.0]]


R180 = rot_y(180)


# ---------------------------------------------------------------------------
# the mob description
# ---------------------------------------------------------------------------

class Mob(object):
    """Everything the shared pipeline needs to know about one mob.

    key        folder / model / sound namespace under rpg: (tower_guard)
    label      name used in generated comments (圣卫)
    generator  script name used in generated comments
    bbmodel    path of the Blockbench project
    parts      [(part, [bones])]; the first bone is the part's animated bone,
               the rest are rigid children merged into it
    glow       bones whose elements are full-bright
    seat       carrier passenger seat height, blocks
    tag        carrier tag; parts get `<tag>.part` and `<tag>.p.<part>`
    score      objective prefix (rpg_tg -> rpg_tg_anim, rpg_tg_t, ...)
    carrier    entity type of the carrier
    clips      [(clip, ticks between samples, loops)]; the index is the clip
               id in `<score>_anim`, idle and walk come first
    model_scale  visual scale of the rig on top of the carrier's own
    sounds     {event: ((zh subtitle, en subtitle), [source files], extra
               sounds.json fields per file)}
    cues       {clip: [(seconds, event, volume, pitch)]}: on that frame
    enter_cues {clip: [(event, volume, pitch)]}: once, when the clip starts
               (for loops, whose frame 0 repeats)
    hurt       event played when the carrier takes a hit
    death      event played where its parts are swept after it is removed
    ambient    (event, chance per tick) while alive
    on_death   extra lines for the death function (at the swept anchor part)
    on_hurt    extra lines for the hurt function (as the carrier)
    carrier    entity type of the carrier, or None when carriers of several
               types share the tag (selectors then go by tag alone)
    """

    def __init__(self, key, label, generator, bbmodel, parts, glow, seat, tag, score,
                 clips, carrier="minecraft:vindicator", model_scale=1.0,
                 sounds=None, sound_dir=None, cues=None, enter_cues=None,
                 hurt=None, death=None, ambient=None, on_death=(), on_hurt=()):
        self.key, self.label, self.generator = key, label, generator
        self.bbmodel, self.parts, self.glow = bbmodel, parts, set(glow)
        self.seat, self.tag, self.score, self.carrier = seat, tag, score, carrier
        self.clips, self.model_scale = clips, model_scale
        self.sounds, self.sound_dir, self.cues = sounds or {}, sound_dir, cues or {}
        self.enter_cues = enter_cues or {}
        self.hurt, self.death, self.ambient, self.on_death = hurt, death, ambient, list(on_death)
        self.on_hurt = list(on_hurt)
        self.carrier_sel = "type=%s,tag=%s" % (carrier, tag) if carrier else "tag=%s" % tag
        self.tex = "%s:item/%s/atlas" % (NS, key)
        self.fn = "%s:%s" % (NS, key)
        self.clip_score, self.t_score = score + "_anim", score + "_t"

    def paths(self, rp, dp):
        self.rp, self.dp = rp, dp
        self.func = os.path.join(dp, "data", NS, "function", self.key)
        self.anim = os.path.join(self.func, "anim")


# ---------------------------------------------------------------------------
# .bbmodel
# ---------------------------------------------------------------------------

def load_bbmodel(mob):
    with io.open(mob.bbmodel, encoding="utf-8") as fh:
        doc = json.load(fh)
    groups = {g["uuid"]: g for g in doc["groups"]}
    elements = {e["uuid"]: e for e in doc["elements"]}
    bones = {}          # name -> {pivot, rotation, parent, cubes}

    def walk(node, parent):
        g = groups[node["uuid"]]
        bones[g["name"]] = {"pivot": g["origin"], "rotation": g.get("rotation") or [0, 0, 0],
                            "parent": parent, "cubes": []}
        for child in node["children"]:
            if isinstance(child, str):
                bones[g["name"]]["cubes"].append(elements[child])
            else:
                walk(child, g["name"])

    for node in doc["outliner"]:
        walk(node, None)
    tex = doc["textures"][0]["source"]
    png = base64.b64decode(tex.split(",", 1)[1])
    return bones, png, doc["resolution"]


def chain(bones, name):
    out = []
    while name:
        out.append(name)
        name = bones[name]["parent"]
    return out[::-1]


def bone_matrix(bones, name, stop=None):
    """Rest matrix of `name` relative to ancestor `stop` (exclusive)."""
    m = ident()
    names = chain(bones, name)
    if stop:
        names = names[names.index(stop) + 1:]
    for n in names:
        b = bones[n]
        m = mat_mul(m, about(b["pivot"], b["rotation"]))
    return m


# ---------------------------------------------------------------------------
# Java item models
# ---------------------------------------------------------------------------

def part_model(mob, bones, part, members, res):
    root = members[0]
    raw = []             # (element, child bone matrix relative to root, glow)
    for name in members:
        rel = ident() if name == root else bone_matrix(bones, name, stop=root)
        for c in bones[name]["cubes"]:
            raw.append((c, rel, name in mob.glow))

    # bounding box (rest, root-bone space) -> offset K centring it on (8,8,8)
    lo, hi = [1e9] * 3, [-1e9] * 3
    for c, rel, _ in raw:
        inf = c.get("inflate", 0)
        for corner in range(8):
            p = [c["from"][i] - inf if not (corner >> i) & 1 else c["to"][i] + inf for i in range(3)]
            q = [sum(rel[i][k] * p[k] for k in range(3)) + rel[i][3] for i in range(3)]
            lo = [min(lo[i], q[i]) for i in range(3)]
            hi = [max(hi[i], q[i]) for i in range(3)]
    K = [(lo[i] + hi[i]) / 2 - 8 for i in range(3)]

    su, sv = 16.0 / res["width"], 16.0 / res["height"]
    elements = []
    for c, rel, glow in raw:
        inf = c.get("inflate", 0)
        f = [c["from"][i] - inf - K[i] for i in range(3)]
        t = [c["to"][i] + inf - K[i] for i in range(3)]
        for v in f + t:
            if not -16 <= v <= 32:
                raise SystemExit("%s: %s element out of -16..32 (%s)" % (mob.key, part, v))
        el = {"from": [round(v, 4) for v in f], "to": [round(v, 4) for v in t], "faces": {}}
        if rel != ident():
            # a merged child bone with its own rest rotation: one axis only
            b = next(n for n in members if c in bones[n]["cubes"])
            rx, ry, rz = bones[b]["rotation"]
            axis, ang = [(a, v) for a, v in zip("xyz", (rx, ry, rz)) if v][0]
            piv = [bones[b]["pivot"][i] - K[i] for i in range(3)]
            el["rotation"] = {"origin": [round(v, 4) for v in piv], "axis": axis, "angle": ang}
        if glow:
            el["light_emission"] = 15
            el["shade"] = False
        for face, data in c["faces"].items():
            if data.get("texture") is None:
                continue
            u0, v0, u1, v1 = data["uv"]
            el["faces"][face] = {"uv": [round(u0 * su, 4), round(v0 * sv, 4),
                                        round(u1 * su, 4), round(v1 * sv, 4)],
                                 "texture": "#0", "tintindex": 0}
        elements.append(el)
    model = {"textures": {"0": mob.tex, "particle": mob.tex}, "elements": elements}
    return model, K


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def wf(path, lines):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def display_matrix(mob, bones, part_bone, K, W=None):
    """T = G . W . F^-1 (see module docstring)."""
    W = W or bone_matrix(bones, part_bone)
    F = mat_mul(scale(1 / 16.0), mat_mul(R180, translate(-K[0] - 8, -K[1] - 8, -K[2] - 8)))
    G = mat_mul(translate(0, -mob.seat, 0), mat_mul(scale(mob.model_scale / 16.0), R180))
    return mat_mul(G, mat_mul(W, inverse_affine(F)))


# ---------------------------------------------------------------------------
# animations
# ---------------------------------------------------------------------------

def load_animations(mob):
    with io.open(mob.bbmodel, encoding="utf-8") as fh:
        doc = json.load(fh)
    names = {g["uuid"]: g["name"] for g in doc["groups"]}
    clips = {}
    for a in doc.get("animations", []):
        tracks = {}
        for uuid, an in a["animators"].items():
            for kf in an.get("keyframes", []):
                if kf["channel"] not in ("rotation", "position"):
                    raise SystemExit("%s: %s uses channel %s" % (mob.key, a["name"], kf["channel"]))
                if kf["interpolation"] not in ("linear", "catmullrom", "step"):
                    raise SystemExit("%s: %s uses %s keys" % (mob.key, a["name"], kf["interpolation"]))
                p = kf["data_points"][0]
                val = [float(p[k]) for k in "xyz"]         # raises on Molang
                tracks.setdefault((names[uuid], kf["channel"]), []).append(
                    (kf["time"], val, kf["interpolation"]))
        for keys in tracks.values():
            keys.sort(key=lambda k: k[0])
        clips[a["name"].split("animation.", 1)[-1]] = {"length": a["length"], "tracks": tracks,
                                                       "loop": a["loop"] == "loop"}
    return clips


def catmull_rom(t, p0, p1, p2, p3):
    v0, v1 = (p2 - p0) * 0.5, (p3 - p1) * 0.5
    return ((2 * p1 - 2 * p2 + v0 + v1) * t ** 3 + (-3 * p1 + 3 * p2 - 2 * v0 - v1) * t ** 2
            + v0 * t + p1)


def track_value(keys, time, loop=False):
    """Blockbench's keyframe interpolation for one channel.  In a looping
    clip a catmull-rom end segment takes its outer neighbour from the other
    end of the track (the last key doubles as the first)."""
    if time <= keys[0][0]:
        return keys[0][1]
    if time >= keys[-1][0]:
        return keys[-1][1]
    i = max(n for n in range(len(keys)) if keys[n][0] <= time)
    (t0, a, ia), (t1, b, ib) = keys[i], keys[i + 1]
    alpha = (time - t0) / (t1 - t0)
    if ia == "step":
        return a
    if "catmullrom" in (ia, ib):
        wrap = loop and len(keys) >= 3
        pa = keys[i - 1][1] if i > 0 else keys[-2][1] if wrap else a
        pb = keys[i + 2][1] if i + 2 < len(keys) else keys[1][1] if wrap else b
        return [catmull_rom(alpha, pa[k], a[k], b[k], pb[k]) for k in range(3)]
    return [a[k] + (b[k] - a[k]) * alpha for k in range(3)]


def posed_matrix(bones, name, clip, time):
    """World matrix of bone `name` at `time` into `clip`."""
    m = ident()
    for n in chain(bones, name):
        b = bones[n]
        rot = list(b["rotation"])
        off = [0.0, 0.0, 0.0]
        if (n, "rotation") in clip["tracks"]:
            r = track_value(clip["tracks"][(n, "rotation")], time, clip["loop"])
            rot = [rot[k] + r[k] for k in range(3)]
        if (n, "position") in clip["tracks"]:
            off = track_value(clip["tracks"][(n, "position")], time, clip["loop"])
        m = mat_mul(m, mat_mul(translate(*off), about(b["pivot"], rot)))
    return m


def quaternion(m):
    """Unit quaternion [x, y, z, w] of the rotation block of `m`."""
    tr = m[0][0] + m[1][1] + m[2][2]
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2
        q = [(m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s, 0.25 * s]
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        s = math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2
        q = [0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s]
    elif m[1][1] > m[2][2]:
        s = math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2
        q = [(m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s]
    else:
        s = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
        q = [(m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s, (m[1][0] - m[0][1]) / s]
    n = math.sqrt(sum(v * v for v in q))
    return [v / n for v in q]


def components(T, s, prev=None):
    """Display transform as (translation, left_rotation) at uniform scale s.
    Explicit components interpolate as a single slerp, where the game's
    own decomposition of a raw matrix is ambiguous from frame to frame.
    The quaternion keeps the sign of the previous sample."""
    R = [[T[i][j] / s for j in range(3)] + [0.0] for i in range(3)] if s != 1 else T
    q = quaternion(R)
    if prev and sum(a * b for a, b in zip(q, prev[1])) < 0:
        q = [-v for v in q]
    return [T[0][3], T[1][3], T[2][3]], q


def fl(vals):
    """SNBT float list in fixed notation (no exponents, no -0)."""
    out = []
    for v in vals:
        txt = ("%.5f" % v).rstrip("0").rstrip(".")
        out.append(("0" if txt in ("-0", "") else txt) + "f")
    return "[" + ",".join(out) + "]"


def snbt_components(mob, c):
    s = fl([mob.model_scale] * 3)
    return ("{translation:%s,left_rotation:%s,scale:%s,right_rotation:[0f,0f,0f,1f]}"
            % (fl(c[0]), fl(c[1]), s))


def bake(mob, bones, offsets, clips):
    """clip name -> list of frames; a frame maps part -> components."""
    baked = {}
    for name, step, loop in mob.clips:
        clip = clips.get(name)
        if clip is None:
            raise SystemExit("%s: no animation.%s in the .bbmodel" % (mob.key, name))
        ticks = int(round(clip["length"] / TICK))
        times = list(range(0, ticks, step)) if loop else list(range(0, ticks + 1, step))
        frames, prev = [], {}
        for t in times:
            frame = {}
            for part, members in mob.parts:
                T = display_matrix(mob, bones, members[0], offsets[part],
                                   posed_matrix(bones, members[0], clip, t * TICK))
                frame[part] = prev[part] = components(T, mob.model_scale, prev.get(part))
            frames.append((t, frame))
        baked[name] = {"ticks": ticks, "step": step, "loop": loop, "frames": frames}
    return baked


# ---------------------------------------------------------------------------
# sounds
# ---------------------------------------------------------------------------

def sound_id(mob, event):
    return "%s:%s.%s" % (NS, mob.key, event)


def playsound(mob, event, volume=1.0, pitch=1.0, radius=24):
    return ("playsound %s hostile @a[distance=..%d] ~ ~ ~ %s %s"
            % (sound_id(mob, event), radius, ("%g" % volume), ("%g" % pitch)))


def write_sounds(mob):
    """Copy the mob's .ogg files under lowercase names and merge its events
    into assets/rpg/sounds.json (other mobs' events are left alone)."""
    out = os.path.join(mob.rp, "assets", NS, "sounds", mob.key)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    path = os.path.join(mob.rp, "assets", NS, "sounds.json")
    doc = {}
    if os.path.isfile(path):
        with io.open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    prefix = mob.key + "."
    doc = {k: v for k, v in doc.items() if not k.startswith(prefix)}
    lang = {"zh_cn": {}, "en_us": {}}
    for event, (subtitle, files, extra) in sorted(mob.sounds.items()):
        entries = []
        for src in files:
            name = os.path.splitext(src)[0].lower().replace("-", "_")
            shutil.copyfile(os.path.join(mob.sound_dir, src), os.path.join(out, name + ".ogg"))
            entry = dict(extra, name="%s:%s/%s" % (NS, mob.key, name)) if extra else \
                "%s:%s/%s" % (NS, mob.key, name)
            entries.append(entry)
        key = "subtitles.%s.%s.%s" % (NS, mob.key, event)
        doc[prefix + event] = {"subtitle": key, "sounds": entries}
        lang["zh_cn"][key], lang["en_us"][key] = subtitle
    wj(path, dict(sorted(doc.items())))
    # subtitles, merged the same way (en_us is the fallback for other locales)
    sub = "subtitles.%s.%s." % (NS, mob.key)
    for code, keys in lang.items():
        lp = os.path.join(mob.rp, "assets", NS, "lang", code + ".json")
        ldoc = {}
        if os.path.isfile(lp):
            with io.open(lp, encoding="utf-8") as fh:
                ldoc = json.load(fh)
        ldoc = {k: v for k, v in ldoc.items() if not k.startswith(sub)}
        ldoc.update(keys)
        wj(lp, ldoc)


# ---------------------------------------------------------------------------
# data pack: animation state machine, follow, orphan cleanup
# ---------------------------------------------------------------------------

def passenger(mob, part, comp):
    return ('{id:"minecraft:item_display",Tags:["%s.part","%s.p.%s"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"%s:%s/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1.5f,transformation:%s}'
            % (mob.tag, mob.tag, part, NS, mob.key, part, snbt_components(mob, comp)))


def dispatch_tree(mob, path, fn, frames):
    """Score-range binary search over the sample ticks of one clip."""
    lines = []
    if len(frames) <= 4:
        for tick, target in frames:
            lines.append("execute if score @s %s matches %d run return run function %s"
                         % (mob.t_score, tick, target))
    else:
        half = len(frames) // 2
        lo, hi = frames[:half], frames[half:]
        lines.append("execute if score @s %s matches ..%d run return run function %s_a"
                     % (mob.t_score, lo[-1][0], fn))
        lines.append("function %s_b" % fn)
        dispatch_tree(mob, path + "_a", fn + "_a", lo)
        dispatch_tree(mob, path + "_b", fn + "_b", hi)
    wf(path + ".mcfunction", lines)


def cue_lines(mob, name, t, step):
    """Sounds cued in (t - step, t]: each lands on exactly one sample."""
    out = []
    for sec, event, volume, pitch in mob.cues.get(name, ()):
        at = int(round(sec / TICK))
        if t - step < at <= t or (at == 0 and t == 0):
            out.append("execute at @s run " + playsound(mob, event, volume, pitch))
    return out


def write_anim(mob, baked):
    ids = {name: i for i, (name, _, _) in enumerate(mob.clips)}
    S, T, sc, tg = mob.clip_score, mob.t_score, mob.score, mob.tag
    # both trees are owned by this generator; drop frames of renamed clips
    for d in (mob.anim, os.path.join(mob.func, "debug")):
        if os.path.isdir(d):
            shutil.rmtree(d)
    for name, clip in baked.items():
        d = os.path.join(mob.anim, name)
        fn = "%s/anim/%s" % (mob.fn, name)
        step = clip["step"]
        prev, leaves = None, []
        for k, (t, frame) in enumerate(clip["frames"]):
            lines = ["# %s 第 %d 刻的姿势（每 %d 刻一帧，补间 %d 刻）。由 %s 烘焙。"
                     % (name, t, step, step, mob.generator)]
            for part, _ in mob.parts:
                c = frame[part]
                # frame 0 may follow any clip, so it sets every part
                if k and all(abs(a - b) < 1e-4 for a, b in zip(c[0] + c[1], prev[part][0] + prev[part][1])):
                    continue
                lines.append("execute on passengers if entity @s[tag=%s.p.%s] run data merge entity @s "
                             "{start_interpolation:0,interpolation_duration:%d,transformation:%s}"
                             % (tg, part, step, snbt_components(mob, c)))
            lines += cue_lines(mob, name, t, step)
            prev = frame
            wf(os.path.join(d, "f%d.mcfunction" % t), lines)
            # the clip tick runs after its own +1, so sample t plays at t+1
            leaves.append((t + 1, "%s/f%d" % (fn, t)))
        ticks = clip["ticks"]
        if clip["loop"]:
            head = ["execute if score @s %s matches %d.. run scoreboard players set @s %s 0"
                    % (T, ticks, T)]
        else:
            head = ["execute if score @s %s matches %d.. run return run function %s/anim/enter/idle"
                    % (T, ticks + 1, mob.fn)]
        wf(os.path.join(d, "tick.mcfunction"),
           ["# %s：%d 刻%s。由 %s 生成。" % (name, ticks, "循环" if clip["loop"] else "，播完回到 idle",
                                         mob.generator)]
           + head + ["scoreboard players add @s %s 1" % T, "function %s/at" % fn])
        dispatch_tree(mob, os.path.join(d, "at"), fn + "/at", leaves)
        wf(os.path.join(mob.anim, "enter", name + ".mcfunction"), [
            "# 切到 %s 并立即播放第一帧。" % name,
            "scoreboard players set @s %s %d" % (S, ids[name]),
            "scoreboard players set @s %s 0" % T,
        ] + ["execute at @s run " + playsound(mob, e, v, p) for e, v, p in mob.enter_cues.get(name, ())] + [
            "return run function %s/tick" % fn,
        ])
        wf(os.path.join(mob.func, "debug", "anim", name + ".mcfunction"), [
            "# 调试：让所有%s播放 %s%s。" % (mob.label, name, "（移动时自动切换走/站）" if name in ("idle", "walk") else ""),
            "execute as @e[%s] run function %s/anim/enter/%s" % (mob.carrier_sel, mob.fn, name),
        ])

    idle, walk = ids["idle"], ids["walk"]
    tick = [
        "# %s动画（as 载体）。%s = 当前片段，%s = 已播放刻数。" % (mob.label, S, T),
        "execute unless score @s %s matches 0.. run function %s/anim/init" % (S, mob.fn),
        "# 水平位移（百分之一格）的平方 >= 4 记为在走；停下 4 刻后才回 idle，免得来回抖",
        "execute store result score #x %s run data get entity @s Pos[0] 100" % sc,
        "execute store result score #z %s run data get entity @s Pos[2] 100" % sc,
        "scoreboard players operation #dx %s = #x %s" % (sc, sc),
        "scoreboard players operation #dx %s -= @s %s_x" % (sc, sc),
        "scoreboard players operation #dz %s = #z %s" % (sc, sc),
        "scoreboard players operation #dz %s -= @s %s_z" % (sc, sc),
        "scoreboard players operation @s %s_x = #x %s" % (sc, sc),
        "scoreboard players operation @s %s_z = #z %s" % (sc, sc),
        "scoreboard players operation #dx %s *= #dx %s" % (sc, sc),
        "scoreboard players operation #dz %s *= #dz %s" % (sc, sc),
        "scoreboard players operation #dx %s += #dz %s" % (sc, sc),
        "execute if score #dx %s matches 4.. run scoreboard players set @s %s_mv 4" % (sc, sc),
        "execute if score #dx %s matches ..3 if score @s %s_mv matches 1.. run scoreboard players remove @s %s_mv 1"
        % (sc, sc, sc),
        "execute if score @s %s matches %d if score @s %s_mv matches 1.. run return run function %s/anim/enter/walk"
        % (S, idle, sc, mob.fn),
        "execute if score @s %s matches %d if score @s %s_mv matches 0 run return run function %s/anim/enter/idle"
        % (S, walk, sc, mob.fn),
    ]
    for name, _, _ in mob.clips:
        tick.append("execute if score @s %s matches %d run return run function %s/anim/%s/tick"
                    % (S, ids[name], mob.fn, name))
    wf(os.path.join(mob.anim, "tick.mcfunction"), tick)
    wf(os.path.join(mob.anim, "init.mcfunction"), [
        "# 新%s：从 idle 第一帧开始，记下当前位置。" % mob.label,
        "scoreboard players set @s %s %d" % (S, idle),
        "scoreboard players set @s %s 0" % T,
        "scoreboard players set @s %s_mv 0" % sc,
        "execute store result score @s %s_x run data get entity @s Pos[0] 100" % sc,
        "execute store result score @s %s_z run data get entity @s Pos[2] 100" % sc,
    ])
    wf(os.path.join(mob.func, "load.mcfunction"), [
        "# %s计分板。由 %s 生成。" % (mob.label, mob.generator),
    ] + ["scoreboard objectives add %s dummy" % o
         for o in (S, T, sc + "_mv", sc + "_x", sc + "_z", sc)])


def hook_tag(dp, name, entry, before_last):
    tag = os.path.join(dp, "data", "minecraft", "tags", "function", name + ".json")
    with io.open(tag, encoding="utf-8") as fh:
        doc = json.load(fh)
    vals = doc["values"]
    if entry not in vals:
        # "before last" means before rpg:command/tick_end, which is meant to
        # run last; an entry appended after it must not move that slot
        end = "rpg:command/tick_end"
        at = (vals.index(end) if end in vals else len(vals) - 1) if before_last else len(vals)
        vals.insert(at, entry)
    wj(tag, doc)


def write_rig_runtime(mob, tick_lines, follow_extra=()):
    """Per-tick entry, follow and the riding predicate.  `tick_lines` is the
    mob's own entry (which carriers to follow); orphan cleanup is appended.

    A dying carrier drops out of @e on its killing blow, so its death
    cannot be heard from the follow loop.  Its parts keep riding through
    the 20-tick death animation and become orphans when it is removed;
    every other removal path kills the passengers first.  So an orphaned
    anchor part is the carrier's death, and that is where it is voiced."""
    orphan = "type=minecraft:item_display,tag=%s.part,predicate=!%s/riding" % (mob.tag, mob.fn)
    if mob.death or mob.on_death:
        anchor = "type=minecraft:item_display,tag=%s.p.%s,predicate=!%s/riding" % (mob.tag, mob.parts[0][0], mob.fn)
        sweep = "execute if entity @e[%s,limit=1] run function %s/orphans" % (orphan, mob.fn)
        wf(os.path.join(mob.func, "orphans.mcfunction"), [
            "# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。",
            "execute as @e[%s] at @s run function %s/death" % (anchor, mob.fn),
            "kill @e[%s]" % orphan,
        ])
        wf(os.path.join(mob.func, "death.mcfunction"), [
            "# %s的遗骸消散（at 部件位置）。" % mob.label,
        ] + ([playsound(mob, mob.death, radius=48)] if mob.death else []) + mob.on_death)
    else:
        sweep = "execute if entity @e[%s,limit=1] run kill @e[%s]" % (orphan, orphan)
    wf(os.path.join(mob.func, "tick.mcfunction"), tick_lines + [sweep])
    voice = []
    if mob.hurt:
        # Silent carrier: its voice is ours.  HurtTime is 10 on the first
        # tick after a hit.
        voice.append("execute if entity @s[nbt={HurtTime:10s}] run function %s/hurt" % mob.fn)
        wf(os.path.join(mob.func, "hurt.mcfunction"), [
            "# %s挨了一下。" % mob.label,
            playsound(mob, mob.hurt),
        ] + mob.on_hurt)
    if mob.ambient:
        event, chance = mob.ambient
        voice.append("execute if predicate %s/ambient run %s" % (mob.fn, playsound(mob, event, 1, 1, 16)))
        wj(os.path.join(mob.dp, "data", NS, "predicate", mob.key, "ambient.json"),
           {"condition": "minecraft:random_chance", "chance": chance})
    wf(os.path.join(mob.func, "follow.mcfunction"), [
        "# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。",
        "execute on passengers run rotate @s ~ 0",
        "function %s/anim/tick" % mob.fn,
    ] + voice + list(follow_extra))
    wj(os.path.join(mob.dp, "data", NS, "predicate", mob.key, "riding.json"), {
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {"vehicle": {}},
    })
    # idempotent hooks: tick before rpg:command/tick_end, load after the rest
    hook_tag(mob.dp, "tick", "%s/tick" % mob.fn, True)
    hook_tag(mob.dp, "load", "%s/load" % mob.fn, False)


def build(mob, rp, dp):
    """Atlas, part models and item definitions, baked clips.  Returns
    (baked, first idle frame as [(part, components)])."""
    mob.paths(rp, dp)
    bones, png, res = load_bbmodel(mob)
    tex_path = os.path.join(rp, "assets", NS, "textures", "item", mob.key, "atlas.png")
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)
    with open(tex_path, "wb") as fh:
        fh.write(png)

    offsets = {}
    for part, members in mob.parts:
        model, K = part_model(mob, bones, part, members, res)
        offsets[part] = K
        wj(os.path.join(rp, "assets", NS, "models", mob.key, part + ".json"), model)
        wj(os.path.join(rp, "assets", NS, "items", mob.key, part + ".json"), {
            "model": {"type": "minecraft:model", "model": "%s:%s/%s" % (NS, mob.key, part),
                      "tints": [{"type": "minecraft:custom_model_data", "index": 0,
                                 "default": 16777215}]}})
    baked = bake(mob, bones, offsets, load_animations(mob))
    write_anim(mob, baked)
    if mob.sounds:
        write_sounds(mob)
    # spawn already in idle's first pose so nothing snaps on the first tick
    first = baked["idle"]["frames"][0][1]
    print("%s: %d parts, atlas %dx%d, clips %s" % (
        mob.key, len(mob.parts), res["width"], res["height"],
        ", ".join("%s(%d)" % (n, len(c["frames"])) for n, c in baked.items())))
    return baked, [(part, first[part]) for part, _ in mob.parts]
