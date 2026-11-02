# -*- coding: utf-8 -*-
"""Guard the single palette (ART-STYLE.md §1.6).

Fails the build when the palette itself breaks its own rules (a text colour
below 4.5:1 on the tooltip ground, or two colours of one family too close),
or when any item name or lore in the built pack still carries a pillar's old
colour.  Hex literals left in generators are reported as *warnings* for now:
the long tail (the 2023 weapon restyles in modernize_legacy_*.py, ritual tool
accents) is still being migrated, and the spec turns this into a failure once
it reaches zero.
"""

import io
import os
import re
import sys

import polish_ui
import rpg_ui_style as ui

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
HERE = os.path.dirname(os.path.abspath(__file__))
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
COLOUR_KEY = re.compile(r'"color"\s*:\s*"(#[0-9A-Fa-f]{6})"')


def registered():
    out = set()
    for value in vars(ui).values():
        if isinstance(value, str) and HEX.fullmatch(value):
            out.add(value.upper())
    for p in ui.PILLARS:
        out.update((p["deep"].upper(), p["lit"].upper()))
    out.update(v.upper() for v in ui.SEPHIROT.values())
    out.update(v.upper() for v in ui.NAMED.values())
    out.update((ui.NAMELESS["deep"].upper(), ui.NAMELESS["lit"].upper()))
    out.update(c.upper() for _t, c in ui.TIERS.values() if c)
    return out


def main():
    problems = ui.self_check()

    legacy = set()
    for slug, values in ui.PILLAR_LEGACY.items():
        legacy.update(v.upper() for v in values)
    legacy -= registered()
    for root, _, files in os.walk(os.path.join(DP, "data")):
        for name in files:
            if not name.endswith(".mcfunction"):
                continue
            text = io.open(os.path.join(root, name), encoding="utf-8").read()
            # book pages are light paper: dark ink there is correct
            for lo, hi in reversed(polish_ui.book_spans(text)):
                text = text[:lo] + text[hi:]
            for found in COLOUR_KEY.findall(text):
                if found.upper() in legacy:
                    problems.append("%s: 七柱旧色 %s 仍在写字" % (name, found))
                    break

    known = registered()
    loose = {}
    for name in sorted(os.listdir(HERE)):
        if (not name.endswith(".py") or name in ("rpg_ui_style.py", "check_ui_palette.py")
                or name.startswith("check_")):
            continue
        text = io.open(os.path.join(HERE, name), encoding="utf-8").read()
        found = [h for h in HEX.findall(text) if h.upper() not in known]
        if found:
            loose[name] = len(found)

    if problems:
        raise SystemExit("色板检查失败：\n" + "\n".join(problems[:30]))
    print("palette: self-check ok, no pillar legacy colour in built text")
    if loose:
        print("palette: [warn] %d generators still spell %d unregistered hex literals: %s" % (
            len(loose), sum(loose.values()),
            ", ".join("%s=%d" % kv for kv in sorted(loose.items(), key=lambda kv: -kv[1]))))


if __name__ == "__main__":
    main()
