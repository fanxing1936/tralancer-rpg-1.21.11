# -*- coding: utf-8 -*-
"""Render each catalogued item to the icon the client actually draws.

The old version took a single texture -- item definition -> model ->
textures.layer0 -- which is only correct for items the game draws in one flat
pass.  Anything the client composites came out wrong on the page: leather
armour showed the bare greyscale hide instead of its dye, every trimmed piece
lost its trim entirely, and potions showed empty glass.

This follows the client's real path:

  item definition -> (select on trim_material / range_dispatch on
  custom_model_data) -> model -> layer0..layerN, each layer multiplied by
  tints[i] when the model declares one -> alpha-composited bottom-up.

Trim sprites are not files.  `assets/minecraft/atlases/armor_trims.json`
generates them at load with a `paletted_permutations` source: the greyscale
`trims/items/<slot>_trim.png` has each pixel looked up in the 8-entry key
palette `trims/color_palettes/trim_palette.png` and replaced with the same
index from `color_palettes/<material>.png`.  That is reproduced here, so
`trims/items/helmet_trim_netherite` resolves even though no such file exists.

Textures come from the resource pack first and the real 1.21.11 client jar
second, so every card shows exactly what a player sees.
"""

import base64
import json
import os
import zipfile

import png_tool as P

RP = os.path.join(os.path.dirname(__file__), "..", "resourcepack")
JAR = r"F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar"

_jar = zipfile.ZipFile(JAR)
_jar_names = set(_jar.namelist())
_cache = {}
_tex_cache = {}
MISSES = []

ATLAS = "assets/minecraft/atlases/armor_trims.json"


def _read(rel):
    p = os.path.join(RP, rel)
    if os.path.isfile(p):
        return open(p, "rb").read()
    if rel in _jar_names:
        return _jar.read(rel)
    return None


def _json(rel):
    b = _read(rel)
    return json.loads(b.decode("utf-8")) if b else None


def _json_pack(rel):
    p = os.path.join(RP, rel)
    if not os.path.isfile(p):
        return None
    return json.loads(open(p, "rb").read().decode("utf-8"))


def _json_jar(rel):
    if rel not in _jar_names:
        return None
    return json.loads(_jar.read(rel).decode("utf-8"))


def _split(ref):
    ns, path = (ref.split(":", 1) if ":" in ref else ("minecraft", ref))
    return ns, path


# --------------------------------------------------------------------------
# paletted_permutations: synthesise the trim sprites the atlas generates
# --------------------------------------------------------------------------
_perm = None


def _permutations():
    """-> (key palette rgb list, {permutation name: rgb list})"""
    global _perm
    if _perm is not None:
        return _perm
    key, perms = [], {}
    # Atlas definitions are one of the few resource types the game *merges*
    # across packs instead of overriding, so read every layer.  The pack ships
    # its own armor_trims.json adding a custom "holy" material; reading only
    # the pack copy would lose all twelve vanilla materials, and reading only
    # the jar would lose "holy".
    sources = []
    for doc in (_json_pack(ATLAS), _json_jar(ATLAS)):
        sources += (doc or {}).get("sources", [])
    for src in sources:
        if (src.get("type") or "").split(":")[-1] != "paletted_permutations":
            continue
        ns, path = _split(src["palette_key"])
        w, h, rgba = P.decode(_read("assets/%s/textures/%s.png" % (ns, path)))
        key = [tuple(rgba[i * 4:i * 4 + 3]) for i in range(w * h)]
        for name, ref in src.get("permutations", {}).items():
            ns, path = _split(ref)
            raw = _read("assets/%s/textures/%s.png" % (ns, path))
            if raw is None:
                continue
            w2, h2, rgba2 = P.decode(raw)
            perms[name] = [tuple(rgba2[i * 4:i * 4 + 3]) for i in range(w2 * h2)]
    _perm = (key, perms)
    return _perm


def _permute(base_path, perm_name):
    """Recolour a greyscale trim sprite through one material palette."""
    key, perms = _permutations()
    pal = perms.get(perm_name)
    if pal is None:
        return None
    raw = _read("assets/minecraft/textures/%s.png" % base_path)
    if raw is None:
        return None
    w, h, rgba = P.decode(raw)
    lut = {}
    for i, k in enumerate(key):
        if i < len(pal):
            lut[k] = pal[i]
    out = bytearray(rgba)
    for i in range(w * h):
        o = i * 4
        if out[o + 3] == 0:
            continue
        rep = lut.get((out[o], out[o + 1], out[o + 2]))
        if rep:
            out[o], out[o + 1], out[o + 2] = rep
    return w, h, bytes(out)


def _texture(ref):
    """texture id -> (w, h, rgba), resolving generated trim permutations."""
    if ref in _tex_cache:
        return _tex_cache[ref]
    ns, path = _split(ref)
    raw = _read("assets/%s/textures/%s.png" % (ns, path))
    got = None
    if raw is not None:
        got = P.decode(raw)
    else:
        # not a real file -- try the atlas permutations, longest name first so
        # "..._diamond_darker" wins over "..._diamond"
        _key, perms = _permutations()
        for name in sorted(perms, key=len, reverse=True):
            if path.endswith("_" + name):
                got = _permute(path[:-(len(name) + 1)], name)
                break
    _tex_cache[ref] = got
    return got


# --------------------------------------------------------------------------
# item definition / model resolution
# --------------------------------------------------------------------------
def _model_layers(ref, depth=0):
    """model id -> [texture id, ...] in layer order (follows `parent`)."""
    if depth > 6:
        return []
    ns, path = _split(ref)
    doc = _json("assets/%s/models/%s.json" % (ns, path))
    if not doc:
        return []
    tex = doc.get("textures") or {}
    layers = []
    i = 0
    while ("layer%d" % i) in tex:
        v = tex["layer%d" % i]
        if isinstance(v, str) and not v.startswith("#"):
            layers.append(v)
        i += 1
    if layers:
        return layers
    for slot in ("0", "all", "texture"):
        v = tex.get(slot)
        if isinstance(v, str) and not v.startswith("#"):
            return [v]
    if "parent" in doc:
        return _model_layers(doc["parent"], depth + 1)
    return []


def _pick(node, cmd, trim_material):
    """Walk an item definition -> (model id, tints list)."""
    if not isinstance(node, dict):
        return None, []
    t = (node.get("type") or "").split(":")[-1]
    if t == "model":
        return node.get("model"), node.get("tints") or []
    if t == "range_dispatch" and node.get("property", "").endswith("custom_model_data"):
        best = None
        for e in node.get("entries", []):
            if cmd is not None and cmd >= e["threshold"]:
                if best is None or e["threshold"] >= best["threshold"]:
                    best = e
        if best is not None:
            return _pick(best["model"], cmd, trim_material)
        return _pick(node.get("fallback"), cmd, trim_material)
    if t == "select" and node.get("property", "").endswith("display_context"):
        # Spears (and anything else with a separate in-hand model) branch on
        # where they are being drawn.  A codex entry is an inventory icon, so
        # take the "gui" case; the fallback is the in-hand art.
        for case in node.get("cases", []):
            whens = case.get("when")
            whens = whens if isinstance(whens, list) else [whens]
            if any(str(x).split(":")[-1] == "gui" for x in whens):
                return _pick(case.get("model"), cmd, trim_material)
        return _pick(node.get("fallback"), cmd, trim_material)
    if t == "select" and node.get("property", "").endswith("trim_material"):
        if trim_material:
            want = trim_material.split(":")[-1]
            for case in node.get("cases", []):
                whens = case.get("when")
                whens = whens if isinstance(whens, list) else [whens]
                if any(str(x).split(":")[-1] == want for x in whens):
                    return _pick(case.get("model"), cmd, trim_material)
        return _pick(node.get("fallback"), cmd, trim_material)
    # any other branch: take the resting state, which is what an inventory
    # icon shows
    for k in ("on_false", "fallback"):
        if k in node:
            got = _pick(node[k], cmd, trim_material)
            if got[0]:
                return got
    for case in node.get("cases", []):
        got = _pick(case.get("model"), cmd, trim_material)
        if got[0]:
            return got
    return None, []


# --------------------------------------------------------------------------
# compositing
# --------------------------------------------------------------------------
OVERRIDE = {"vault": "minecraft:block/vault_front_on"}

# Skulls use a `minecraft:special` model -- a 3D head built from a skin, with no
# flat sprite anywhere to read.  Rebuild the icon the way the game builds the
# head itself: the face region of the default skin with the hat layer over it.
SKIN = "assets/minecraft/textures/entity/player/wide/steve.png"


def _player_head():
    raw = _read(SKIN)
    if raw is None:
        return None
    w, h, rgba = P.decode(raw)

    def crop(x0, y0):
        out = bytearray(8 * 8 * 4)
        for y in range(8):
            s = ((y0 + y) * w + x0) * 4
            out[y * 32:(y + 1) * 32] = rgba[s:s + 32]
        return out

    face = crop(8, 8)
    _over(face, crop(40, 8))          # the hat layer sits on top of the face
    return 16, 16, P.nearest(8, 8, bytes(face), 16, 16)


def _tint_rgb(tint, dyed, potion):
    """A tint entry + the item's own components -> (r, g, b), or None."""
    t = (tint.get("type") or "").split(":")[-1]
    val = None
    if t == "dye":
        val = dyed
    elif t == "potion":
        val = (potion or {}).get("custom_color")
    if val is None:
        val = tint.get("default")
    if val is None:
        return None
    v = int(val) & 0xFFFFFF
    return (v >> 16 & 255, v >> 8 & 255, v & 255)


def _over(dst, src):
    """Alpha-composite src over dst, both flat RGBA bytearrays of equal size."""
    for i in range(0, len(dst), 4):
        sa = src[i + 3]
        if sa == 0:
            continue
        if sa == 255 or dst[i + 3] == 0:
            dst[i:i + 4] = src[i:i + 4]
            continue
        a = sa / 255.0
        da = dst[i + 3] / 255.0
        out_a = a + da * (1 - a)
        for c in range(3):
            dst[i + c] = int(round(
                (src[i + c] * a + dst[i + c] * da * (1 - a)) / out_a))
        dst[i + 3] = int(round(out_a * 255))


def composite(item_id, cmd=None, dyed=None, trim=None, potion=None):
    """-> (w, h, rgba) for the icon as the client draws it."""
    item_id = item_id.split(":")[-1]
    if item_id in OVERRIDE:
        return _texture(OVERRIDE[item_id])
    if item_id in ("player_head", "skeleton_skull", "zombie_head",
                   "creeper_head", "piglin_head", "dragon_head"):
        got = _player_head() if item_id == "player_head" else None
        if got:
            return got

    material = (trim or {}).get("material")
    defn = _json("assets/minecraft/items/%s.json" % item_id)
    layers, tints = [], []
    if defn:
        mdl, tints = _pick(defn.get("model"), float(cmd) if cmd else None, material)
        if mdl:
            layers = _model_layers(mdl)
    if not layers:
        layers = _model_layers("minecraft:item/" + item_id)
    if not layers:
        layers = ["minecraft:item/" + item_id]

    base = None
    for i, ref in enumerate(layers):
        got = _texture(ref)
        if got is None:
            MISSES.append((item_id, cmd, ref))
            continue
        w, h, rgba = got
        px = bytearray(rgba)
        if i < len(tints):
            rgb = _tint_rgb(tints[i], dyed, potion)
            if rgb:
                for o in range(0, len(px), 4):
                    if px[o + 3]:
                        px[o] = px[o] * rgb[0] // 255
                        px[o + 1] = px[o + 1] * rgb[1] // 255
                        px[o + 2] = px[o + 2] * rgb[2] // 255
        if base is None:
            base = [w, h, px]
        elif (w, h) == (base[0], base[1]):
            _over(base[2], px)
    return None if base is None else (base[0], base[1], bytes(base[2]))


def texture_for(item_id, cmd=None, dyed=None, trim=None, potion=None):
    key = (item_id.split(":")[-1], cmd, dyed,
           json.dumps(trim, sort_keys=True) if trim else None,
           (potion or {}).get("custom_color"))
    if key in _cache:
        return _cache[key]
    got = composite(item_id, cmd, dyed, trim, potion)
    uri = None
    if got:
        uri = ("data:image/png;base64,"
               + base64.b64encode(P.encode(*got)).decode("ascii"))
    _cache[key] = uri
    return uri


def img(item_id, cmd=None, alt="", dyed=None, trim=None, potion=None, glint=False):
    uri = texture_for(item_id, cmd, dyed, trim, potion)
    if not uri:
        return '<span class="icon icon-none" aria-hidden="true"></span>'
    tag = ('<img class="icon" src="%s" alt="%s" loading="lazy" decoding="async">'
           % (uri, alt.replace('"', "&quot;")))
    if not glint:
        return tag
    # the enchantment sheen: a highlight sweeping across the sprite, masked to
    # the item's own silhouette, the same read as the in-game glint
    return ('<span class="icon-wrap glint" style="--sprite:url(%s)">%s</span>'
            % (uri, tag))


def item_img(entry, alt=None):
    """Convenience wrapper taking a record straight out of _data_items.json."""
    return img(entry.get("item") or "", entry.get("cmd"),
               alt if alt is not None else (entry.get("name") or ""),
               dyed=entry.get("dyed_color"), trim=entry.get("trim"),
               potion=entry.get("potion_contents"),
               glint=bool(entry.get("enchantments")))


def loot_img(entry, alt=None):
    """Same, for a loot-table record.  Those keep the raw component map under
    `components`, keyed by namespaced id, instead of the flattened fields the
    item extractor produces."""
    c = entry.get("components") or {}

    def comp(name):
        return c.get("minecraft:" + name, c.get(name))

    cmd = comp("custom_model_data")
    if isinstance(cmd, dict):
        cmd = (cmd.get("floats") or [None])[0]
    elif not isinstance(cmd, (int, float)):
        cmd = None
    dyed = comp("dyed_color")
    if isinstance(dyed, dict):                 # pre-1.21.5 {rgb: N}
        dyed = dyed.get("rgb")
    ench = comp("enchantments")
    if isinstance(ench, dict):
        ench = ench.get("levels", ench)
    return img(entry.get("item") or "", cmd,
               alt if alt is not None else (entry.get("name") or ""),
               dyed=dyed, trim=comp("trim"), potion=comp("potion_contents"),
               glint=bool(ench) or bool(entry.get("ench")))
