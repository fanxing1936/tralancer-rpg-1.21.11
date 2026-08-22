# -*- coding: utf-8 -*-
"""Which textures does the resource pack ship but never reference?"""

import io
import json
import os
import sys

PACK = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"


def rid(ns, path):
    return "%s:%s" % (ns, path)


def walk_json(path):
    try:
        return json.load(io.open(path, encoding="utf-8"))
    except ValueError:
        return None


used = set()
declared = set()

for dirpath, _d, files in os.walk(PACK):
    for fn in files:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, PACK).replace(os.sep, "/")
        parts = rel.split("/")
        if len(parts) < 3 or parts[0] != "assets":
            continue
        ns = parts[1]
        kind = parts[2]

        if kind == "textures" and fn.endswith(".png"):
            declared.add(rid(ns, "/".join(parts[3:])[:-4]))

        elif kind == "models" and fn.endswith(".json"):
            doc = walk_json(p)
            if not isinstance(doc, dict):
                continue
            for slot, tex in (doc.get("textures") or {}).items():
                if isinstance(tex, str) and not tex.startswith("#"):
                    t = tex if ":" in tex else "minecraft:" + tex
                    used.add(t)

        elif kind == "atlases" and fn.endswith(".json"):
            doc = walk_json(p)
            for src in (doc or {}).get("sources", []):
                for tex in src.get("textures", []):
                    used.add(tex if ":" in tex else "minecraft:" + tex)
                for key in ("palette_key", "resource"):
                    if key in src:
                        v = src[key]
                        used.add(v if ":" in v else "minecraft:" + v)
                for v in (src.get("permutations") or {}).values():
                    used.add(v if ":" in v else "minecraft:" + v)

        elif kind == "font" and fn.endswith(".json"):
            doc = walk_json(p)
            for prov in (doc or {}).get("providers", []):
                f = prov.get("file")
                if isinstance(f, str):
                    f = f[:-4] if f.endswith(".png") else f
                    used.add(f if ":" in f else "minecraft:" + f)


def kind_of(t):
    path = t.split(":", 1)[1]
    return path.split("/")[0]


unused = sorted(declared - used)
print("declared %d   referenced-from-pack %d   unused %d"
      % (len(declared), len(used & declared), len(unused)))

groups = {}
for t in unused:
    groups.setdefault(kind_of(t), []).append(t)
for k in sorted(groups):
    print("\n-- %s (%d)" % (k, len(groups[k])))
    for t in groups[k]:
        print("   " + t)

json.dump(unused, io.open("../_unused_textures.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
