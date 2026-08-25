# -*- coding: utf-8 -*-
"""Find what breaks when a second player joins.

Single-player hides three whole classes of bug, because in single-player they
are all the same thing:

* **@a / @p is "me".**  `@a[tag=...,limit=1,sort=nearest]` reads as "the caster"
  with one player online.  With two, it can resolve to the other one -- damage
  gets attributed to a bystander, a skill fires from the wrong feet.
* **A fake-player score is a variable.**  `#charge rpg_x` reads as "this cast's
  scratch value".  With two players casting in the same tick it is one shared
  global, and the second write wins.
* **A tag is a flag.**  Fine while it lives and dies inside one function call;
  a bug the moment it survives across ticks, because now two players can carry
  it at once and any unbounded `@a[tag=...]` hits both.

And one class of lag: anything under `execute as @a` costs N times as much on
an N-player server.  That is fine for a scoreboard compare and ruinous for a
world walk.

This reports, it does not rewrite -- every finding needs a human call about
what the intent was.
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

# A world walk is any @e the entity-type index cannot serve.  That means no
# `type=` at all -- but ALSO `type=!...`, which is the trap: a *negative* type
# filter still has to visit every entity in the box to find out what to skip.
# Counting those as "typed" is what hid damage_scan's real cost from the first
# run of this audit.
WALK = re.compile(r"@e\[(?![^\]]*\btype=(?!!))[^\]]*\]")
TYPED = re.compile(r"@e\[[^\]]*\btype=(?!!)[^\]]*\]")
# @a used to pick one player -- the "who cast this" idiom
PICK = re.compile(r"@[ap]\[[^\]]*\b(?:limit=1|sort=nearest)[^\]]*\]")
FAKE = re.compile(r"scoreboard players \w+ (#\w+) (\w+)")
FAKE_OP = re.compile(r"scoreboard players operation (#\w+) ")
STORE_FAKE = re.compile(r"store result score (#\w+) ")


def read(rel):
    with io.open(os.path.join(FUNC, rel), encoding="utf-8") as fh:
        return fh.read()


def all_funcs():
    for root, dirs, files in os.walk(FUNC):
        dirs.sort()
        for f in sorted(files):
            if f.endswith(".mcfunction"):
                p = os.path.join(root, f)
                yield os.path.relpath(p, FUNC).replace(os.sep, "/")[:-len(".mcfunction")]


def body(name):
    return read(name + ".mcfunction")


CALL = re.compile(r"function rpg:([\w/]+)")


def reachable_from(entry, seen=None):
    """Every function reachable from an entry point."""
    if seen is None:
        seen = set()
    if entry in seen:
        return seen
    seen.add(entry)
    try:
        text = body(entry)
    except IOError:
        return seen
    for m in CALL.finditer(text):
        reachable_from(m.group(1), seen)
    return seen


def per_player_cost():
    """What does one extra player actually cost per tick?

    Walk the call graph from every `execute as @a ... run function` on the tick
    path and add up the world walks behind it.  Those are the lines that get
    paid once per online player.
    """
    tick = reachable_from("command/tick") | reachable_from("command/index")
    hot = []
    for name in sorted(tick):
        try:
            text = body(name)
        except IOError:
            continue
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            m = re.match(r"execute as @a\b.*run function rpg:([\w/]+)", line)
            if not m:
                continue
            sub = reachable_from(m.group(1))
            walks = typed = 0
            for s in sub:
                try:
                    t = body(s)
                except IOError:
                    continue
                for l in t.split("\n"):
                    if l.strip().startswith("#"):
                        continue
                    walks += len(WALK.findall(l))
                    typed += len(TYPED.findall(l))
            if walks or typed:
                hot.append((walks, typed, name, m.group(1), len(sub)))
    hot.sort(reverse=True)
    return hot


def unbounded_player_picks():
    """`@a[tag=...]` with no distance -- reaches across the whole world."""
    out = []
    for name in all_funcs():
        for i, line in enumerate(body(name).split("\n"), 1):
            if line.strip().startswith("#"):
                continue
            for m in re.finditer(r"@a\[([^\]]*)\]", line):
                inner = m.group(1)
                if "tag=" not in inner or "distance=" in inner:
                    continue
                out.append((name, i, m.group(0), line.strip()[:110]))
    return out


def nearest_player_uses():
    """Every `@p` is a multiplayer ownership decision until proven otherwise.

    Some are intentional (for example a world event choosing its nearest
    recipient), but `@p` inside a weapon or pact function very often means the
    author lost the original @s after switching execution to a projectile or
    victim.  Keep these in a separate, short list so they cannot hide among
    hundreds of ordinary @a traversals.
    """
    out = []
    for name in all_funcs():
        for i, line in enumerate(body(name).split("\n"), 1):
            if line.strip().startswith("#"):
                continue
            for m in re.finditer(r"@p(?:\[[^\]]*\])?", line):
                out.append((name, i, m.group(0), line.strip()[:120]))
    return out


def shared_scratch():
    """Fake-player scores written from a player-scoped context.

    A `#name` holder is one global cell.  If the code that writes it can run
    for two players in the same tick, the second write clobbers the first.
    """
    out = {}
    for name in all_funcs():
        text = body(name)
        names = set()
        for rx in (FAKE, FAKE_OP, STORE_FAKE):
            for m in rx.finditer(text):
                names.add(m.group(1))
        for h in sorted(names):
            out.setdefault(h, []).append(name)
    return out


def cross_tick_tags():
    """Tags added in one function and removed in another -- they survive ticks.

    Those are the ones a second player can also be carrying, so every
    unbounded `@a[tag=...]`/`@e[tag=...]` against them is suspect.
    """
    added, removed, same = {}, {}, set()
    for name in all_funcs():
        text = body(name)
        for m in re.finditer(r"^tag (@\S+) add (\S+)", text, re.M):
            added.setdefault(m.group(2), set()).add(name)
        for m in re.finditer(r"^tag (@\S+) remove (\S+)", text, re.M):
            removed.setdefault(m.group(2), set()).add(name)
        for m in re.finditer(r"tag @s add (\S+)", text):
            if ("tag @s remove " + m.group(1)) in text:
                same.add(m.group(1))
    out = []
    for t in sorted(set(added) | set(removed)):
        if t in same:
            continue                     # born and buried in one call: safe
        if not t.startswith(("rpg.", "devil", "boss")):
            continue
        out.append((t, sorted(added.get(t, ())), sorted(removed.get(t, ()))))
    return out


GUARDED = re.compile(r"@a\[[^\]]*(?:scores=|tag=)")


def scaling():
    """Cost as a function of player count.

    Only the *unconditional* `execute as @a` lines scale -- a line gated on a
    score or a tag costs one selector evaluation per player and nothing more
    unless that player is actually doing the thing.  Those are the ones worth
    knowing about before a server fills up.
    """
    tick = reachable_from("command/tick") | reachable_from("command/index")
    always, gated = [], []
    for name in sorted(tick):
        try:
            text = body(name)
        except IOError:
            continue
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            m = re.match(r"execute as (@a\[[^\]]*\]|@a).*run function rpg:([\w/]+)", line)
            if not m:
                continue
            walks = 0
            for sname in reachable_from(m.group(2)):
                try:
                    t = body(sname)
                except IOError:
                    continue
                for l in t.split("\n"):
                    if not l.strip().startswith("#"):
                        walks += len(WALK.findall(l))
            row = (name, m.group(2), walks)
            (gated if GUARDED.search(m.group(1)) else always).append(row)
    return always, gated


def main():
    always, gated = scaling()
    print("=" * 78)
    print("0. what one more player costs")
    print("=" * 78)
    print("  unconditional per-player entry points (paid by every player, every tick):")
    tot = 0
    for name, fn, walks in always:
        tot += walks
        print("    %-44s walks=%d" % (name + " -> " + fn, walks))
    print("  -> %d world walk(s) per online player per tick" % tot)
    print("  gated per-player entry points (one selector test each, "
          "body only when active): %d" % len(gated))
    print()
    print("=" * 78)
    print("1. per-player tick cost -- these are paid once per online player")
    print("=" * 78)
    for walks, typed, host, fn, size in per_player_cost()[:14]:
        print("  %-42s walks=%-4d typed=%-4d  (%d fn)" % (host + " -> " + fn, walks, typed, size))

    print()
    print("=" * 78)
    print("2. @a[tag=...] with no distance -- reaches the whole world")
    print("=" * 78)
    rows = unbounded_player_picks()
    for name, i, sel, line in rows[:40]:
        print("  %-46s:%-4d %s" % (name, i, sel))
    print("  ... %d total" % len(rows))

    print()
    print("=" * 78)
    print("2b. @p nearest-player ownership decisions")
    print("=" * 78)
    rows = nearest_player_uses()
    for name, i, sel, line in rows[:60]:
        print("  %-46s:%-4d %-42s %s" % (name, i, sel, line))
    print("  ... %d total" % len(rows))

    print()
    print("=" * 78)
    print("3. shared fake-player scratch cells")
    print("=" * 78)
    for h, users in sorted(shared_scratch().items()):
        if len(users) > 1 or True:
            print("  %-16s %s" % (h, ", ".join(users[:4]) + (" ..." if len(users) > 4 else "")))

    print()
    print("=" * 78)
    print("4. tags that survive across ticks (a second player can carry them too)")
    print("=" * 78)
    for t, a, r in cross_tick_tags():
        print("  %-22s add:%-34s remove:%s" % (t, ",".join(a)[:34], ",".join(r)[:30]))


if __name__ == "__main__":
    main()
