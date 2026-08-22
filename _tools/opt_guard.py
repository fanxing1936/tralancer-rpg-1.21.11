# -*- coding: utf-8 -*-
"""Put one guard in front of each run of lines that share a world-wide `@e` walk.

The pack spends most of its per-tick budget walking the entity list looking for
tags that are empty almost all the time -- `rpg.hurt` (nothing was damaged this
tick), `devil` (no boss summoned), the in-flight arrow tags.  legend1 alone does
271 of those walks per tick.

A run of consecutive lines that all open on the identical selector is moved into
a sub-function and called behind a single `if entity <same selector>`.  The lines
keep their own `as @e[...]`, their order, and their context, so behaviour is
unchanged: the guard can only skip lines that would every one of them have
matched nothing.
"""

import io
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
MIN_RUN = 3

HEAD_RE = re.compile(r"^execute\s+as\s+(@e\[[^\]]*\])\s")
FUNC_RE = re.compile(r"\bfunction\s+([a-z0-9_.-]+:[a-z0-9_./-]+)")

STATS = {"guards": 0, "lines": 0, "functions": 0}


def path_of(ref):
    ns, path = ref.split(":", 1)
    return os.path.join(ROOT, "data", ns, "function", path + ".mcfunction")


def guardable(sel):
    """Only tag-driven world walks: cheap to test, and the tag is the whole point."""
    body = sel[2:]
    if "nbt=" in body or "scores=" in body:
        return False
    # a typed selector is already indexed, but repeating it N times still walks
    # that type's list N times -- worth one guard all the same
    return bool(re.search(r"(^|\[|,)tag=(?!!)[A-Za-z0-9_.+-]+", body))


def process(ref, seen):
    if ref in seen:
        return
    seen.add(ref)
    p = path_of(ref)
    if not os.path.isfile(p):
        return
    src = io.open(p, encoding="utf-8").read().split("\n")

    for line in src:
        for m in FUNC_RE.finditer(line):
            process(m.group(1), seen)

    ns, path = ref.split(":", 1)
    out, i, made = [], 0, 0
    while i < len(src):
        st = src[i].strip()
        m = HEAD_RE.match(st)
        if not m or not guardable(m.group(1)):
            out.append(src[i])
            i += 1
            continue
        head = m.group(1)
        j, block = i, []
        while j < len(src):
            s2 = src[j].strip()
            if not s2 or s2.startswith("#"):
                # absorb blanks/comments only if the run continues past them
                k = j
                while k < len(src) and (not src[k].strip() or src[k].strip().startswith("#")):
                    k += 1
                m2 = HEAD_RE.match(src[k].strip()) if k < len(src) else None
                if m2 and m2.group(1) == head:
                    block.extend(src[j:k])
                    j = k
                    continue
                break
            m2 = HEAD_RE.match(s2)
            if not m2 or m2.group(1) != head:
                break
            block.append(src[j])
            j += 1
        cmds = [b for b in block if b.strip() and not b.strip().startswith("#")]
        if len(cmds) < MIN_RUN:
            out.append(src[i])
            i += 1
            continue

        sub = "%s/g%d" % (path, made)
        made += 1
        sp = os.path.join(ROOT, "data", ns, "function", sub + ".mcfunction")
        d = os.path.dirname(sp)
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(sp, "w", encoding="utf-8", newline="\n").write(
            "# %d 行原本各自扫一遍全实体表找 %s；现在由上层一次判定后统一进入。\n"
            "# 行内容与顺序原样保留。\n" % (len(cmds), head)
            + "\n".join(block).rstrip("\n") + "\n")
        out.append("execute if entity %s run function %s:%s" % (head, ns, sub))
        STATS["guards"] += 1
        STATS["lines"] += len(cmds)
        i = j

    if made:
        STATS["functions"] += 1
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))


def main():
    tag = os.path.join(ROOT, "data", "minecraft", "tags", "function", "tick.json")
    roots = json.load(io.open(tag, encoding="utf-8"))["values"]
    seen = set()
    for r in roots:
        process(r, seen)
    print("guards inserted: %d, covering %d lines across %d functions"
          % (STATS["guards"], STATS["lines"], STATS["functions"]))


if __name__ == "__main__":
    main()
