# -*- coding: utf-8 -*-
"""Invert the hurt-driven weapon loops, but only where it provably commutes.

`rpg:item/sword/legend/legend1` and its `g*` blocks each open every line with
the same `execute as @e[tag=rpg.hurt] ...`, so a tick in which anything took
damage walks the whole entity table once per line -- 63 walks in legend1, 36 in
g8, and so on, 612 across the pack at worst.

Folding that into one walk (`execute as @e[tag=rpg.hurt] run function <body>`,
body operating on `@s`) is the same trick opt_index.py uses on the flag index.
It is *not* unconditionally safe here though: it turns line-major evaluation
(for each line, for each entity) into entity-major (for each entity, for each
line).  Those two orders give different results whenever a later line writes
state that an earlier line reads -- with two mobs hit by one sweep, the second
mob would see scores the first mob's later lines had already changed.

So each block is checked for a backward dependence first:

  * every line's reads  -- objectives named in `scores={...}` / `if score`,
    tags named in `tag=` -- and its writes -- `scoreboard players set|add|
    remove|reset`, `tag @... add|remove` -- are collected;
  * a block is invertible only if no line writes anything that an earlier line
    in the same block reads.

With no backward dependence the two loop orders commute, so the inversion is
behaviour-preserving.  Blocks that fail the test are left exactly as they are
and reported, rather than being quietly "optimised" into a combat bug.
"""

import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
DRY = "--dry-run" in sys.argv
FUNC = os.path.join(ROOT, "data/rpg/function")

PREFIX = "execute as @e[tag=rpg.hurt] "

RE_SCORES = re.compile(r"scores=\{([^}]*)\}")
RE_SCORE_KEY = re.compile(r"(\w+)\s*=")
RE_IF_SCORE = re.compile(r"\bif score \S+ (\w+)")
RE_TAG_READ = re.compile(r"tag=!?([A-Za-z0-9_.+-]+)")
RE_SB_WRITE = re.compile(
    r"\bscoreboard players (?:set|add|remove|reset|operation)\s+\S+\s+(\w+)")
RE_TAG_WRITE = re.compile(r"\btag @\S+ (?:add|remove) ([A-Za-z0-9_.+-]+)")
# things that can change which entities carry rpg.hurt out from under us
RE_VOLATILE = re.compile(r"\b(kill|ride|tp)\b.*rpg\.hurt")


def reads(line):
    out = set()
    for blk in RE_SCORES.findall(line):
        out |= set(RE_SCORE_KEY.findall(blk))
    out |= set(RE_IF_SCORE.findall(line))
    out |= set(RE_TAG_READ.findall(line))
    return out


def writes(line):
    return set(RE_SB_WRITE.findall(line)) | set(RE_TAG_WRITE.findall(line))


def body_lines(text):
    """The runnable lines, keeping comments/blanks separate."""
    return [l for l in text.split("\n") if l.strip()
            and not l.strip().startswith("#")]


def strip(line):
    """Drop just the `as @e[tag=rpg.hurt]` clause, keeping a valid command.

    The prefix includes the word `execute`, so removing all of it would leave
    `at @s on attacker ... run ...` -- not a command.  Put `execute` back, or
    return the bare command when nothing but `run` was left.
    """
    rest = line[len(PREFIX):]
    if rest.startswith("run "):
        return rest[len("run "):]
    return "execute " + rest


def invertible(lines):
    """-> (ok, reason).  Safe iff no line writes what an earlier line reads."""
    seen_reads = set()
    for l in lines:
        if "rpg.hurt" in " ".join(RE_TAG_WRITE.findall(l)):
            return False, "block rewrites rpg.hurt itself"
        if RE_VOLATILE.search(l):
            return False, "block moves/kills the hurt set"
        w = writes(l)
        clash = w & seen_reads
        if clash:
            return False, "writes %s that an earlier line reads" % ",".join(sorted(clash))
        seen_reads |= reads(l)
    return True, ""


def main():
    total_lines = saved = converted = 0
    skipped = []
    for root, _dirs, files in os.walk(FUNC):
        for f in sorted(files):
            if not f.endswith(".mcfunction"):
                continue
            path = os.path.join(root, f)
            text = io.open(path, encoding="utf-8").read()
            lines = body_lines(text)
            if len(lines) < 4 or not all(l.startswith(PREFIX) for l in lines):
                continue
            rel = os.path.relpath(path, FUNC).replace(os.sep, "/")[:-len(".mcfunction")]
            ok, why = invertible(lines)
            if not ok:
                skipped.append((rel, len(lines), why))
                continue
            converted += 1
            total_lines += len(lines)
            saved += len(lines) - 1
            if DRY:
                continue
            body = ["# 由 opt_invert.py 内外翻：原本这 %d 行每行都自己扫一遍全实体表" % len(lines),
                    "# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。",
                    "# 已静态验证过没有反向依赖，所以两种遍历顺序等价。", ""]
            body += [strip(l) for l in lines]
            io.open(path[:-len(".mcfunction")] + "_body.mcfunction", "w",
                    encoding="utf-8", newline="\n").write("\n".join(body) + "\n")
            io.open(path, "w", encoding="utf-8", newline="\n").write(
                "# %d 行折进 %s_body，全实体表每刻只扫一遍。\n"
                "execute as @e[tag=rpg.hurt] run function rpg:%s_body\n"
                % (len(lines), os.path.basename(rel), rel))

    print("inverted blocks: %d  (%d lines -> %d walks, %d fewer)"
          % (converted, total_lines, converted, saved))
    if skipped:
        print("left alone (would change behaviour):")
        for rel, n, why in skipped:
            print("  %-46s %3d lines  -- %s" % (rel, n, why))


if __name__ == "__main__":
    main()
