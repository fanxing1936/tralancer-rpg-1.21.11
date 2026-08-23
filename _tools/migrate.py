# -*- coding: utf-8 -*-
"""Drive the 1.21 -> 1.21.11 migration over a data pack directory."""

import io
import json
import os
import re
import sys

import transform as T
import jsonpass
import mcfunc

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

PACK_MCMETA = {
    "pack": {
        "description": "TRALANCER RPG!",
        "pack_format": 94,
        "min_format": [94, 1],
        "max_format": 94,
    }
}

errors = []
touched = []


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def do_mcfunction(path):
    with io.open(path, encoding="utf-8") as fh:
        src = fh.read()
    lines = src.split("\n")
    out = []
    changed = False
    for ln, line in enumerate(lines, 1):
        try:
            new = mcfunc.process_line(line)
        except Exception as exc:                       # pragma: no cover
            errors.append("%s:%d  %s: %s" % (rel(path), ln, type(exc).__name__, exc))
            new = line
        if new != line:
            changed = True
        out.append(new)
    if changed:
        touched.append(rel(path))
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(out))


def do_json(path):
    with io.open(path, encoding="utf-8") as fh:
        raw = fh.read()
    try:
        doc = json.loads(raw)
    except ValueError as exc:
        errors.append("%s  invalid JSON: %s" % (rel(path), exc))
        return
    r = rel(path)
    doc = jsonpass.walk(doc)
    if "/advancement/" in r:
        doc = jsonpass.advancement_pass(doc)
    if "/trim_material/" in r:
        doc = jsonpass.trim_material_pass(doc)
    new = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    if new != raw:
        touched.append(r)
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new)


CREEPER_RE = re.compile(r'"?Fuse"?\s*:\s*0\b')


def fix_creeper_fuse(root):
    """`Fuse:0` 在 1.21.11 是死名字 —— 本该当场引爆的苦力怕会站着不动。

    实测：苦力怕的 NBT 里既没有 `Fuse` 也没有 `fuse`，写进 summon 会被
    静默丢掉。现在让它立刻炸的字段是 `ignited:1b`（实测带它召出来的
    苦力怕两刻之内就消失了）。

    只改 `Fuse:0` —— 那是「立刻炸」的写法。别处非零的引信留给作者自己定。
    """
    hit = 0
    for base, _d, files in os.walk(root):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(base, f)
            s = io.open(p, encoding="utf-8").read()
            if not CREEPER_RE.search(s):
                continue
            t = CREEPER_RE.sub("ignited:1b", s)
            if t != s:
                io.open(p, "w", encoding="utf-8", newline="\n").write(t)
                hit += 1
    if hit:
        print("creeper Fuse:0 -> ignited:1b in %d file(s)" % hit)
    return hit


def main():
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            if fn.endswith(".mcfunction"):
                do_mcfunction(path)
            elif fn == "pack.mcmeta":
                continue
            elif fn.endswith(".json"):
                do_json(path)

    fix_creeper_fuse(ROOT)

    with io.open(os.path.join(ROOT, "pack.mcmeta"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(PACK_MCMETA, ensure_ascii=False, indent=4) + "\n")

    print("files rewritten: %d" % len(touched))
    print()
    for k in sorted(T.STATS):
        print("  %-42s %d" % (k, T.STATS[k]))
    if mcfunc.SKIPPED:
        print("\n!! %d unparsed regions:" % len(mcfunc.SKIPPED))
        seen = set()
        for kind, msg in mcfunc.SKIPPED:
            k = (kind, msg[:70])
            if k in seen:
                continue
            seen.add(k)
            print("   [%s] %s" % (kind, msg[:150]))
            if len(seen) > 25:
                break
    if errors:
        print("\n!! %d problems:" % len(errors))
        for e in errors[:60]:
            print("   " + e)


if __name__ == "__main__":
    main()
