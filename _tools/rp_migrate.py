# -*- coding: utf-8 -*-
"""TRALANCER RPG resource pack: 1.21 (pack_format 34/42) -> 1.21.11 (75.0).

Three things changed under this pack's feet between 1.21 and 1.21.11:

* 1.21.4  item models stopped honouring `overrides`; every item that switches
          model now needs an *item definition* in `assets/<ns>/items/`.
* 1.21.4  item textures moved off the `blocks` atlas onto a new `items` atlas.
* 1.21.5  armour trim textures moved from `trims/models/armor/<p>` to
          `trims/entity/humanoid/<p>` + `trims/entity/humanoid_leggings/<p>`.

Atlas and font files are *merged* across packs rather than replaced, so each
source below only declares what this pack adds.
"""

import io
import json
import os
import shutil
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "../_orig_rp"
DST = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"

STATS = {}


def bump(k, n=1):
    STATS[k] = STATS.get(k, 0) + n


def write_json(rel, doc):
    path = os.path.join(DST, rel)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def read_json(rel, root=None):
    path = os.path.join(root or DST, rel)
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# item-definition helpers
# ---------------------------------------------------------------------------

def model(m):
    return {"type": "minecraft:model", "model": m}


def cmd_dispatch(fallback, entries):
    """Switch on custom_model_data floats[0] -- the modern form of the old
    `overrides: [{predicate:{custom_model_data: N}}]` list."""
    return {
        "type": "minecraft:range_dispatch",
        "property": "minecraft:custom_model_data",
        "index": 0,
        "fallback": fallback,
        "entries": [{"threshold": t, "model": m} for t, m in entries],
    }


def bow_variant(base, pull0, pull1, pull2):
    return {
        "type": "minecraft:condition",
        "property": "minecraft:using_item",
        "on_false": model(base),
        "on_true": {
            "type": "minecraft:range_dispatch",
            "property": "minecraft:use_duration",
            "scale": 0.05,
            "fallback": model(pull0),
            "entries": [
                {"threshold": 0.65, "model": model(pull1)},
                {"threshold": 0.9, "model": model(pull2)},
            ],
        },
    }


def crossbow_variant(base, pull0, pull1, pull2, arrow, rocket):
    return {
        "type": "minecraft:select",
        "property": "minecraft:charge_type",
        "cases": [
            {"when": "arrow", "model": model(arrow)},
            {"when": "rocket", "model": model(rocket)},
        ],
        "fallback": {
            "type": "minecraft:condition",
            "property": "minecraft:using_item",
            "on_false": model(base),
            "on_true": {
                "type": "minecraft:range_dispatch",
                "property": "minecraft:crossbow/pull",
                "fallback": model(pull0),
                "entries": [
                    {"threshold": 0.58, "model": model(pull1)},
                    {"threshold": 1.0, "model": model(pull2)},
                ],
            },
        },
    }


def trim_select(fallback_model, cases):
    return {
        "type": "minecraft:select",
        "property": "minecraft:trim_material",
        "cases": [{"when": w, "model": model(m)} for w, m in cases],
        "fallback": model(fallback_model),
    }


# ---------------------------------------------------------------------------

VANILLA_TRIM_TEXTURES = [
    "sentry", "dune", "coast", "wild", "ward", "eye", "vex", "tide", "snout",
    "rib", "spire", "wayfinder", "shaper", "silence", "raiser", "host", "flow",
    "bolt",
]

# every material the custom axe trim overlay has to be generated for
AXE_TRIM_MATERIALS = [
    "quartz", "iron", "gold", "diamond", "netherite", "redstone", "copper",
    "emerald", "lapis", "amethyst", "resin",
]

# custom_model_data -> model, straight ports of the old `overrides` lists
SIMPLE_CMD = {
    "netherite_sword": ("minecraft:item/netherite_sword", [
        (1110001, "rpg:item/chainsaw_sword"), (1110002, "rpg:item/king_sword"),
        (1110003, "rpg:item/warrior_sword"), (1110004, "rpg:item/long_stick"),
        (1110005, "rpg:item/sakura_sword"), (1110006, "rpg:item/venom_glaive"),
        (1110007, "rpg:item/katana"), (1110008, "rpg:item/eternal_knife"),
        (1110009, "rpg:item/cutlass"), (1110010, "rpg:item/frost_slayer"),
    ]),
    "netherite_axe": ("minecraft:item/netherite_axe", [
        (1110001, "rpg:item/chill_gale_knife"),
        (1110002, "rpg:item/resolute_tempest_knife"),
        (1110003, "rpg:item/nightmares_bite"), (1110004, "rpg:item/feather"),
        (1110005, "rpg:item/sponge_striker"), (1110006, "rpg:item/coral_blade"),
    ]),
    "mace": ("minecraft:item/mace", [
        (1110001, "rpg:item/venom_glaive"), (1110002, "rpg:item/jailors_scythe"),
        (1110003, "rpg:item/king_sword"), (1110004, "rpg:item/long_stick"),
        (1110005, "rpg:item/whispering_spear"), (1110006, "rpg:item/frost_scythe"),
    ]),
    "totem_of_undying": ("minecraft:item/totem_of_undying", [
        (1110001, "rpg:item/rooted_poppy"), (1110002, "rpg:item/s"),
        (1110003, "rpg:item/a"), (1110004, "rpg:item/b"),
        (1110005, "rpg:item/c"), (1110006, "rpg:item/d"),
    ]),
    "quartz": ("minecraft:item/quartz", [
        (1110001, "rpg:item/quartz"), (1110002, "rpg:item/amethyst_shard"),
        (1110003, "rpg:item/netherite_upgrade_smithing_template"),
    ]),
}


def build_item_definitions():
    for item, (base, entries) in SIMPLE_CMD.items():
        write_json("assets/minecraft/items/%s.json" % item,
                   {"model": cmd_dispatch(model(base),
                                          [(t, model(m)) for t, m in entries])})
        bump("item definitions written")

    # --- bow: custom_model_data x (idle / pulling stages) -------------------
    write_json("assets/minecraft/items/bow.json", {"model": cmd_dispatch(
        bow_variant("minecraft:item/bow", "minecraft:item/bow_pulling_0",
                    "minecraft:item/bow_pulling_1", "minecraft:item/bow_pulling_2"),
        [(1110001, bow_variant("rpg:item/bubble_bow",
                               "rpg:item/bubble_bow_pulling_0",
                               "rpg:item/bubble_bow_pulling_1",
                               "rpg:item/bubble_bow_pulling_2"))])})
    bump("item definitions written")

    # --- crossbow: custom_model_data x (charge type / pulling stages) -------
    write_json("assets/minecraft/items/crossbow.json", {"model": cmd_dispatch(
        crossbow_variant("minecraft:item/crossbow",
                         "minecraft:item/crossbow_pulling_0",
                         "minecraft:item/crossbow_pulling_1",
                         "minecraft:item/crossbow_pulling_2",
                         "minecraft:item/crossbow_arrow",
                         "minecraft:item/crossbow_firework"),
        [
            (1110001, crossbow_variant("rpg:item/crossbow_standby",
                                       "rpg:item/crossbow_pulling_0",
                                       "rpg:item/crossbow_pulling_1",
                                       "rpg:item/crossbow_pulling_2",
                                       "rpg:item/crossbow_arrow",
                                       "rpg:item/crossbow_firework")),
            (1110002, crossbow_variant("rpg:item/soul_hunter/crossbow_standby",
                                       "rpg:item/soul_hunter/crossbow_pulling_0",
                                       "rpg:item/soul_hunter/crossbow_pulling_1",
                                       "rpg:item/soul_hunter/crossbow_pulling_2",
                                       "rpg:item/soul_hunter/crossbow_arrow",
                                       "rpg:item/soul_hunter/crossbow_firework")),
        ])})
    bump("item definitions written")

    # --- iron_axe: the pack's custom trimmable item ------------------------
    cases = [("minecraft:" + m, "rpg:item/iron_axe_%s_trim" % m)
             for m in AXE_TRIM_MATERIALS]
    cases.append(("rpg:holy", "rpg:item/iron_axe_holy_trim"))
    write_json("assets/minecraft/items/iron_axe.json",
               {"model": trim_select("minecraft:item/iron_axe", cases)})
    bump("item definitions written")


def build_axe_trim_models():
    """The old pack shipped 9 of the 12 axe trim models; `trim_type` fell
    through to a neighbouring material for the rest.  `select` has no such
    fallthrough, so fill in the gaps -- they are one-line texture swaps."""
    for mat in AXE_TRIM_MATERIALS + ["holy"]:
        rel = "assets/rpg/models/item/iron_axe_%s_trim.json" % mat
        if os.path.exists(os.path.join(DST, rel)):
            continue
        write_json(rel, {
            "parent": "rpg:item/sword_handheld",
            "textures": {
                "layer0": "minecraft:item/iron_axe",
                "layer1": "rpg:trims/items/axe_trim_%s" % mat,
            },
        })
        bump("axe trim models added")


def build_chestplate_definition(jar_items):
    """Vanilla's own trim select, plus the pack's `holy` case.

    The old pack keyed holy off `trim_type: 1.1`, which the material's
    item_model_index (0.45) could never produce -- so the holy chestplate icon
    never actually showed.  `select` matches the material by id, so it works."""
    doc = json.loads(jar_items["assets/minecraft/items/netherite_chestplate.json"])
    node = doc["model"]
    node["cases"].append({"when": "rpg:holy",
                          "model": model("rpg:item/netherite_chestplate_holy_trim")})
    write_json("assets/minecraft/items/netherite_chestplate.json", doc)
    bump("item definitions written")


def build_atlases():
    # worn armour trims: 1.21.5 texture layout
    textures = []
    for p in VANILLA_TRIM_TEXTURES:
        textures.append("minecraft:trims/entity/humanoid/%s" % p)
        textures.append("minecraft:trims/entity/humanoid_leggings/%s" % p)
    write_json("assets/minecraft/atlases/armor_trims.json", {"sources": [{
        "type": "minecraft:paletted_permutations",
        "textures": textures,
        "palette_key": "minecraft:trims/color_palettes/trim_palette",
        "permutations": {"holy": "rpg:trims/color_palettes/holy"},
    }]})
    bump("atlases rewritten")

    # item icons: since 1.21.4 these live on the `items` atlas, not `blocks`
    vanilla_items = ["helmet", "chestplate", "leggings", "boots"]
    write_json("assets/minecraft/atlases/items.json", {"sources": [
        {
            "type": "minecraft:paletted_permutations",
            "textures": ["minecraft:trims/items/%s_trim" % i for i in vanilla_items],
            "palette_key": "minecraft:trims/color_palettes/trim_palette",
            "permutations": {"holy": "rpg:trims/color_palettes/holy"},
        },
        {
            "type": "minecraft:paletted_permutations",
            "textures": ["rpg:trims/items/axe_trim"],
            "palette_key": "minecraft:trims/color_palettes/trim_palette",
            "permutations": dict(
                [(m, "minecraft:trims/color_palettes/%s" % m) for m in AXE_TRIM_MATERIALS]
                + [("holy", "rpg:trims/color_palettes/holy")]),
        },
    ]})
    bump("atlases rewritten")

    old_blocks = os.path.join(DST, "assets/minecraft/atlases/blocks.json")
    if os.path.exists(old_blocks):
        os.remove(old_blocks)
        bump("stale blocks atlas removed")


def strip_overrides():
    """`overrides` has been dead since 1.21.4 -- drop it so the model files
    say what they actually do."""
    root = os.path.join(DST, "assets")
    for dirpath, _d, names in os.walk(root):
        for fn in names:
            if not fn.endswith(".json") or os.sep + "models" + os.sep not in dirpath + os.sep:
                continue
            path = os.path.join(dirpath, fn)
            doc = json.load(io.open(path, encoding="utf-8"))
            if isinstance(doc, dict) and "overrides" in doc:
                doc.pop("overrides")
                with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(doc, fh, ensure_ascii=False, indent=2)
                    fh.write("\n")
                bump("dead `overrides` blocks removed")


RENAMES = [
    # 1.21 renamed the armour glint texture
    ("assets/minecraft/textures/misc/enchanted_glint_entity.png",
     "assets/minecraft/textures/misc/enchanted_glint_armor.png"),
]
# pre-1.20 leftovers that no vanilla path matches any more
DEAD = [
    "assets/minecraft/textures/misc/enchanted_item_glint.png",
    "assets/minecraft/textures/misc/enchanted_item_glint.png.mcmeta",
]
# image editor / model editor working files -- never read by the game
JUNK_EXT = (".pdn", ".bbmodel")


def tidy_textures():
    for old, new in RENAMES:
        o = os.path.join(DST, old)
        if os.path.exists(o):
            shutil.move(o, os.path.join(DST, new))
            bump("textures renamed for 1.21.11")
    for rel in DEAD:
        p = os.path.join(DST, rel)
        if os.path.exists(p):
            os.remove(p)
            bump("dead texture overrides removed")
    for dirpath, _d, names in os.walk(DST):
        for fn in names:
            if fn.endswith(JUNK_EXT):
                os.remove(os.path.join(dirpath, fn))
                bump("editor source files removed")


def main():
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    jar = sys.argv[3] if len(sys.argv) > 3 else (
        "F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar")
    import zipfile
    z = zipfile.ZipFile(jar)
    jar_items = {"assets/minecraft/items/netherite_chestplate.json":
                 z.read("assets/minecraft/items/netherite_chestplate.json")}

    write_json("pack.mcmeta", {"pack": {
        "description": "TRALANCER RPG!",
        "pack_format": 75,
        "min_format": [75, 0],
        "max_format": 75,
    }})

    build_item_definitions()
    build_chestplate_definition(jar_items)
    build_axe_trim_models()
    build_atlases()
    strip_overrides()
    tidy_textures()

    for k in sorted(STATS):
        print("  %-38s %d" % (k, STATS[k]))


if __name__ == "__main__":
    main()
