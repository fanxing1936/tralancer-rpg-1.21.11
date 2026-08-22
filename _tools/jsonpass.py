# -*- coding: utf-8 -*-
"""JSON-side migrations: loot tables, item modifiers, advancements, registries."""

import transform as T
from transform import bump, strip_attr_prefix, consumable_json


def fname(d):
    f = d.get("function")
    return f.split(":", 1)[-1] if isinstance(f, str) else ""


def components_pass(comps):
    """comps: {component id -> value}  (loot `set_components`, item predicates)."""
    out = {}
    extra = {}
    hidden = []
    for cid, val in comps.items():
        short = cid.split(":", 1)[-1]

        if short == "food" and isinstance(val, dict) and "eat_seconds" in val:
            secs = val.pop("eat_seconds")
            bump("food.eat_seconds -> consumable")
            extra["minecraft:consumable"] = consumable_json(secs)
            out[cid] = val
            continue

        if short == "custom_model_data" and isinstance(val, (int, float)):
            bump("custom_model_data -> floats")
            out[cid] = {"floats": [float(val)]}
            continue

        if short == "fire_resistant":
            bump("fire_resistant -> damage_resistant")
            out["minecraft:damage_resistant"] = {"types": "#minecraft:is_fire"}
            continue

        if short in ("enchantments", "stored_enchantments") and isinstance(val, dict):
            if val.get("show_in_tooltip") is False:
                hidden.append("minecraft:" + short)
            val.pop("show_in_tooltip", None)
            if isinstance(val.get("levels"), dict):
                bump("enchantments.levels flattened")
                val = val["levels"]
            out[cid] = val
            continue

        if short == "attribute_modifiers" and isinstance(val, dict):
            if val.get("show_in_tooltip") is False:
                hidden.append("minecraft:attribute_modifiers")
            val.pop("show_in_tooltip", None)
            if isinstance(val.get("modifiers"), list):
                bump("attribute_modifiers flattened")
                val = val["modifiers"]
            out[cid] = val
            continue

        if short == "dyed_color" and isinstance(val, dict):
            if val.get("show_in_tooltip") is False:
                hidden.append("minecraft:dyed_color")
            if "rgb" in val:
                bump("dyed_color flattened")
                val = val["rgb"]
            out[cid] = val
            continue

        if isinstance(val, dict) and val.get("show_in_tooltip") is False:
            hidden.append(cid if ":" in cid else "minecraft:" + cid)
            val.pop("show_in_tooltip", None)

        out[cid] = val

    out.update(extra)
    if hidden:
        bump("tooltip_display added")
        td = out.setdefault("minecraft:tooltip_display", {})
        lst = td.setdefault("hidden_components", [])
        for h in hidden:
            if h not in lst:
                lst.append(h)
    return out


def walk(node, parent_key=None):
    if isinstance(node, dict):
        # --- set_attributes: attribute ids lost their category prefix -----
        if fname(node) == "set_attributes":
            for m in node.get("modifiers", []):
                if isinstance(m, dict) and isinstance(m.get("attribute"), str):
                    new = strip_attr_prefix(m["attribute"])
                    if new != m["attribute"]:
                        bump("attribute id renamed")
                        m["attribute"] = new

        # --- set_custom_model_data: `value` is gone -----------------------
        if fname(node) == "set_custom_model_data" and "value" in node:
            bump("set_custom_model_data -> set_components")
            val = node.pop("value")
            node.clear()
            node["function"] = "minecraft:set_components"
            node["components"] = {"minecraft:custom_model_data": {"floats": [float(val)]}}

        for k, v in list(node.items()):
            if k == "components" and isinstance(v, dict):
                node[k] = components_pass(v)
                walk(node[k], k)
            else:
                walk(v, k)
        return node

    if isinstance(node, list):
        for v in node:
            walk(v, parent_key)
    return node


# ---------------------------------------------------------------------------

def advancement_pass(doc):
    disp = doc.get("display")
    if isinstance(disp, dict) and isinstance(disp.get("background"), str):
        bg = disp["background"]
        new = bg
        if new.endswith(".png"):
            new = new[:-4]
        # 1.21.5: background is a GUI sprite id, not a raw texture path
        if ":" in new:
            ns, path = new.split(":", 1)
        else:
            ns, path = "minecraft", new
        if path.startswith("textures/"):
            path = path[len("textures/"):]
        new = ns + ":" + path
        if new != bg:
            bump("advancement background -> sprite id")
            disp["background"] = new
    return doc


def trim_material_pass(doc):
    for gone in ("ingredient", "item_model_index"):
        if gone in doc:
            bump("trim_material.%s removed" % gone)
            doc.pop(gone)
    return doc
