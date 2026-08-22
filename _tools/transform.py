# -*- coding: utf-8 -*-
"""1.21 (pack_format 48)  ->  1.21.11 (pack_format 94) data pack transforms."""

import json
import re

from snbt import Str, Word, Comp, Lst, Comps, Parser, ParseError, parse_value

# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------

ATTR_PREFIXES = ("generic.", "player.", "horse.", "zombie.")

STATS = {}


def bump(key, n=1):
    STATS[key] = STATS.get(key, 0) + n


def strip_ns(name):
    return name.split(":", 1)[1] if ":" in name else name


def strip_attr_prefix(name):
    ns = ""
    body = name
    if ":" in name:
        ns, body = name.split(":", 1)
        ns += ":"
    for p in ATTR_PREFIXES:
        if body.startswith(p):
            return ns + body[len(p):]
    return name


def as_text(node):
    if isinstance(node, Str):
        return node.val
    if isinstance(node, Word):
        return node.text
    return None


def retext(node, new):
    """Return a node of the same flavour as `node` carrying text `new`."""
    if isinstance(node, Str):
        return Str(node.q, new)
    return Word(new)


NUMERIC_RE = re.compile(r"^-?\d+(\.\d+)?[bslfdBSLFD]?$")


def is_falsey(node):
    t = as_text(node)
    return t in ("false", "0", "0b", "0B")


def number_text(node):
    """Bare numeric text of a Word, without any type suffix."""
    t = as_text(node) or ""
    return t.rstrip("bslfdBSLFD")


# ----------------------------------------------------------------------------
# JSON text component  ->  SNBT node
# ----------------------------------------------------------------------------

def json_to_node(o):
    if o is None:
        return Str('"', "")
    if isinstance(o, bool):
        return Word("true" if o else "false")
    if isinstance(o, str):
        return Str('"', o)
    if isinstance(o, int):
        return Word(str(o))
    if isinstance(o, float):
        return Word(repr(o))
    if isinstance(o, list):
        return Lst("", [json_to_node(v) for v in o])
    if isinstance(o, dict):
        return Comp([(Str('"', k), json_to_node(v)) for k, v in o.items()])
    raise TypeError(type(o))


def text_component(node):
    """A text component stored as a JSON *string* becomes a real SNBT component."""
    if isinstance(node, Str):
        s = node.val.strip()
        if s[:1] in ("[", "{"):
            try:
                return json_to_node(json.loads(s))
            except ValueError:
                return node
    return node


# ----------------------------------------------------------------------------
# item components
# ----------------------------------------------------------------------------

# components whose `show_in_tooltip:false` becomes an entry in tooltip_display
TOOLTIP_OWNERS = {
    "trim", "unbreakable", "dyed_color", "enchantments", "stored_enchantments",
    "attribute_modifiers", "can_break", "can_place_on", "jukebox_playable",
}

# what `hide_additional_tooltip` used to suppress
ADDITIONAL_TOOLTIP_COMPONENTS = [
    "minecraft:potion_contents", "minecraft:written_book_content",
    "minecraft:banner_patterns", "minecraft:stored_enchantments",
    "minecraft:charged_projectiles", "minecraft:bundle_contents",
    "minecraft:container", "minecraft:instrument", "minecraft:map_id",
    "minecraft:firework_explosion", "minecraft:fireworks",
]


# `food.eat_seconds` disappeared in 1.21.5; the item now needs a `consumable`
# component.  Every field is written out explicitly so that the advancement
# predicates that exact-match this component keep matching.
CONSUMABLE_ANIMATION = "eat"
CONSUMABLE_SOUND = "minecraft:entity.generic.eat"


def consumable_node(seconds):
    return Comp([
        (Word("consume_seconds"), Word(str(seconds) + "f")),
        (Word("animation"), Str('"', CONSUMABLE_ANIMATION)),
        (Word("sound"), Str('"', CONSUMABLE_SOUND)),
        (Word("has_consume_particles"), Word("true")),
        (Word("on_consume_effects"), Lst("", [])),
    ])


def consumable_json(seconds):
    return {
        "consume_seconds": float(seconds),
        "animation": CONSUMABLE_ANIMATION,
        "sound": CONSUMABLE_SOUND,
        "has_consume_particles": True,
        "on_consume_effects": [],
    }


class Entry(object):
    """One item component, independent of block-syntax vs compound-syntax."""

    __slots__ = ("name", "value", "negated", "quoted", "namespaced", "sep")

    def __init__(self, name, value, negated=False, quoted=False,
                 namespaced=False, sep="="):
        self.name = name          # short name, no namespace
        self.value = value
        self.negated = negated
        self.quoted = quoted      # key was written as a quoted string
        self.namespaced = namespaced
        self.sep = sep            # "=" exact component, "~" item sub-predicate


def fix_modifier(mod):
    """One attribute_modifiers / set_attributes entry."""
    if not isinstance(mod, Comp):
        return
    for field in ("type", "attribute"):
        i = mod.find(field)
        if i >= 0:
            k, v = mod.items[i]
            t = as_text(v)
            if t:
                nt = strip_attr_prefix(t)
                if nt != t:
                    bump("attribute id renamed")
                mod.items[i] = (k, retext(v, nt))
    # modifier ids must be strings (resource locations), never bare numbers
    i = mod.find("id")
    if i >= 0:
        k, v = mod.items[i]
        if isinstance(v, Word):
            bump("attribute modifier id quoted")
            mod.items[i] = (k, Str('"', v.text))


def transform_entries(entries):
    """entries: list[Entry]  ->  new list[Entry] (in place semantics)."""
    hidden = []
    extra = []
    out = []

    for e in entries:
        n = e.name
        v = e.value

        if n in ("custom_name", "item_name") and v is not None:
            nv = text_component(v)
            if nv is not v:
                bump("custom_name -> SNBT")
            e.value = nv

        elif n == "lore" and isinstance(v, Lst):
            changed = False
            for idx, el in enumerate(v.items):
                nel = text_component(el)
                if nel is not el:
                    changed = True
                v.items[idx] = nel
            if changed:
                bump("lore -> SNBT")

        elif n in ("enchantments", "stored_enchantments") and isinstance(v, Comp):
            if v.has("show_in_tooltip"):
                if is_falsey(v.get("show_in_tooltip")):
                    hidden.append("minecraft:" + n)
                v.pop("show_in_tooltip")
            lv = v.get("levels")
            if isinstance(lv, Comp):
                bump("enchantments.levels flattened")
                e.value = lv

        elif n == "attribute_modifiers":
            if isinstance(v, Comp):
                if v.has("show_in_tooltip"):
                    if is_falsey(v.get("show_in_tooltip")):
                        hidden.append("minecraft:attribute_modifiers")
                    v.pop("show_in_tooltip")
                mods = v.get("modifiers")
                if isinstance(mods, Lst):
                    bump("attribute_modifiers flattened")
                    e.value = mods
            if isinstance(e.value, Lst):
                for m in e.value.items:
                    fix_modifier(m)

        elif n == "dyed_color":
            if isinstance(v, Comp):
                if v.has("show_in_tooltip"):
                    if is_falsey(v.get("show_in_tooltip")):
                        hidden.append("minecraft:dyed_color")
                    v.pop("show_in_tooltip")
                rgb = v.get("rgb")
                if rgb is not None:
                    bump("dyed_color flattened")
                    e.value = rgb

        elif n == "custom_model_data":
            if isinstance(v, Word):
                bump("custom_model_data -> floats")
                e.value = Comp([(Word("floats"), Lst("", [Word(number_text(v) + ".0f")]))])

        elif n == "fire_resistant":
            bump("fire_resistant -> damage_resistant")
            e.name = "damage_resistant"
            e.value = Comp([(Word("types"), Str('"', "#minecraft:is_fire"))])

        elif n == "food" and isinstance(v, Comp):
            secs = v.pop("eat_seconds")
            if secs is not None:
                bump("food.eat_seconds -> consumable")
                extra.append(Entry("consumable", consumable_node(number_text(secs)),
                                   quoted=e.quoted, namespaced=e.namespaced))
            # nutrition/saturation stay; normalise the float
            i = v.find("saturation")
            if i >= 0 and isinstance(v.items[i][1], Word):
                v.items[i] = (v.items[i][0], Word(number_text(v.items[i][1]) + "f"))

        elif n == "hide_additional_tooltip":
            bump("hide_additional_tooltip -> tooltip_display")
            hidden.extend(ADDITIONAL_TOOLTIP_COMPONENTS)
            continue        # component itself is gone

        elif n == "hide_tooltip":
            bump("hide_tooltip -> tooltip_display")
            extra.append(Entry("tooltip_display",
                               Comp([(Word("hide_tooltip"), Word("true"))]),
                               quoted=e.quoted, namespaced=e.namespaced))
            continue

        elif n in TOOLTIP_OWNERS and isinstance(v, Comp):
            if v.has("show_in_tooltip"):
                if is_falsey(v.get("show_in_tooltip")):
                    hidden.append("minecraft:" + n)
                v.pop("show_in_tooltip")
                bump("show_in_tooltip -> tooltip_display")

        out.append(e)

    out.extend(extra)

    if hidden:
        bump("tooltip_display added")
        proto = out[0] if out else Entry("x", None)
        existing = None
        for e in out:
            if e.name == "tooltip_display":
                existing = e
                break
        if existing is None:
            existing = Entry("tooltip_display", Comp(), quoted=proto.quoted,
                             namespaced=proto.namespaced)
            out.append(existing)
        if not isinstance(existing.value, Comp):
            existing.value = Comp()
        lst = existing.value.get("hidden_components")
        if not isinstance(lst, Lst):
            lst = Lst("", [])
            existing.value.set("hidden_components", lst)
        have = {as_text(x) for x in lst.items}
        for h in hidden:
            if h not in have:
                lst.items.append(Str('"', h))
                have.add(h)

    return out


# --- adapters ---------------------------------------------------------------

def comps_to_entries(block):
    out = []
    for name, value, neg, sep in block.entries:
        out.append(Entry(strip_ns(name), value, neg,
                         quoted=False, namespaced=name.startswith("minecraft:"),
                         sep=sep))
    return out


def entries_to_comps(entries):
    res = []
    for e in entries:
        name = ("minecraft:" + e.name) if e.namespaced else e.name
        res.append((name, e.value, e.negated, e.sep))
    return Comps(res)


def comp_to_entries(comp):
    out = []
    for k, v in comp.items:
        raw = comp.keytext(k)
        out.append(Entry(strip_ns(raw), v, False,
                         quoted=isinstance(k, Str),
                         namespaced=raw.startswith("minecraft:")))
    return out


def entries_to_comp(entries):
    items = []
    for e in entries:
        name = ("minecraft:" + e.name) if e.namespaced else e.name
        key = Str('"', name) if e.quoted else Word(name)
        items.append((key, e.value))
    return Comp(items)


# ----------------------------------------------------------------------------
# entity NBT
# ----------------------------------------------------------------------------

ARMOR_SLOTS = ["feet", "legs", "chest", "head"]
HAND_SLOTS = ["mainhand", "offhand"]


def is_blank_item(node):
    """`{}` and id-less stubs such as `{Count:1}` meant "no item" in the old
    fixed-length ArmorItems / HandItems lists.  An `equipment` slot must hold a
    real stack, so those stubs have to be dropped instead of carried over."""
    if not isinstance(node, Comp):
        return True
    return not node.has("id")


def merge_equipment(comp):
    """ArmorItems/HandItems/SaddleItem/body_armor_item -> equipment (1.21.5)."""
    eq_pairs = []
    dc_pairs = []

    armor = comp.pop("ArmorItems")
    if isinstance(armor, Lst):
        bump("ArmorItems -> equipment")
        for slot, item in zip(ARMOR_SLOTS, armor.items):
            if not is_blank_item(item):
                eq_pairs.append((slot, item))
    hands = comp.pop("HandItems")
    if isinstance(hands, Lst):
        bump("HandItems -> equipment")
        for slot, item in zip(HAND_SLOTS, hands.items):
            if not is_blank_item(item):
                eq_pairs.append((slot, item))
    saddle = comp.pop("SaddleItem")
    if saddle is not None:
        bump("SaddleItem -> equipment.saddle")
        eq_pairs.append(("saddle", saddle))
    body = comp.pop("body_armor_item")
    if body is not None:
        bump("body_armor_item -> equipment.body")
        eq_pairs.append(("body", body))

    adc = comp.pop("ArmorDropChances")
    if isinstance(adc, Lst):
        for slot, ch in zip(ARMOR_SLOTS, adc.items):
            dc_pairs.append((slot, ch))
    hdc = comp.pop("HandDropChances")
    if isinstance(hdc, Lst):
        for slot, ch in zip(HAND_SLOTS, hdc.items):
            dc_pairs.append((slot, ch))
    bdc = comp.pop("body_armor_drop_chance")
    if bdc is not None:
        dc_pairs.append(("body", bdc))

    if eq_pairs:
        eq = comp.get("equipment")
        if not isinstance(eq, Comp):
            eq = Comp()
            comp.set("equipment", eq)
        for slot, item in eq_pairs:
            eq.set(slot, item)
    if dc_pairs:
        bump("drop chances -> drop_chances")
        dc = comp.get("drop_chances")
        if not isinstance(dc, Comp):
            dc = Comp()
            comp.set("drop_chances", dc)
        for slot, ch in dc_pairs:
            dc.set(slot, ch)


# 1.21.5 moved the player's armour and offhand out of `Inventory` into the same
# `equipment` compound that every other living entity uses.
PLAYER_SLOTS = {"100": "feet", "101": "legs", "102": "chest", "103": "head",
                "-106": "offhand"}


def migrate_player_inventory(comp):
    inv = comp.get("Inventory")
    if not isinstance(inv, Lst):
        return
    keep = []
    moved = []
    for el in inv.items:
        slot = as_text(el.get("Slot")) if isinstance(el, Comp) else None
        name = PLAYER_SLOTS.get(number_text(el.get("Slot"))) if slot else None
        if name is None:
            keep.append(el)
            continue
        el.pop("Slot")
        moved.append((name, el))
    if not moved:
        return
    bump("player armour Inventory slot -> equipment")
    if keep:
        comp.set("Inventory", Lst(inv.prefix, keep))
    else:
        comp.pop("Inventory")
    eq = comp.get("equipment")
    if not isinstance(eq, Comp):
        eq = Comp()
        comp.set("equipment", eq)
    for name, el in moved:
        eq.set(name, el)


# Entity vectors are decoded strictly since 1.21.5: a short list is rejected
# outright ("Input is not a list of 3 elements") and the whole summon fails.
# The pack has 38 `Rotation:[<yaw>f]` and 10 `Motion:[x,y]` written that way.
VECTOR_ARITY = {"Motion": (3, "0d"), "Pos": (3, "0d"), "Rotation": (2, "0f")}


def pad_vectors(comp):
    for name, (size, fill) in VECTOR_ARITY.items():
        v = comp.get(name)
        if isinstance(v, Lst) and 0 < len(v.items) < size:
            bump("short %s vector padded" % name)
            v.items.extend(Word(fill) for _ in range(size - len(v.items)))


def transform_comp(comp):
    # --- item stack: Count -> count -------------------------------------
    if comp.has("id") and comp.has("Count"):
        i = comp.find("Count")
        k, v = comp.items[i]
        comp.items[i] = (Word("count"), v)
        bump("Count -> count")

    # --- CustomName is a real text component now -------------------------
    i = comp.find("CustomName")
    if i >= 0:
        k, v = comp.items[i]
        nv = text_component(v)
        if nv is not v:
            bump("CustomName -> SNBT")
        comp.items[i] = (k, nv)

    # --- entity attribute list -------------------------------------------
    attrs = comp.get("attributes")
    if isinstance(attrs, Lst):
        for a in attrs.items:
            if isinstance(a, Comp):
                i = a.find("id")
                if i >= 0:
                    k, v = a.items[i]
                    t = as_text(v)
                    if t:
                        nt = strip_attr_prefix(t)
                        if nt != t:
                            bump("attribute id renamed")
                        a.items[i] = (k, retext(v, nt))

    # --- nested component map ---------------------------------------------
    i = comp.find("components")
    if i >= 0:
        k, v = comp.items[i]
        if isinstance(v, Comp):
            comp.items[i] = (k, entries_to_comp(transform_entries(comp_to_entries(v))))

    merge_equipment(comp)
    migrate_player_inventory(comp)
    pad_vectors(comp)


def walk(node):
    """Depth-first: children first, then the node itself."""
    if isinstance(node, Comp):
        for _, v in node.items:
            walk(v)
        transform_comp(node)
    elif isinstance(node, Lst):
        for v in node.items:
            walk(v)


def transform_nbt(node):
    walk(node)
    return node


def transform_component_block(block):
    for entry in block.entries:
        if entry[3] == "~":
            return block          # item sub-predicate, not a component value
        if entry[1] is not None:
            walk(entry[1])
    return entries_to_comps(transform_entries(comps_to_entries(block)))
