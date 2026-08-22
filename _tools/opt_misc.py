# -*- coding: utf-8 -*-
"""Small targeted tick-cost fixes that don't fit the generic passes."""

import io
import os
import sys

GOLD_HEX = "#FFD700"

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

HEALTH = os.path.join(ROOT, "data", "rpg", "function", "entities",
                      "drowned", "health.mcfunction")
GUARD_NOTE = [
    "# rpg:entities/drowned/magic is a 3568-command particle circle.  Only draw it",
    "# when a player is close enough for the particles to render at all.",
]


def guard_magic_circle():
    if not os.path.isfile(HEALTH):
        return 0
    lines = io.open(HEALTH, encoding="utf-8").read().rstrip("\n").split("\n")
    out, changed = [], 0
    for line in lines:
        if "entities/drowned/magic" in line and "if entity @a" not in line:
            line = line.replace("at @s run function",
                                "at @s if entity @a[distance=..48] run function")
            changed += 1
        out.append(line)
    if changed:
        out = GUARD_NOTE + out
        io.open(HEALTH, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    return changed


def fix_belial_devil_tag():
    """贝利尔 shipped with custom_data={blil_tag:1b,sword_tag:1b} -- the only one
    of the five demons missing devil_tag, so anything keyed on the demon flag
    (rpg.h.devil_tag1) silently skipped it."""
    path = os.path.join(ROOT, "data/rpg/function/command/give/weapon.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    old = "custom_data={blil_tag:1b,sword_tag:1b}"
    new = "custom_data={blil_tag:1b,sword_tag:1b,devil_tag:1b}"
    if old not in s:
        return 0
    n = s.count(old)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
    return n


def fix_limited_legend():
    """`[l·legend]` was half English and shipped in two different colours
    (#ffcc33 on one weapon, #D84E4E on the other).  It becomes 限定传说 in a
    single gold, one step brighter than the plain 传说 tier's vanilla `gold`
    so the two stay distinguishable."""
    import glob
    n = 0
    for path in glob.glob(os.path.join(
            ROOT, "data/rpg/function/command/give/*.mcfunction")):
        s = io.open(path, encoding="utf-8").read()
        before = s
        for colour in ('"italic":false,"bold":true,"color":"#ffcc33"',
                       '"italic":false,"color":"#D84E4E","bold":true'):
            s = s.replace('{"text":"[l·legend]",' + colour + "}",
                          '{"text":"[限定传说]","italic":false,'
                          '"color":"%s","bold":true}' % GOLD_HEX)
        if s != before:
            io.open(path, "w", encoding="utf-8", newline="\n").write(s)
            n += before.count("[l·legend]")
    return n


# section heading -> the item flag nothing in it can act without
COM_GATES = [
    # 洗练 reforges a dropped weapon when a reforge stone lies on it.  34 of its
    # 42 commands name the stone outright; the rest only read a counter that
    # feeds them, so with no stone on the ground the whole section is inert.
    ("##洗练", "rpg.i.diamond_tag1", "xilian"),
    # 武器分支: every single line requires the weapon flag.
    ("##武器分支", "rpg.i.weapon_tag1", "branch"),
]


def guard_com_sections():
    """rpg:command/com runs unguarded every tick.  Two of its sections are
    forging logic that can only matter while the relevant item is lying on the
    ground -- hoist each behind one `type=minecraft:item` lookup (indexed, so
    it costs a list probe rather than a walk) and move the body to its own
    function."""
    path = os.path.join(ROOT, "data/rpg/function/command/com.mcfunction")
    lines = io.open(path, encoding="utf-8").read().split("\n")
    sdir = os.path.join(ROOT, "data/rpg/function/command/com")
    if not os.path.isdir(sdir):
        os.makedirs(sdir)

    moved = 0
    for head, tag, name in COM_GATES:
        try:
            a = next(i for i, l in enumerate(lines) if l.strip() == head)
        except StopIteration:
            continue
        b = next((i for i in range(a + 1, len(lines))
                  if lines[i].strip().startswith("##")), len(lines))
        body = lines[a + 1:b]
        if not any(l.strip() and not l.strip().startswith("#") for l in body):
            continue
        with io.open(os.path.join(sdir, name + ".mcfunction"), "w",
                     encoding="utf-8", newline="\n") as fh:
            fh.write("# 由 opt_misc.guard_com_sections 从 rpg:command/com 提出。\n"
                     "# 整段只在 %s 落在地上时才有意义，所以上层用一次\n"
                     "# type=minecraft:item 的带类型查找把它挡住 —— 行内容原样保留。\n"
                     % tag)
            fh.write("\n".join(body).strip("\n") + "\n")
        lines[a + 1:b] = [
            "execute if entity @e[type=minecraft:item,tag=%s] "
            "run function rpg:command/com/%s" % (tag, name), ""]
        moved += 1
    if moved:
        io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    return moved


if __name__ == "__main__":
    print("magic-circle proximity guards added: %d" % guard_magic_circle())
    print("com sections gated: %d" % guard_com_sections())
    print("limited-legend prefix normalised: %d" % fix_limited_legend())
    print("belial devil_tag added: %d" % fix_belial_devil_tag())
