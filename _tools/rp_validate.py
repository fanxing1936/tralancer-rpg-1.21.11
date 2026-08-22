# -*- coding: utf-8 -*-
"""Resolve every reference a resource pack makes against a real client jar.

This reproduces, statically, the "Unable to find texture / model" warnings the
game prints at pack load, plus a few things the game silently ignores (dead
overrides of vanilla paths that no longer exist).
"""

import io
import json
import os
import sys
import zipfile

PACK = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
JAR = sys.argv[2] if len(sys.argv) > 2 else (
    "F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar")

problems = []
notes = []


def rid(s, kind):
    """`ns:path` -> the file it must resolve to."""
    if ":" in s:
        ns, path = s.split(":", 1)
    else:
        ns, path = "minecraft", s
    if kind == "model":
        return "assets/%s/models/%s.json" % (ns, path)
    if kind == "texture":
        return "assets/%s/textures/%s.png" % (ns, path)
    if kind == "texture_file":            # font providers already carry .png
        return "assets/%s/textures/%s" % (ns, path)
    if kind == "sound":
        return "assets/%s/sounds/%s.ogg" % (ns, path)
    raise ValueError(kind)


def canon(s):
    return s if ":" in s else "minecraft:" + s


# --- file indexes -----------------------------------------------------------
jar = zipfile.ZipFile(JAR)
VANILLA = set(n for n in jar.namelist() if n.startswith("assets/"))

PACK_FILES = set()
for dirpath, _d, names in os.walk(PACK):
    for fn in names:
        rel = os.path.relpath(os.path.join(dirpath, fn), PACK).replace(os.sep, "/")
        PACK_FILES.add(rel)

ALL = VANILLA | PACK_FILES


def load(rel):
    if rel in PACK_FILES:
        return json.load(io.open(os.path.join(PACK, rel), encoding="utf-8"))
    return json.loads(jar.read(rel))


# --- sprites produced by atlas sources --------------------------------------
GENERATED = set()


def atlas_sources(rel):
    """Atlas files MERGE across packs -- vanilla's sources still apply even
    when the pack ships a file at the same path."""
    out = []
    if rel in VANILLA:
        out.extend(json.loads(jar.read(rel)).get("sources", []))
    if rel in PACK_FILES:
        out.extend(json.load(io.open(os.path.join(PACK, rel), encoding="utf-8")).get("sources", []))
    return out


def scan_atlases():
    for rel in sorted(x for x in ALL if "/atlases/" in x and x.endswith(".json")):
        try:
            sources = atlas_sources(rel)
        except ValueError as exc:
            problems.append("%s: bad JSON (%s)" % (rel, exc))
            continue
        for src in sources:
            t = src.get("type", "").split(":")[-1]
            if t == "paletted_permutations":
                pk = rid(src["palette_key"], "texture")
                if pk not in ALL:
                    problems.append("%s: palette_key missing %s" % (rel, src["palette_key"]))
                for name, pal in src.get("permutations", {}).items():
                    if rid(pal, "texture") not in ALL:
                        problems.append("%s: permutation palette missing %s" % (rel, pal))
                for tex in src.get("textures", []):
                    if rid(tex, "texture") not in ALL:
                        problems.append("%s: source texture missing %s" % (rel, tex))
                    for name in src.get("permutations", {}):
                        GENERATED.add(canon(tex) + "_" + name)
            elif t == "single":
                if rid(src["resource"], "texture") not in ALL:
                    problems.append("%s: single source missing %s" % (rel, src["resource"]))


# --- models -----------------------------------------------------------------
checked_models = set()


def check_model(ref, origin):
    ref = canon(ref)
    if ref in checked_models:
        return
    checked_models.add(ref)
    if ref.startswith("minecraft:builtin/"):
        return                      # hardcoded in the client, not a file
    rel = rid(ref, "model")
    if rel not in ALL:
        problems.append("%s -> model not found: %s" % (origin, ref))
        return
    try:
        doc = load(rel)
    except ValueError as exc:
        problems.append("%s: bad JSON (%s)" % (rel, exc))
        return
    if "parent" in doc:
        check_model(doc["parent"], rel)
    for slot, tex in (doc.get("textures") or {}).items():
        if not isinstance(tex, str) or tex.startswith("#"):
            continue
        if canon(tex) in GENERATED:
            continue
        if rid(tex, "texture") not in ALL:
            problems.append("%s: texture not found: %s (slot %s)" % (rel, tex, slot))


def walk_item_model(node, origin):
    if isinstance(node, dict):
        if node.get("type", "").split(":")[-1] == "model" and isinstance(node.get("model"), str):
            check_model(node["model"], origin)
        for v in node.values():
            walk_item_model(v, origin)
    elif isinstance(node, list):
        for v in node:
            walk_item_model(v, origin)


def check_item_definitions():
    for rel in sorted(x for x in PACK_FILES if "/items/" in x and x.endswith(".json")):
        if rel not in VANILLA:
            notes.append("%s: no vanilla item by that name (definition will be ignored)" % rel)
        try:
            doc = load(rel)
        except ValueError as exc:
            problems.append("%s: bad JSON (%s)" % (rel, exc))
            continue
        if "model" not in doc:
            problems.append("%s: item definition has no `model`" % rel)
        walk_item_model(doc, rel)


def check_pack_models():
    for rel in sorted(x for x in PACK_FILES if "/models/" in x and x.endswith(".json")):
        ns = rel.split("/")[1]
        path = rel.split("/models/", 1)[1][:-5]
        check_model("%s:%s" % (ns, path), rel)


def check_fonts():
    for rel in sorted(x for x in PACK_FILES if "/font/" in x and x.endswith(".json")):
        doc = load(rel)
        for p in doc.get("providers", []):
            f = p.get("file")
            if isinstance(f, str) and rid(f, "texture_file") not in ALL:
                problems.append("%s: font texture not found: %s" % (rel, f))


def check_sounds():
    for rel in sorted(x for x in PACK_FILES if x.endswith("/sounds.json")):
        ns = rel.split("/")[1]
        doc = load(rel)
        for event, body in doc.items():
            for s in body.get("sounds", []):
                name = s if isinstance(s, str) else s.get("name", "")
                if isinstance(s, dict) and s.get("type") == "event":
                    continue
                if ":" not in name:
                    name = ns + ":" + name
                if rid(name, "sound") not in ALL:
                    problems.append("%s: sound not found: %s (event %s)" % (rel, name, event))


def check_dead_overrides():
    """A pack file that shadows nothing is either new content (fine, in the
    pack's own namespace) or a stale path from an older version (not fine)."""
    for rel in sorted(PACK_FILES):
        if not rel.startswith("assets/minecraft/"):
            continue
        if "/items/" in rel or "/atlases/" in rel or "/font/" in rel:
            continue
        if rel.endswith("sounds.json"):
            continue
        if rel.startswith("assets/minecraft/sounds/"):
            continue
        if rel.startswith("assets/minecraft/textures/font/"):
            continue
        if rel not in VANILLA:
            problems.append("overrides a path 1.21.11 no longer has: %s" % rel)


scan_atlases()
check_item_definitions()
check_pack_models()
check_fonts()
check_sounds()
check_dead_overrides()

print("pack files: %d   vanilla assets: %d   generated sprites: %d"
      % (len(PACK_FILES), len(VANILLA), len(GENERATED)))
if notes:
    print("\n%d notes:" % len(notes))
    for n in notes[:20]:
        print("  " + n)
if problems:
    print("\n%d problems:" % len(problems))
    for p in problems[:60]:
        print("  " + p)
    sys.exit(1)
print("\nno problems found")
