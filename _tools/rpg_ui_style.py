# -*- coding: utf-8 -*-
"""Shared native-text UI grammar for the TRALANCER RPG pack.

The pack deliberately uses a small semantic palette and a predictable text
hierarchy:

* square-bracket prefixes are bold; the actual item name is never bold;
* lore is non-italic, framed by the pack's thin ASCII rule;
* instructions and explanations are gray, while only system nouns and skill
  names receive accent colours;
* sacred, ritual and covenant text reuse colours already present in the
  exorcism tools, verdict UI and player panel.

Keep this module presentation-only.  Gameplay generators may import it, but
no score, timing, damage or item identity belongs here.
"""

import json


# Existing pack palette.  Do not create near-duplicate shades in generators.
WHITE = "#FFFFFF"
GRAY = "gray"
DARK_GRAY = "dark_gray"
RED = "#FF3300"

HOLY = "#FFD85A"
HOLY_LIGHT = "#FFF2A8"
HOLY_DARK = "#D4AF37"
RITUAL = "#D596F2"
CYAN = "#62D9E8"
CYAN_LIGHT = "#E8F4FF"
READY = "#70DB70"

RULE_TEXT = "+------------------+"


def comp(text, color=WHITE, bold=False, italic=False, **extra):
    """Return one explicit Minecraft text component."""
    value = {
        "text": text,
        "color": color,
        "bold": bool(bold),
        "italic": bool(italic),
    }
    value.update(extra)
    return value


def row_value(*parts):
    return [""] + list(parts)


def row(*parts):
    return json.dumps(row_value(*parts), ensure_ascii=False,
                      separators=(",", ":"))


def item_name(prefix, name, prefix_color, name_color=WHITE):
    """Pack-standard item name: bold category prefix + non-bold proper name."""
    return row(comp(prefix, prefix_color, True),
               comp(name, name_color, False))


def lore_value(rows):
    rule = row_value(comp(RULE_TEXT, WHITE))
    return [rule] + [row_value(*parts) for parts in rows] + [rule]


def lore(rows):
    return json.dumps(lore_value(rows), ensure_ascii=False,
                      separators=(",", ":"))


def label(text, glyph="🜏"):
    """Section label matching the seven-pillar contract lore hierarchy."""
    return comp(glyph + text, WHITE, True)


def prefix_message(prefix, prefix_color, text, text_color=GRAY):
    return row(comp(prefix, prefix_color, True), comp(text, text_color))
