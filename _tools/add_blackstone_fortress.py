# -*- coding: utf-8 -*-
"""Generate the Blackstone Fortress jigsaw structure for dimension `rpg:paradise_lost`.

Usage (from `_tools/`):
    python add_blackstone_fortress.py ../rpg

Depends ONLY on files inside this repository (`_tools/fortress_ref/pieces/*.nbt`,
`_tools/fortress_ref/pieces/extract_meta.json`, `_tools/fortress_ref/nbt.py`).
No running game or external packages required.

Outputs:
    rpg/data/rpg/structure/paradise/fortress/*.nbt
    rpg/data/rpg/worldgen/processor_list/paradise/fortress.json
    rpg/data/rpg/worldgen/template_pool/paradise/fortress/*.json
    rpg/data/rpg/worldgen/structure/paradise/fortress.json
    rpg/data/rpg/worldgen/structure_set/paradise/fortress.json
    rpg/data/rpg/loot_table/paradise/fortress_chest.json
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.join(HERE, "fortress_ref")
PIECES_DIR = os.path.join(REF_DIR, "pieces")
if REF_DIR not in sys.path:
    sys.path.insert(0, REF_DIR)

import nbt

DATA_VERSION = 4671
NS = "rpg"
SUB = "paradise/fortress"
PILLAR_EXTEND = 136   # 用户 2026-11-24：落差约 100 格（桥面 = 地表 + START_HEIGHT_OFFSET + PILLAR_EXTEND + 4）
PILLAR_PIECES = ("nebs", "nebcr", "nece", "nebef")

# Jigsaw tuning parameters (validated against 20 generated fortresses on 1.21.11)
JIGSAW_MAX_DEPTH = 11   # 规模加大（原 10 层、96 格）；再深城堡走廊会指数膨胀，生成卡死
JIGSAW_MAX_DIST = 128
# nebcr_start has 16-block pillars underneath; deck surface is at template y = 20
# (orig y=4 + 16). With WORLD_SURFACE_WG + start_height=-12, deck sits at ground + 8
# and pillar bottoms reach ground - 12 (sinking cleanly into mud and water basins).
START_HEIGHT_OFFSET = -40
BRIDGE_TIERS = 6

# Doorway definitions for all 14 South-facing (O=0) pieces in ORIGINAL (pre-pillar)
# local coordinates. Verified directly against the extracted 1.21.11 piece faces.
#
# Coordinate convention for O=0 (South-facing):
#   -Z (z=0):      north_up (Entrance)
#   +Z (z=sz-1):   south_up (Front exit F)
#   -X (x=0):      west_up  (Right when facing South)
#   +X (x=sx-1):   east_up  (Left when facing South)
#
# Note on differences from rough source-code table (all verified on real O=0 NBT):
#   - nesr:   upper exit is on x=6 (east_up), not x=0 (x=0 is a barred window)
#   - nescrt: corridor turn opens on x=4 (east_up), not x=0 (O=0 mirrored local X)
#   - nesclt: corridor turn opens on x=0 (west_up), not x=4 (O=0 mirrored local X)
#   - nectb:  side openings are centered at z=2 (x=0 and x=8), y=0
PIECE_DOORS = {
    "nebs": {
        "in": (2, 3, 0, "north_up"),
        "out": [(2, 3, 18, "south_up", "bridge")],
    },
    "nebcr": {
        "in": (9, 3, 0, "north_up"),
        "out": [
            (9, 3, 18, "south_up", "bridge"),
            (0, 3, 9, "west_up", "bridge"),
            (18, 3, 9, "east_up", "bridge"),
        ],
    },
    "nerc": {
        "in": (3, 0, 0, "north_up"),
        "out": [
            (3, 0, 6, "south_up", "bridge"),
            (0, 0, 3, "west_up", "bridge"),
            (6, 0, 3, "east_up", "bridge"),
        ],
    },
    "nesr": {
        "in": (3, 0, 0, "north_up"),
        "out": [(6, 6, 3, "east_up", "bridge")],
    },
    "nemt": {
        "in": (3, 0, 0, "north_up"),
        "out": [],
    },
    "nece": {
        "in": (6, 3, 0, "north_up"),
        "out": [(6, 3, 12, "south_up", "castle")],
    },
    "nesc": {
        "in": (2, 0, 0, "north_up"),
        "out": [(2, 0, 4, "south_up", "castle")],
    },
    "nescsc": {
        "in": (2, 0, 0, "north_up"),
        "out": [
            (2, 0, 4, "south_up", "castle"),
            (0, 0, 2, "west_up", "castle"),
            (4, 0, 2, "east_up", "castle"),
        ],
    },
    "nescrt": {
        "in": (2, 0, 0, "north_up"),
        "out": [(4, 0, 2, "east_up", "castle")],
    },
    "nesclt": {
        "in": (2, 0, 0, "north_up"),
        "out": [(0, 0, 2, "west_up", "castle")],
    },
    "neccs": {
        "in": (2, 7, 0, "north_up"),
        "out": [(2, 0, 9, "south_up", "castle")],
    },
    "nectb": {
        "in": (4, 0, 0, "north_up"),
        "out": [
            (0, 0, 2, "west_up", "castle"),
            (8, 0, 2, "east_up", "castle"),
        ],
    },
    "necsr": {
        "in": (6, 3, 0, "north_up"),
        "out": [
            (6, 3, 12, "south_up", "castle"),
            (6, 11, 12, "south_up", "castle"),
        ],
    },
    "nebef": {
        "in": (2, 3, 0, "north_up"),
        "out": [],
    },
}

CONNECT_NAME = "%s:fortress_connect" % NS


def _write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def _load_ref_piece(pid):
    doc = nbt.read_file(os.path.join(PIECES_DIR, pid + ".nbt"))
    sx, sy, sz = [v.value for v in doc["size"]]
    pal = []
    for p in doc["palette"]:
        name = p["Name"].value
        props = {}
        if "Properties" in p:
            for k, v in p["Properties"].items():
                props[k] = v.value
        pal.append((name, props))
    grid = {}
    for b in doc["blocks"]:
        px, py, pz = [v.value for v in b["pos"]]
        name, props = pal[b["state"].value]
        be = b["nbt"] if "nbt" in b else None
        grid[(px, py, pz)] = (name, dict(props), be)
    return (sx, sy, sz), grid


def _is_full_solid_above(name):
    return name in (
        "minecraft:nether_bricks",
        "minecraft:polished_blackstone_bricks",
        "minecraft:soul_sand",
    )


def _convert_fence_to_wall(pos, props, orig_grid):
    """Convert minecraft:nether_brick_fence state to minecraft:polished_blackstone_brick_wall."""
    x, y, z = pos
    above = orig_grid.get((x, y + 1, z))
    above_name = above[0] if above else "minecraft:air"
    above_props = above[1] if above else {}
    above_full = _is_full_solid_above(above_name)
    above_fence = (above_name == "minecraft:nether_brick_fence")

    wall = {}
    connected = {}
    for d in ("north", "south", "east", "west"):
        conn = (props.get(d, "false") == "true")
        connected[d] = conn
        if not conn:
            wall[d] = "none"
        else:
            if above_full or (above_fence and above_props.get(d, "false") == "true"):
                wall[d] = "tall"
            else:
                wall[d] = "low"

    # Vanilla WallBlock post rule: straight 2-way line has up=false unless the block
    # above forces a post (e.g. a wall/fence post directly above); isolated bars,
    # ends, T-junctions, corners and 4-way crosses keep up=true.
    straight_ns = connected["north"] and connected["south"] and not connected["east"] and not connected["west"]
    straight_ew = connected["east"] and connected["west"] and not connected["north"] and not connected["south"]
    if straight_ns or straight_ew:
        wall["up"] = "false"
    else:
        wall["up"] = "true"
    wall["waterlogged"] = props.get("waterlogged", "false")
    return wall


def _make_blaze_spawner_nbt():
    entity = nbt.Compound()
    entity["id"] = nbt.String("minecraft:blaze")
    entity["Health"] = nbt.Float(40.0)
    entity["Tags"] = nbt.List(nbt.TAG_STRING, [nbt.String("rpg.pl")])
    attr_hp = nbt.Compound()
    attr_hp["id"] = nbt.String("minecraft:max_health")
    attr_hp["base"] = nbt.Double(40.0)
    attr_atk = nbt.Compound()
    attr_atk["id"] = nbt.String("minecraft:attack_damage")
    attr_atk["base"] = nbt.Double(9.0)
    entity["attributes"] = nbt.List(nbt.TAG_COMPOUND, [attr_hp, attr_atk])

    spawn_data = nbt.Compound()
    spawn_data["entity"] = entity

    sp = nbt.Compound()
    sp["id"] = nbt.String("minecraft:mob_spawner")
    sp["SpawnData"] = spawn_data
    sp["SpawnPotentials"] = nbt.List(nbt.TAG_COMPOUND)
    sp["Delay"] = nbt.Short(20)
    sp["MinSpawnDelay"] = nbt.Short(200)
    sp["MaxSpawnDelay"] = nbt.Short(800)
    sp["SpawnCount"] = nbt.Short(4)
    sp["MaxNearbyEntities"] = nbt.Short(6)
    sp["RequiredPlayerRange"] = nbt.Short(16)
    sp["SpawnRange"] = nbt.Short(4)
    return sp


def _make_chest_nbt():
    ch = nbt.Compound()
    ch["id"] = nbt.String("minecraft:chest")
    ch["LootTable"] = nbt.String("%s:paradise/fortress_chest" % NS)
    return ch


def _format_final_state(name, props):
    if not props:
        return name
    kv = ",".join("%s=%s" % (k, v) for k, v in sorted(props.items()))
    return "%s[%s]" % (name, kv)


def _make_jigsaw_nbt(name, target, pool, final_state):
    j = nbt.Compound()
    j["id"] = nbt.String("minecraft:jigsaw")
    j["name"] = nbt.String(name)
    j["target"] = nbt.String(target)
    j["pool"] = nbt.String(pool)
    j["final_state"] = nbt.String(final_state)
    j["joint"] = nbt.String("rollable")
    j["selection_priority"] = nbt.Int(0)
    j["placement_priority"] = nbt.Int(0)
    return j


def convert_piece(pid, meta):
    """Load vanilla O=0 piece, swap blocks/BEs to blackstone theme, and add 16-block pillars if applicable."""
    (sx, sy, sz), orig_grid = _load_ref_piece(pid)
    y_off = PILLAR_EXTEND if pid in PILLAR_PIECES else 0
    new_sy = sy + y_off
    new_grid = {}

    # 1. Convert original blocks (shifted up by y_off)
    for (x, y, z), (name, props, be) in orig_grid.items():
        if name == "minecraft:nether_bricks":
            new_name, new_props, new_be = "minecraft:polished_blackstone_bricks", {}, None
        elif name == "minecraft:nether_brick_stairs":
            new_name, new_props, new_be = "minecraft:polished_blackstone_brick_stairs", dict(props), None
        elif name == "minecraft:nether_brick_fence":
            new_name = "minecraft:polished_blackstone_brick_wall"
            new_props = _convert_fence_to_wall((x, y, z), props, orig_grid)
            new_be = None
        elif name == "minecraft:nether_brick_slab":
            new_name, new_props, new_be = "minecraft:polished_blackstone_brick_slab", dict(props), None
        elif name == "minecraft:spawner":
            new_name, new_props, new_be = "minecraft:spawner", dict(props), _make_blaze_spawner_nbt()
        elif name == "minecraft:chest":
            new_name, new_props, new_be = "minecraft:chest", dict(props), _make_chest_nbt()
        else:
            # air, structure_void, soul_sand, nether_wart, lava
            if "nether_brick" in name:
                raise ValueError("Unhandled nether_brick block in %s: %s" % (pid, name))
            new_name, new_props, new_be = name, dict(props), be
        new_grid[(x, y + y_off, z)] = (new_name, new_props, new_be)

    # 2. Extend 16-block pillars underneath for nebs, nebcr, nece, nebef
    if y_off > 0:
        if pid == "nebef":
            # BridgeEndFiller does not call fillColumnDown in vanilla, so extend
            # directly beneath its jagged y=0 brick foot (x in 0..4, z in 0..2).
            pillar_cols = {
                (x, z)
                for x in range(sx)
                for z in range(sz)
                if orig_grid[(x, 0, z)][0] == "minecraft:nether_bricks"
            }
        else:
            pillar_cols = {(c[0], c[1]) for c in meta["pieces"][pid]["pillar_columns_below_bb"]}
            if not pillar_cols:
                raise RuntimeError("Missing pillar column metadata for %s" % pid)
        for py in range(y_off):
            for pz in range(sz):
                for px in range(sx):
                    if (px, pz) in pillar_cols:
                        new_grid[(px, py, pz)] = ("minecraft:polished_blackstone_bricks", {}, None)
                    else:
                        new_grid[(px, py, pz)] = ("minecraft:structure_void", {}, None)

    return (sx, new_sy, sz), y_off, new_grid


def stamp_jigsaws(pid, size, y_off, base_grid, out_pool_map, is_start=False):
    """Return a copy of base_grid with entrance/exit jigsaw blocks placed."""
    grid = dict(base_grid)
    spec = PIECE_DOORS[pid]

    def place_jig(x, y, z, orient, jname, jtarget, jpool):
        ly = y + y_off
        orig_name, orig_props, _ = grid[(x, ly, z)]
        if orig_name != "minecraft:polished_blackstone_bricks":
            raise AssertionError(
                "%s jigsaw at (%d,%d,%d) expected polished_blackstone_bricks, got %s"
                % (pid, x, ly, z, orig_name)
            )
        final_st = _format_final_state(orig_name, orig_props)
        grid[(x, ly, z)] = (
            "minecraft:jigsaw",
            {"orientation": orient},
            _make_jigsaw_nbt(jname, jtarget, jpool, final_st),
        )

    # Entrance (or 4th exit if this is nebcr_start)
    ix, iy, iz, iori = spec["in"]
    if is_start:
        place_jig(ix, iy, iz, iori, "minecraft:empty", CONNECT_NAME, out_pool_map["bridge"])
    else:
        place_jig(ix, iy, iz, iori, CONNECT_NAME, "minecraft:empty", "minecraft:empty")

    # Exits
    for ox, oy, oz, oori, kind in spec["out"]:
        place_jig(ox, oy, oz, oori, "minecraft:empty", CONNECT_NAME, out_pool_map[kind])

    return grid


def build_structure_nbt(size, grid):
    sx, sy, sz = size
    palette = []
    pal_idx = {}

    def idx_of(name, props):
        key = (name, tuple(sorted(props.items())))
        if key not in pal_idx:
            pal_idx[key] = len(palette)
            e = nbt.Compound()
            e["Name"] = nbt.String(name)
            if props:
                pc = nbt.Compound()
                for k, v in sorted(props.items()):
                    pc[k] = nbt.String(str(v))
                e["Properties"] = pc
            palette.append(e)
        return pal_idx[key]

    blocks = nbt.List(nbt.TAG_COMPOUND)
    for y in range(sy):
        for z in range(sz):
            for x in range(sx):
                name, props, be = grid[(x, y, z)]
                # Omit structure_void from output structure templates (matching vanilla
                # StructureTemplate format so JigsawPlacement leaves existing terrain/air
                # untouched instead of placing literal minecraft:structure_void blocks).
                if name == "minecraft:structure_void":
                    continue
                b = nbt.Compound()
                b["pos"] = nbt.List(nbt.TAG_INT, [nbt.Int(x), nbt.Int(y), nbt.Int(z)])
                b["state"] = nbt.Int(idx_of(name, props))
                if be is not None:
                    b["nbt"] = be
                blocks.append(b)

    root = nbt.Compound()
    root["DataVersion"] = nbt.Int(DATA_VERSION)
    root["size"] = nbt.List(nbt.TAG_INT, [nbt.Int(sx), nbt.Int(sy), nbt.Int(sz)])
    root["palette"] = nbt.List(nbt.TAG_COMPOUND, palette)
    root["blocks"] = blocks
    root["entities"] = nbt.List(nbt.TAG_COMPOUND)
    return root


def _pool_elem(loc_stem, weight, proc="%s:%s" % (NS, SUB)):
    return {
        "weight": weight,
        "element": {
            "element_type": "minecraft:single_pool_element",
            "location": "%s:%s/%s" % (NS, SUB, loc_stem),
            "processors": proc,
            "projection": "rigid",
        },
    }


def write_all(rpg_root):
    meta_path = os.path.join(PIECES_DIR, "extract_meta.json")
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)

    data_root = os.path.join(rpg_root, "data", NS)
    struct_dir = os.path.join(data_root, "structure", "paradise", "fortress")
    proc_dir = os.path.join(data_root, "worldgen", "processor_list", "paradise")
    pool_dir = os.path.join(data_root, "worldgen", "template_pool", "paradise", "fortress")
    str_def_dir = os.path.join(data_root, "worldgen", "structure", "paradise")
    ss_dir = os.path.join(data_root, "worldgen", "structure_set", "paradise")
    loot_dir = os.path.join(data_root, "loot_table", "paradise")

    # Clean old generated fortress structures/pools so re-runs stay tidy
    for d in (struct_dir, pool_dir):
        if os.path.isdir(d):
            for fn in os.listdir(d):
                os.remove(os.path.join(d, fn))
    os.makedirs(struct_dir, exist_ok=True)
    os.makedirs(pool_dir, exist_ok=True)

    # Convert all 14 base pieces once
    converted = {}
    for pid in PIECE_DOORS:
        converted[pid] = convert_piece(pid, meta)

    # Pool IDs
    P_BRIDGE = "%s:%s/bridge" % (NS, SUB)
    P_BRIDGE_MID = "%s:%s/bridge_mid" % (NS, SUB)
    P_BRIDGE_OUTER = "%s:%s/bridge_outer" % (NS, SUB)
    P_BRIDGE_TAIL = "%s:%s/bridge_tail" % (NS, SUB)
    P_CASTLE = "%s:%s/castle" % (NS, SUB)
    P_CASTLE_T2 = "%s:%s/castle_t2" % (NS, SUB)
    P_CASTLE_T3 = "%s:%s/castle_t3" % (NS, SUB)
    P_CASTLE_T4 = "%s:%s/castle_t4" % (NS, SUB)
    P_CASTLE_DEEP = "%s:%s/castle_deep" % (NS, SUB)
    P_END = "%s:%s/end" % (NS, SUB)

    def emit(out_name, pid, out_pools, is_start=False):
        size, y_off, base_grid = converted[pid]
        grid = stamp_jigsaws(pid, size, y_off, base_grid, out_pools, is_start=is_start)
        doc = build_structure_nbt(size, grid)
        nbt.write_file(os.path.join(struct_dir, out_name + ".nbt"), doc, compress=True)

    # 1. Start crossing (all 4 faces exit into `bridge`)
    emit("nebcr_start", "nebcr", {"bridge": P_BRIDGE}, is_start=True)

    # 2. Bridge depth tiers:
    #    depth 1 (bridge) -> depth 2 (bridge_mid) -> depth 3 (bridge_outer)
    #    -> depth 4 (bridge_tail, common only) -> end (nebef).
    #    Rare bridge pieces (nesr, nemt, nece) only appear in layers 1-3, keeping
    #    their counts close to vanilla caps (3 / 2 / 1) while giving bridges a full
    #    120-190 block span and leaving room & depth budget (size=10) for castle wings.
    # 用户 2026-11-24「规模再大一点」：桥链由 4 跳加到 BRIDGE_TIERS + 1 跳
    tiers = [P_BRIDGE] + ["%s:%s/bridge_%d" % (NS, SUB, i) for i in range(2, BRIDGE_TIERS + 1)]
    for pid in ("nebs", "nebcr", "nerc"):
        for i in range(BRIDGE_TIERS):
            emit("%s_t%d" % (pid, i + 1), pid, {"bridge": tiers[i + 1] if i + 1 < BRIDGE_TIERS else P_BRIDGE_TAIL})
        emit(pid, pid, {"bridge": P_END})

    # Rare bridge pieces
    # nesr climbs +6 blocks and continues onto one elevated bridge_tail piece before ending.
    emit("nesr", "nesr", {"bridge": P_BRIDGE_TAIL})
    emit("nemt", "nemt", {})
    emit("nece", "nece", {"castle": P_CASTLE})

    # 3. Castle depth tiers:
    #    castle -> castle_t2 -> castle_t3 -> castle_t4 -> castle_deep (repeats until max_depth)
    #    Rare castle rooms (neccs, nectb, necsr) appear in the first 4 layers with exact
    #    vanilla weights, approximating their per-fortress caps (3 / 2 / 2).
    for pid in ("nesc", "nescsc", "nescrt", "nesclt"):
        emit(pid + "_t1", pid, {"castle": P_CASTLE_T2})
        emit(pid + "_t2", pid, {"castle": P_CASTLE_T3})
        emit(pid + "_t3", pid, {"castle": P_CASTLE_T4})
        emit(pid, pid, {"castle": P_CASTLE_DEEP})

    # Rare castle pieces
    emit("neccs", "neccs", {"castle": P_CASTLE_DEEP})
    emit("nectb", "nectb", {"castle": P_CASTLE_DEEP})
    emit("necsr", "necsr", {"castle": P_CASTLE_DEEP})

    # 4. End cap (fallback for both bridge and castle pools)
    emit("nebef", "nebef", {})

    # ------------------------------------------------------------------
    # Processor list: polished_blackstone_bricks -> 80% intact / 15% cracked / 5% gilded
    # Rules evaluate sequentially and stop at first match:
    #   Rule 1: 0.15       -> cracked (15.0%)
    #   Rule 2: 0.05/0.85  -> gilded  (0.85 * 0.05882353 = 5.0%)
    #   Else:              -> stays polished_blackstone_bricks (80.0%)
    # ------------------------------------------------------------------
    _write_json(os.path.join(proc_dir, "fortress.json"), {
        "processors": [
            {
                "processor_type": "minecraft:rule",
                "rules": [
                    {
                        "input_predicate": {
                            "predicate_type": "minecraft:random_block_match",
                            "block": "minecraft:polished_blackstone_bricks",
                            "probability": 0.15,
                        },
                        "location_predicate": {"predicate_type": "minecraft:always_true"},
                        "output_state": {"Name": "minecraft:cracked_polished_blackstone_bricks"},
                    },
                    {
                        "input_predicate": {
                            "predicate_type": "minecraft:random_block_match",
                            "block": "minecraft:polished_blackstone_bricks",
                            "probability": 0.05882353,
                        },
                        "location_predicate": {"predicate_type": "minecraft:always_true"},
                        "output_state": {"Name": "minecraft:gilded_blackstone"},
                    },
                ],
            }
        ]
    })

    # ------------------------------------------------------------------
    # Template pools:
    #   start
    #   bridge -> bridge_mid -> bridge_outer -> end  (+ bridge_tail after nesr)
    #   castle -> castle_t2 -> castle_t3 -> castle_t4 -> castle_deep -> end
    #   end
    # ------------------------------------------------------------------
    _write_json(os.path.join(pool_dir, "start.json"), {
        "fallback": "minecraft:empty",
        "elements": [_pool_elem("nebcr_start", 1)],
    })

    for i in range(BRIDGE_TIERS):
        _write_json(os.path.join(pool_dir, "bridge.json" if i == 0 else "bridge_%d.json" % (i + 1)), {
            "fallback": P_END,
            "elements": [
                _pool_elem("nebs_t%d" % (i + 1), 30),
                _pool_elem("nebcr_t%d" % (i + 1), 14),
                _pool_elem("nerc_t%d" % (i + 1), 10),
                _pool_elem("nesr", 5),
                _pool_elem("nemt", 4),
                _pool_elem("nece", 7),
            ],
        })

    _write_json(os.path.join(pool_dir, "bridge_tail.json"), {
        "fallback": P_END,
        "elements": [
            _pool_elem("nebs", 30),
            _pool_elem("nebcr", 10),
            _pool_elem("nerc", 10),
        ],
    })

    _write_json(os.path.join(pool_dir, "castle.json"), {
        "fallback": P_END,
        "elements": [
            _pool_elem("nesc_t1", 25),
            _pool_elem("nescsc_t1", 15),
            _pool_elem("nescrt_t1", 5),
            _pool_elem("nesclt_t1", 10),
            _pool_elem("neccs", 10),
            _pool_elem("nectb", 7),
            _pool_elem("necsr", 5),
        ],
    })

    _write_json(os.path.join(pool_dir, "castle_t2.json"), {
        "fallback": P_END,
        "elements": [
            _pool_elem("nesc_t2", 25),
            _pool_elem("nescsc_t2", 15),
            _pool_elem("nescrt_t2", 5),
            _pool_elem("nesclt_t2", 10),
            _pool_elem("neccs", 10),
            _pool_elem("nectb", 7),
            _pool_elem("necsr", 5),
        ],
    })

    _write_json(os.path.join(pool_dir, "castle_t3.json"), {
        "fallback": P_END,
        "elements": [
            _pool_elem("nesc_t3", 25),
            _pool_elem("nescsc_t3", 15),
            _pool_elem("nescrt_t3", 5),
            _pool_elem("nesclt_t3", 10),
            _pool_elem("neccs", 10),
            _pool_elem("nectb", 7),
            _pool_elem("necsr", 5),
        ],
    })

    _write_json(os.path.join(pool_dir, "castle_t4.json"), {
        "fallback": P_END,
        "elements": [
            _pool_elem("nesc", 25),
            _pool_elem("nescsc", 15),
            _pool_elem("nescrt", 5),
            _pool_elem("nesclt", 10),
            _pool_elem("neccs", 10),
            _pool_elem("nectb", 7),
            _pool_elem("necsr", 5),
        ],
    })

    _write_json(os.path.join(pool_dir, "castle_deep.json"), {
        "fallback": P_END,
        "elements": [
            _pool_elem("nesc", 25),
            _pool_elem("nescsc", 15),
            _pool_elem("nescrt", 5),
            _pool_elem("nesclt", 10),
        ],
    })

    _write_json(os.path.join(pool_dir, "end.json"), {
        "fallback": "minecraft:empty",
        "elements": [_pool_elem("nebef", 1)],
    })

    # ------------------------------------------------------------------
    # Structure & Structure Set
    # ------------------------------------------------------------------
    _write_json(os.path.join(str_def_dir, "fortress.json"), {
        "type": "minecraft:jigsaw",
        "biomes": "%s:paradise_lost" % NS,
        "step": "surface_structures",
        "terrain_adaptation": "none",
        "liquid_settings": "ignore_waterlogging",
        "start_pool": "%s:%s/start" % (NS, SUB),
        "size": JIGSAW_MAX_DEPTH,
        "start_height": {"absolute": START_HEIGHT_OFFSET},
        "project_start_to_heightmap": "WORLD_SURFACE_WG",
        "max_distance_from_center": {"horizontal": JIGSAW_MAX_DIST, "vertical": 256},
        "use_expansion_hack": False,
        "spawn_overrides": {},
    })

    _write_json(os.path.join(ss_dir, "fortress.json"), {
        "placement": {
            "type": "minecraft:random_spread",
            "salt": 1795411,
            "spacing": 26,
            "separation": 14,
        },
        "structures": [
            {"structure": "%s:%s" % (NS, SUB), "weight": 1},
        ],
    })

    # ------------------------------------------------------------------
    # Placeholder chest loot table (empty pools as requested)
    # ------------------------------------------------------------------
    _write_json(os.path.join(loot_dir, "fortress_chest.json"), {
        "type": "minecraft:chest",
        "pools": [],
    })

    nbt_count = len([f for f in os.listdir(struct_dir) if f.endswith(".nbt")])
    pool_count = len([f for f in os.listdir(pool_dir) if f.endswith(".json")])
    print("Generated blackstone fortress into %s: %d structure NBT, %d template pools" % (
        rpg_root, nbt_count, pool_count))


def main():
    rpg_root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "rpg")
    write_all(os.path.abspath(rpg_root))


if __name__ == "__main__":
    main()
