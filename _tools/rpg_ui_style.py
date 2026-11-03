# -*- coding: utf-8 -*-
"""Shared visual language for the TRALANCER RPG pack -- the single source.

ART-STYLE.md states the rules; this module holds every number those rules
refer to.  Generators, the codex, the HUD bake and the particle writers import
from here instead of spelling hex literals.

The pack deliberately uses a small semantic palette and a predictable text
hierarchy:

* square-bracket prefixes are bold and carry the tier / pillar / system
  colour; the actual item name is never bold and is always white;
* lore is non-italic, framed by the pack's thin ASCII rule;
* instructions and explanations are gray, while only system nouns and skill
  names receive accent colours;
* every text colour reads at >= 4.5:1 on the vanilla tooltip ground #100010.
  The seven pillars therefore come in pairs: a *deep* identity colour that
  never carries text, and a *lit* colour for text and particle highlights.

Keep this module presentation-only.  Gameplay generators may import it, but
no score, timing, damage or item identity belongs here.
"""

import colorsys
import json
import math


# ---------------------------------------------------------------------------
# Neutral and semantic colours (ART-STYLE.md §1.1, §1.2)
# ---------------------------------------------------------------------------
WHITE = "#FFFFFF"
GRAY = "gray"
DARK_GRAY = "dark_gray"          # disabled states only -- 2.7:1, never prose
# Secondary lore lines (fine print under a skill).  dark_gray lifted just
# enough to read at 4.5:1 -- the same value polish_ui lifts dark_gray to.
MUTED = "#797979"

HOLY = "#FFD85A"                 # exorcism, clergy, the sacred side of a rite
HOLY_LIGHT = "#FFF2A8"
HOLY_DARK = "#D4AF37"            # [档案], 旧约
RITUAL = "#D596F2"               # [秘仪], [源质], Kabbalah
CYAN = "#62D9E8"                 # 新约, 权柄
CYAN_LIGHT = "#E8F4FF"
READY = "#70DB70"
WARN = "#FF6B5E"                 # failure, danger, critical
PASSION = "#FF3300"              # the [神圣] tier only: relics of the Passion

# Old name kept so existing imports keep working.  It used to be #FF3300,
# which made "danger" and the holy tier the same colour.
RED = WARN

RULE_TEXT = "+------------------+"

# Vanilla named colours, for contrast maths on components that use names.
NAMED = {
    "white": "#FFFFFF", "gray": "#AAAAAA", "dark_gray": "#555555",
    "black": "#000000", "gold": "#FFAA00", "yellow": "#FFFF55",
    "aqua": "#55FFFF", "dark_aqua": "#00AAAA", "green": "#55FF55",
    "dark_green": "#00AA00", "red": "#FF5555", "dark_red": "#AA0000",
    "blue": "#5555FF", "dark_blue": "#0000AA", "light_purple": "#FF55FF",
    "dark_purple": "#AA00AA",
}
TOOLTIP_GROUND = "#100010"


# ---------------------------------------------------------------------------
# Tiers (§1.3).  key -> (prefix tag, prefix colour)
# ---------------------------------------------------------------------------
TIERS = {
    "brave": ("[勇者]", "#00AAAA"),
    "epic": ("[史诗]", "#B85CF0"),
    "legend": ("[传说]", "#FFAA00"),
    "limited": ("[限定]", "#FFD700"),
    "holy": ("[神圣]", PASSION),
    "devil": ("[恶魔]", None),       # coloured by the owning pillar
}

# Every spelling the pack has ever used for a prefix -> canonical tag.
# Tier spellings resolve to a tier key; system / material spellings resolve
# straight to the canonical tag (their colour is left to the generator).
TAG_ALIASES = {
    "[brave]": "brave", "[barve]": "brave", "[勇者]": "brave",
    "[epic]": "epic", "[史诗]": "epic",
    "[legend]": "legend", "[传说]": "legend",
    "[LTD]": "limited", "[限定传说]": "limited", "[l·legend]": "limited",
    "[限定]": "limited",
    "[HOLY]": "holy", "[神圣]": "holy",
    "[DEVIL]": "devil", "[恶魔]": "devil",
}
MATERIAL_TAGS = {
    "[🧪]": "[附魔]",        # the 24 touchstones
    "[🗡]": "[锻造]",        # blank, pig iron, smelting stones
    "[item]": "[货币]",      # gold, diamond
    "[currency]": "[货币]",
}


# System prefixes take a semantic colour, never a tier colour.
SYSTEM_TAGS = {
    "[驱魔]": HOLY, "[秘仪]": RITUAL, "[源质]": RITUAL, "[档案]": HOLY_DARK,
}


def tier_tag(key):
    return TIERS[key][0]


def tier_colour(key):
    return TIERS[key][1]


# ---------------------------------------------------------------------------
# The seven pillars (§1.4)
# ---------------------------------------------------------------------------
# deep: identity -- covers, particle shadow end, codex washes.  Never text.
# lit:  text, HUD prompts, particle highlight end.
# mote: the vanilla particle that gives each lord its texture.
PILLARS = [
    dict(n=1, slug="lucifer", who="路西法", sin="傲慢",
         deep="#00491C", lit="#5FD68C", mote="end_rod"),
    dict(n=2, slug="leviathan", who="利维坦", sin="嫉妒",
         deep="#1B4F72", lit="#4F9EF0", mote="nautilus"),
    dict(n=3, slug="abaddon", who="亚巴顿", sin="怠惰",
         deep="#6A6A70", lit="#A7AFC9", mote="sculk_soul"),
    dict(n=4, slug="beelzebub", who="别西卜", sin="暴食",
         deep="#5A6B1E", lit="#B5D957", mote="spore_blossom_air"),
    dict(n=5, slug="samael", who="萨麦尔", sin="暴怒",
         deep="#7B241C", lit="#FF5C52", mote="soul_fire_flame"),
    dict(n=6, slug="belial", who="贝利尔", sin="色欲",
         deep="#5B2C6F", lit="#D97AD9", mote="witch"),
    dict(n=7, slug="mammon", who="玛门", sin="贪婪",
         deep="#B7950B", lit="#E6A23C", mote="wax_on"),
]
# 无名者: the nameless lord that answers when no pillar does.  Not one of
# the seven, but it speaks on the same HUD, so it gets the same pair.
NAMELESS = dict(who="无名者", deep="#3D0000", lit="#DC4450")

_PILLAR_KEYS = {}
for _p in PILLARS:
    for _k in (_p["n"], _p["slug"], _p["who"]):
        _PILLAR_KEYS[_k] = _p


def pillar(key):
    """Look a pillar up by number, slug or Chinese name."""
    return _PILLAR_KEYS[key]


def pillar_in(text):
    """The pillar whose lord is named inside ``text``, or None."""
    for p in PILLARS:
        if p["who"] in text:
            return p
    return None


# Colours the pack used for a pillar before this table existed.  The final
# polish pass folds any of these that still carry text into the lit colour.
PILLAR_LEGACY = {
    "lucifer": ("#00491C", "#004A1C", "#72D99A", "#30D97D"),
    "leviathan": ("#1B4F72", "#123E7C", "#3DA8E8"),
    "abaddon": ("#6A6A70", "#5B5B62", "#C2C2CC", "#91919C"),
    "beelzebub": ("#5A6B1E", "#596B18", "#B8C74A"),
    "samael": ("#7B241C", "#B00057", "#FF665E", "#E34C4C"),
    "belial": ("#5B2C6F", "#57256B", "#660099", "#C28BE0", "#BF6BE8"),
    "mammon": ("#B7950B", "#987B08", "#E3BA3B"),
}


# Dust colours the pack wrote for a pillar before this table existed, as the
# float triplets that appear in commands.  ``lit`` ones become the pillar's
# lit end, ``deep`` ones its deep end; a pure-black end after a pillar colour
# also becomes the deep end (black dust vanishes at night).
PILLAR_DUST_LEGACY = {
    "lucifer": dict(lit=("0.19,0.85,0.49", "0.0,0.29,0.11", "0.45,0.85,0.6"),
                    deep=("0.0,0.18,0.07",)),
    "leviathan": dict(lit=("0.24,0.66,0.91", "0.11,0.31,0.45", "0.25,0.78,0.93"),
                      deep=("0.02,0.09,0.18", "0.02,0.16,0.31")),
    "abaddon": dict(lit=("0.57,0.57,0.61", "0.58,0.58,0.61", "0.76,0.76,0.82"),
                    deep=("0.04,0.03,0.07", "0.1,0.1,0.12")),
    "beelzebub": dict(lit=("0.72,0.78,0.29", "0.7,0.84,0.34"),
                      deep=("0.14,0.17,0.03", "0.18,0.23,0.05")),
    "samael": dict(lit=("0.89,0.3,0.3", "0.69,0.0,0.34", "0.94,0.2,0.18"),
                   deep=("0.24,0.0,0.04", "0.24,0.0,0.12", "0.25,0.01,0.01")),
    "belial": dict(lit=("0.75,0.42,0.91", "0.4,0.0,0.6", "0.36,0.17,0.44", "0.76,0.47,0.88"),
                   deep=("0.12,0.0,0.18", "0.18,0.04,0.25")),
    "mammon": dict(lit=("0.89,0.73,0.23", "1.0,0.79,0.2"),
                   deep=("0.2,0.1,0.0", "0.28,0.17,0.01")),
}


# ---------------------------------------------------------------------------
# Sub-palettes (§1.5)
# ---------------------------------------------------------------------------
# The ten Sephiroth (+ Daath).  A symbolic system of its own, not pillars.
# Binah is traditionally black; pure near-black dust vanishes at night, so it
# is drawn as a dark slate instead.
SEPHIROT = {
    "kether": "#FFFAE0", "chokmah": "#9EA3AD", "binah": "#3B3B4A",
    "daath": "#6B8FAD", "chesed": "#1F85D1", "geburah": "#C7262E",
    "tiphareth": "#F5C73B", "netzach": "#40AD47", "hod": "#EB6129",
    "yesod": "#8538AD", "malkuth": "#7A4530",
}


# ---------------------------------------------------------------------------
# Colour maths
# ---------------------------------------------------------------------------
def hex_of(colour):
    if colour in NAMED:
        return NAMED[colour]
    return "#" + colour.lstrip("#").upper()


def rgb(colour):
    """(r, g, b) floats in 0..1."""
    h = hex_of(colour).lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def from_rgb(r, g, b):
    return "#%02X%02X%02X" % tuple(int(round(max(0.0, min(1.0, c)) * 255))
                                   for c in (r, g, b))


def luminance(colour):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb(colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(colour, ground=TOOLTIP_GROUND):
    a, b = luminance(colour), luminance(ground)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def lab(colour):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb(colour))
    x = (r * .4124 + g * .3576 + b * .1805) / .95047
    y = r * .2126 + g * .7152 + b * .0722
    z = (r * .0193 + g * .1192 + b * .9505) / 1.08883

    def f(t):
        return t ** (1 / 3.0) if t > 0.008856 else 7.787 * t + 16 / 116.0
    return (116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z)))


def delta_e(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(lab(a), lab(b))))


def readable(colour, minimum=4.5):
    """Lift a colour until it reads on the tooltip ground, keeping its hue.

    Used only as a fallback for author accents that are not in any table
    (rune categories, one-off lore words).  Table colours already pass.
    """
    colour = hex_of(colour)
    if contrast(colour) >= minimum:
        return colour
    h, l, s = colorsys.rgb_to_hls(*rgb(colour))
    s = min(s, 0.75)             # fully saturated lifts read as neon
    while l < 0.95:
        l += 0.02
        lifted = from_rgb(*colorsys.hls_to_rgb(h, l, s))
        if contrast(lifted) >= minimum:
            return lifted
    return WHITE


# ---------------------------------------------------------------------------
# Particles (§6)
# ---------------------------------------------------------------------------
def floats(colour):
    """Minecraft dust colour list body: ``0.37,0.84,0.55``."""
    return ",".join(("%.2f" % c).rstrip("0").rstrip(".") if c not in (0, 1)
                    else "%.1f" % c for c in rgb(colour))


def dust(colour, scale):
    return "dust{color:[%s],scale:%s}" % (floats(colour), _num(scale))


def dust_transition(start, end, scale):
    return "dust_color_transition{from_color:[%s],to_color:[%s],scale:%s}" % (
        floats(start), floats(end), _num(scale))


def pillar_dust(key, scale):
    """Single-colour dust for a lord: always the lit end."""
    return dust(pillar(key)["lit"], scale)


def pillar_transition(key, scale):
    p = pillar(key)
    return dust_transition(p["lit"], p["deep"], scale)


def _num(value):
    return ("%.2f" % value).rstrip("0").rstrip(".")


# ---------------------------------------------------------------------------
# Text components (§2)
# ---------------------------------------------------------------------------
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


def tier_name(key, name):
    """Item name for a tier key (not 'devil' -- use devil_name)."""
    tag, colour = TIERS[key]
    return item_name(tag, name, colour)


def devil_name(key, name=None):
    p = pillar(key)
    return item_name(tier_tag("devil"), name or p["who"], p["lit"])


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


# ---------------------------------------------------------------------------
# Ritual broadcasts (§12)
# ---------------------------------------------------------------------------
# One chat line per event: "[标签] " bold, then gray prose.  The tag colour
# says who acted, so the chat column reads the fight at a glance:
#   the exorcist, tools, rite progress  HOLY
#   the demon (counter-rite, domain)    its pillar's lit
#   failure, threat, the rite slipping  WARN
#   the four verdicts                   VERDICTS
#   a sealed relic's stage              the HUD seal stages
# Bold doubles every glyph one unit to the right, which turns the vanilla
# "·" into a dash; tags join their halves with the Unifont dot "・".
TAG_JOIN = "・"
VERDICTS = {"消灭": WARN, "放逐": HOLY_LIGHT, "封印": CYAN, "契约": RITUAL}
SEAL_STAGES = {"遗物休眠": MUTED, "遗物躁动": RITUAL, "遗物危险": HOLY,
               "遗物临界": WARN, "遗物压制": CYAN, "遗物冷却": CYAN}
BROADCAST_WARN = {"仪式失败", "法阵熄灭", "恶魔挣脱", "伪名坐实", "伪名误判",
                  "嫉妒得逞", "逾期加征", "封印失败", "赎金失败"}
BROADCAST_HOLY = {"驱魔调查", "调查档案", "罪证", "镇压", "真名确证", "镇魔二阶段",
                  "罪约裁决", "裁决尚待", "驱魔完成", "驱魔师档案", "职业解锁",
                  "告解铃", "净罪香", "银质圣钉", "仪式粉笔",
                  "真名击破", "妒影击破", "银钉守界", "赎金已付"}
BROADCAST_PILLAR = {"反仪式・吞媒": "别西卜"}
# Tags shared by all seven lords; the line names the lord ("别西卜 · 司祭 巴钦").
BROADCAST_SPEAKER = {"罪群", "罪仆术式", "显形", "弱点媒介", "封印逃逸"}


def broadcast_tag(tag):
    """``[反仪式·暴食]`` -> ``反仪式・暴食``: brackets off, the join made bold-safe."""
    body = tag.strip()[1:-1]
    return TAG_JOIN.join(part.strip() for part in body.split("·"))


def broadcast_colour(tag, body=""):
    """The colour a ritual broadcast tag must carry, or None if it is not one.

    Explicit tables win over the pillar lookup: failure tags such as
    [嫉妒得逞] name a sin but belong to WARN.  ``body`` is the rest of the
    line, which names the lord for the tags in BROADCAST_SPEAKER.
    """
    key = broadcast_tag(tag)
    head, _, tail = key.partition(TAG_JOIN)
    if key in SEAL_STAGES:
        return SEAL_STAGES[key]
    if key in BROADCAST_WARN:
        return WARN
    if key in BROADCAST_HOLY:
        return HOLY
    if key in VERDICTS:
        return VERDICTS[key]
    if head == "裁决" and tail in VERDICTS:
        return VERDICTS[tail]
    if key in BROADCAST_PILLAR:
        return pillar(BROADCAST_PILLAR[key])["lit"]
    if key in BROADCAST_SPEAKER:
        speaker = pillar_in(body)
        return speaker["lit"] if speaker else None
    for p in PILLARS:
        if head == p["who"] or (head in ("反仪式", "罪域") and tail in (p["who"], p["sin"])):
            return p["lit"]
    return None


# ---------------------------------------------------------------------------
# Self-check (§1.6) -- run by check_ui_palette.py on every build
# ---------------------------------------------------------------------------
TEXT_COLOURS = dict(
    [("tier." + k, c) for k, (_t, c) in TIERS.items() if c] +
    [("pillar." + p["slug"], p["lit"]) for p in PILLARS] +
    [("HOLY", HOLY), ("HOLY_LIGHT", HOLY_LIGHT), ("HOLY_DARK", HOLY_DARK),
     ("RITUAL", RITUAL), ("CYAN", CYAN), ("CYAN_LIGHT", CYAN_LIGHT),
     ("READY", READY), ("WARN", WARN), ("PASSION", PASSION),
     ("WHITE", WHITE), ("GRAY", NAMED["gray"]), ("MUTED", MUTED),
     ("NAMELESS", NAMELESS["lit"])])

# Cross-family pairs that may sit close because they never share a slot.
ACCEPTED_NEAR = {
    frozenset(("pillar.samael", "WARN")),
    frozenset(("pillar.belial", "RITUAL")),
    frozenset(("tier.holy", "PASSION")),
}


def self_check():
    problems = []
    for name, colour in TEXT_COLOURS.items():
        if contrast(colour) < 4.5:
            problems.append("%s %s contrast %.2f < 4.5" % (name, colour, contrast(colour)))
    families = {
        "tier": {k: v for k, v in TEXT_COLOURS.items() if k.startswith("tier.")},
        "pillar": {k: v for k, v in TEXT_COLOURS.items() if k.startswith("pillar.")},
    }
    for fam, group in families.items():
        keys = sorted(group)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                d = delta_e(group[a], group[b])
                if d < 20:
                    problems.append("%s %s/%s too close (dE %.1f)" % (fam, a, b, d))
    return problems
