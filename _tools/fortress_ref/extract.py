# -*- coding: utf-8 -*-
"""Extract all 14 vanilla Nether Fortress piece templates (O=0 / South-facing)
from a temporary headless 1.21.11 dedicated server.

Method:
  Uses natural structure generation on two superflat worlds with the EXACT SAME
  seed (so every fortress and child piece generates at the exact same coordinates
  with full `structures.starts["minecraft:fortress"].Children[]` chunk NBT):
    1. Solid-glass flat world (`light_gray_stained_glass`, y=-63..136):
       - Blocks inside a piece's BB that remain glass were NOT touched by the
         piece -> written as `minecraft:structure_void`.
       - Blocks inside BB that became `minecraft:air` were explicitly carved ->
         preserved as `minecraft:air`.
    2. Air-only flat world (1 layer bedrock at y=-64):
       - Cross-checks every non-void block of the exact same piece instance.
       - Reads the exact vanilla pillar column footprints directly below BB
         (`y = minY - 1`) for nebs, nebcr, nece, nebef.

Output:
  _tools/fortress_ref/pieces/<piece_id>.nbt    (14 vanilla piece templates, DataVersion=4671)
  _tools/fortress_ref/pieces/extract_meta.json (sizes, pillars, block stats, verification)

Never touches user saves; temporary worlds live in the OS temp directory.
"""

import argparse
import io
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(HERE)
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import mc_env
import nbt

DATA_VERSION = 4671
FILLER_BLOCK = "minecraft:light_gray_stained_glass"
WORLD_SEED = "1234567"
CELL_SPACING_CHUNKS = 20
CELL_SEPARATION_CHUNKS = 14

REQUIRED_PIECES = [
    "nebs",    # 直桥
    "nebcr",   # 十字桥
    "nerc",    # 十字室
    "nesr",    # 楼梯室
    "nemt",    # 烈焰台
    "nece",    # 城堡入口
    "nesc",    # 小走廊
    "nescsc",  # 小走廊十字
    "nescrt",  # 小走廊右转（有宝箱）
    "nesclt",  # 小走廊左转（有宝箱）
    "neccs",   # 走廊楼梯（下行）
    "nectb",   # 走廊 T 形阳台
    "necsr",   # 地狱疣室
    "nebef",   # 桥的尽头
]

PILLAR_PIECES = ("nebs", "nebcr", "nece", "nebef")
CHEST_PIECES = ("nescrt", "nesclt")

SKIP_LIB = (
    "sponge-mixin", "fabric-loader", "mixinextras", "tiny-mappings",
    "tiny-remapper", "access-widener", "lwjgl", "text2speech", "jinput",
)


def _free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _maven_path(name):
    parts = name.split(":")
    group, artifact, version = parts[0], parts[1], parts[2]
    classifier = parts[3] if len(parts) > 3 else None
    fn = "%s-%s%s.jar" % (artifact, version, "-" + classifier if classifier else "")
    return os.path.join(mc_env.LIBS, group.replace(".", "/"), artifact, version, fn)


def _server_classpath():
    doc = json.load(io.open(mc_env.VJSON, encoding="utf-8"))
    out = []
    for lib in doc["libraries"]:
        name = lib["name"]
        if any(s in name for s in SKIP_LIB):
            continue
        p = _maven_path(name)
        if os.path.isfile(p):
            out.append(p)
    out.append(mc_env.JAR)
    return out


def install_fortress_only_datapack(world_dir):
    """Temporary datapack: make nether_complexes spawn fortress-only at controlled spacing."""
    dp = os.path.join(world_dir, "datapacks", "fort_only")
    ss_dir = os.path.join(dp, "data", "minecraft", "worldgen", "structure_set")
    os.makedirs(ss_dir, exist_ok=True)
    with open(os.path.join(dp, "pack.mcmeta"), "w", encoding="utf-8") as fh:
        json.dump({
            "pack": {
                "pack_format": 94,
                "min_format": [94, 1],
                "max_format": 94,
                "description": "Temp fortress-only structure_set for extraction",
            }
        }, fh)
    with open(os.path.join(ss_dir, "nether_complexes.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "placement": {
                "type": "minecraft:random_spread",
                "salt": 30084232,
                "spacing": CELL_SPACING_CHUNKS,
                "separation": CELL_SEPARATION_CHUNKS,
            },
            "structures": [
                {"structure": "minecraft:fortress", "weight": 1},
            ],
        }, fh)


def run_temp_server(run_dir, gen_settings_dict, commands, wait_boot=180):
    os.makedirs(run_dir, exist_ok=True)
    install_fortress_only_datapack(os.path.join(run_dir, "world"))
    with open(os.path.join(run_dir, "eula.txt"), "w", encoding="utf-8") as fh:
        fh.write("eula=true\n")
    port = _free_port()
    props = [
        "server-ip=127.0.0.1",
        "server-port=%d" % port,
        "online-mode=false",
        "enable-rcon=false",
        "enable-query=false",
        "enable-status=false",
        "enforce-secure-profile=false",
        "pause-when-empty-seconds=0",
        "max-tick-time=-1",
        "view-distance=4",
        "simulation-distance=4",
        "spawn-protection=0",
        "allow-nether=false",
        "level-seed=%s" % WORLD_SEED,
        "level-type=minecraft:flat",
        "generate-structures=true",
        "generator-settings=" + json.dumps(gen_settings_dict, separators=(",", ":")),
        "motd=Fortress Extractor",
    ]
    with open(os.path.join(run_dir, "server.properties"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(props) + "\n")

    cmd = [
        mc_env.JAVA, "-Xmx2G", "-Dfile.encoding=UTF-8",
        "-cp", os.pathsep.join(_server_classpath()),
        "net.minecraft.server.Main", "--nogui",
        "--universe", run_dir, "--world", "world",
    ]
    proc = subprocess.Popen(
        cmd, cwd=run_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        bufsize=1, universal_newlines=True, encoding="utf-8", errors="replace",
    )

    lines = []
    done = False
    deadline = time.time() + wait_boot
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        s = line.rstrip()
        lines.append(s)
        if 'For help, type "help"' in s or "Done (" in s:
            done = True
            break

    if not done:
        proc.kill()
        raise RuntimeError("Server failed to boot:\n" + "\n".join(lines[-40:]))

    tail = []
    marker_event = threading.Event()
    expected_marker = [None]

    def pump():
        for line in proc.stdout:
            s = line.rstrip()
            tail.append(s)
            m = expected_marker[0]
            if m and m in s:
                marker_event.set()

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()

    for idx, c in enumerate(commands):
        if isinstance(c, tuple) and c[0] == "sleep":
            time.sleep(c[1])
            continue
        m = "__DONE_%d__" % idx
        marker_event.clear()
        expected_marker[0] = m
        lines.append(">>> " + c)
        proc.stdin.write(c + "\n")
        proc.stdin.write("say " + m + "\n")
        proc.stdin.flush()
        marker_event.wait(timeout=60.0)
        if idx < 4 or (idx + 1) % 30 == 0 or idx == len(commands) - 1:
            print("    [%d/%d] %s" % (idx + 1, len(commands), c), flush=True)

    proc.stdin.write("stop\n")
    proc.stdin.flush()
    reader.join(timeout=60)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
    lines.extend(tail)
    return lines


def _bb_intersects(a, b):
    return (a[0] <= b[3] and a[3] >= b[0] and
            a[1] <= b[4] and a[4] >= b[1] and
            a[2] <= b[5] and a[5] >= b[2])


def _chunks_full(world, bb):
    minx, _, minz, maxx, _, maxz = bb
    for cx in range(minx >> 4, (maxx >> 4) + 1):
        for cz in range(minz >> 4, (maxz >> 4) + 1):
            ch = world.get_chunk(cx, cz)
            if ch is None:
                return False
            st = ch.get("Status")
            if st is None or st.value != "minecraft:full":
                return False
    return True


def scan_fortress_children(region_dir, world):
    """Scan all .mca files in region_dir and collect every fortress start's Children."""
    pieces_by_id = {pid: [] for pid in REQUIRED_PIECES}
    other_ids = set()
    total_starts = 0
    for fn in sorted(os.listdir(region_dir)):
        if not fn.endswith(".mca"):
            continue
        for cx, cz, chunk in nbt.iter_region_chunks(os.path.join(region_dir, fn)):
            structs = chunk.get("structures")
            if not structs:
                continue
            starts = structs.get("starts")
            if not starts:
                continue
            fort = starts.get("minecraft:fortress")
            if not fort or "Children" not in fort:
                continue
            children = fort["Children"]
            if len(children) == 0:
                continue
            total_starts += 1
            child_list = []
            for ch in children:
                raw_id = ch["id"].value
                pid = raw_id.split(":")[-1].lower()
                bb = list(ch["BB"].value)
                o = ch["O"].value if "O" in ch else -1
                child_list.append((pid, bb, o, ch))
            for idx, (pid, bb, o, ch) in enumerate(child_list):
                if not _chunks_full(world, bb):
                    continue
                overlaps = sum(
                    1 for j, (_, obb, _, _) in enumerate(child_list)
                    if j != idx and _bb_intersects(bb, obb)
                )
                rec = {
                    "id": pid,
                    "bb": bb,
                    "o": o,
                    "overlaps": overlaps,
                    "has_chest_tag": ("Chest" in ch and ch["Chest"].value != 0),
                    "start_chunk": (cx, cz),
                }
                if pid in pieces_by_id:
                    pieces_by_id[pid].append(rec)
                else:
                    other_ids.add(pid)
    return pieces_by_id, total_starts, sorted(other_ids)


def slice_piece(world, bb, filler_block=None):
    minx, miny, minz, maxx, maxy, maxz = bb
    sx, sy, sz = maxx - minx + 1, maxy - miny + 1, maxz - minz + 1
    out = {}
    for ly in range(sy):
        wy = miny + ly
        for lz in range(sz):
            wz = minz + lz
            for lx in range(sx):
                wx = minx + lx
                name, props, be = world.get_block(wx, wy, wz)
                if filler_block and name == filler_block:
                    out[(lx, ly, lz)] = ("minecraft:structure_void", {}, None)
                else:
                    out[(lx, ly, lz)] = (name, props, be)
    return (sx, sy, sz), out


def clean_block_entity(be):
    if be is None:
        return None
    cleaned = nbt.Compound()
    for k, v in be.items():
        if k in ("x", "y", "z", "keepPacked"):
            continue
        cleaned[k] = v
    return cleaned


def build_structure_nbt(size, blocks_dict):
    sx, sy, sz = size
    palette = []
    pal_index = {}

    def get_state_idx(name, props):
        key = (name, tuple(sorted(props.items())))
        if key not in pal_index:
            pal_index[key] = len(palette)
            entry = nbt.Compound()
            entry["Name"] = nbt.String(name)
            if props:
                pcomp = nbt.Compound()
                for pk, pv in sorted(props.items()):
                    pcomp[pk] = nbt.String(str(pv))
                entry["Properties"] = pcomp
            palette.append(entry)
        return pal_index[key]

    blocks_list = nbt.List(nbt.TAG_COMPOUND)
    for ly in range(sy):
        for lz in range(sz):
            for lx in range(sx):
                name, props, be = blocks_dict[(lx, ly, lz)]
                bcomp = nbt.Compound()
                bcomp["pos"] = nbt.List(nbt.TAG_INT, [nbt.Int(lx), nbt.Int(ly), nbt.Int(lz)])
                bcomp["state"] = nbt.Int(get_state_idx(name, props))
                cbe = clean_block_entity(be)
                if cbe is not None:
                    bcomp["nbt"] = cbe
                blocks_list.append(bcomp)

    root = nbt.Compound()
    root["DataVersion"] = nbt.Int(DATA_VERSION)
    root["size"] = nbt.List(nbt.TAG_INT, [nbt.Int(sx), nbt.Int(sy), nbt.Int(sz)])
    root["palette"] = nbt.List(nbt.TAG_COMPOUND, palette)
    root["blocks"] = blocks_list
    root["entities"] = nbt.List(nbt.TAG_COMPOUND)
    return root


def choose_instance(pid, instances, world):
    south = [r for r in instances if r["o"] == 0]
    if not south:
        return None
    if pid in CHEST_PIECES:
        with_chest = []
        for r in south:
            _, blocks = slice_piece(world, r["bb"], filler_block=FILLER_BLOCK)
            if any(name == "minecraft:chest" for name, _, _ in blocks.values()):
                with_chest.append(r)
        if not with_chest:
            return None
        south = with_chest
    if pid == "nebef":
        scored = []
        for r in south:
            _, blocks = slice_piece(world, r["bb"], filler_block=FILLER_BLOCK)
            solid = sum(1 for name, _, _ in blocks.values()
                        if name not in ("minecraft:air", "minecraft:structure_void"))
            scored.append((r["overlaps"], -solid, r))
        scored.sort(key=lambda x: (x[0], x[1]))
        return scored[0][2]
    south.sort(key=lambda r: r["overlaps"])
    return south[0]


def make_forceload_commands(grid_n, sleep_sec=1.2):
    cmds = []
    step = CELL_SPACING_CHUNKS * 16  # 320 blocks per cell
    for gx in range(grid_n):
        for gz in range(grid_n):
            cx = gx * step + 48
            cz = gz * step + 48
            # 15x15 chunks = 225 chunks (<= 256 max)
            cmds.append("forceload add %d %d %d %d" % (cx - 112, cz - 112, cx + 112, cz + 112))
            cmds.append(("sleep", sleep_sec))
            cmds.append("forceload remove all")
    cmds.append("save-all flush")
    return cmds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--grid", type=int, default=6, help="NxN grid of fortress cells to generate")
    args = parser.parse_args()

    out_dir = os.path.join(HERE, "pieces")
    os.makedirs(out_dir, exist_ok=True)
    tmp_root = tempfile.mkdtemp(prefix="fortress_extract_")
    print("Temp dir:", tmp_root, flush=True)

    try:
        cmds = make_forceload_commands(args.grid, sleep_sec=1.2)

        # Pass 1: Solid glass flat world
        glass_dir = os.path.join(tmp_root, "glass_srv")
        glass_gen = {
            "biome": "minecraft:nether_wastes",
            "layers": [
                {"block": "minecraft:bedrock", "height": 1},
                {"block": FILLER_BLOCK, "height": 200},
            ],
            "structure_overrides": ["minecraft:nether_complexes"],
        }
        print("Pass 1: generating %dx%d cells in solid-glass flat world..." % (args.grid, args.grid), flush=True)
        run_temp_server(glass_dir, glass_gen, cmds)

        glass_region = os.path.join(glass_dir, "world", "region")
        glass_world = nbt.WorldReader(glass_region)
        glass_pieces, glass_starts, other_ids = scan_fortress_children(glass_region, glass_world)
        print("  Glass world fortress starts: %d  other_ids: %s" % (glass_starts, other_ids), flush=True)

        # Pass 2: Air-only flat world with EXACT SAME SEED
        air_dir = os.path.join(tmp_root, "air_srv")
        air_gen = {
            "biome": "minecraft:nether_wastes",
            "layers": [{"block": "minecraft:bedrock", "height": 1}],
            "structure_overrides": ["minecraft:nether_complexes"],
        }
        print("Pass 2: generating %dx%d cells in air-only flat world (same seed)..." % (args.grid, args.grid), flush=True)
        run_temp_server(air_dir, air_gen, cmds)

        air_region = os.path.join(air_dir, "world", "region")
        air_world = nbt.WorldReader(air_region)

        meta = {
            "data_version": DATA_VERSION,
            "seed": WORLD_SEED,
            "glass_starts": glass_starts,
            "other_ids": other_ids,
            "pieces": {},
        }

        missing = []
        for pid in REQUIRED_PIECES:
            g_insts = glass_pieces[pid]
            south_count = sum(1 for r in g_insts if r["o"] == 0)
            chosen = choose_instance(pid, g_insts, glass_world)
            if chosen is None:
                missing.append(pid)
                print("  [MISSING] %s (total=%d, O=0=%d)" % (pid, len(g_insts), south_count), flush=True)
                continue

            size, g_blocks = slice_piece(glass_world, chosen["bb"], filler_block=FILLER_BLOCK)

            # Cross-check EXACT same BB in air world:
            # - Verify zero block-name discrepancies between glass and air worlds.
            # - Take block states (especially fence connections!) from air_world so
            #   boundary fences never connect spuriously to the glass filler.
            air_name_diffs = 0
            air_prop_diffs = 0
            pillar_cols = []
            blocks = dict(g_blocks)
            if _chunks_full(air_world, chosen["bb"]):
                _, a_blocks = slice_piece(air_world, chosen["bb"], filler_block=None)
                for pos, (gname, gprops, gbe) in g_blocks.items():
                    aname, aprops, abe = a_blocks[pos]
                    if gname == "minecraft:structure_void":
                        if aname != "minecraft:air":
                            air_name_diffs += 1
                    else:
                        if gname != aname:
                            air_name_diffs += 1
                        else:
                            if gprops != aprops:
                                air_prop_diffs += 1
                            blocks[pos] = (aname, aprops, abe if abe is not None else gbe)
                if pid in PILLAR_PIECES:
                    minx, miny, minz, maxx, maxy, maxz = chosen["bb"]
                    sx, _, sz = size
                    for lx in range(sx):
                        for lz in range(sz):
                            bname, _, _ = air_world.get_block(minx + lx, miny - 1, minz + lz)
                            if bname != "minecraft:air":
                                pillar_cols.append([lx, lz, bname])

            doc = build_structure_nbt(size, blocks)
            nbt_path = os.path.join(out_dir, pid + ".nbt")
            nbt.write_file(nbt_path, doc, compress=True)

            # Block histogram + block entities
            hist = {}
            bes = []
            for pos, (bname, bprops, be) in blocks.items():
                hist[bname] = hist.get(bname, 0) + 1
                if be is not None:
                    bes.append({"pos": list(pos), "block": bname, "nbt": nbt.unwrap(clean_block_entity(be))})

            meta["pieces"][pid] = {
                "size": list(size),
                "bb": chosen["bb"],
                "overlaps": chosen["overlaps"],
                "total_instances": len(g_insts),
                "south_instances": south_count,
                "air_vs_glass_name_diffs": air_name_diffs,
                "air_vs_glass_prop_diffs": air_prop_diffs,
                "pillar_columns_below_bb": pillar_cols,
                "block_counts": dict(sorted(hist.items())),
                "block_entities": bes,
            }
            print("  [OK] %-7s size=%-10s total=%-3d O=0=%-3d ov=%d name_diff=%d prop_diff=%d pillars=%d" % (
                pid, "x".join(str(x) for x in size), len(g_insts), south_count,
                chosen["overlaps"], air_name_diffs, air_prop_diffs, len(pillar_cols),
            ), flush=True)

        meta_path = os.path.join(out_dir, "extract_meta.json")
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

        if missing:
            raise SystemExit("Missing O=0 pieces: %s (try larger --grid)" % missing)
        print("All 14 pieces extracted successfully to", out_dir, flush=True)
    finally:
        if not args.keep_temp:
            shutil.rmtree(tmp_root, ignore_errors=True)
        else:
            print("Kept temp dir:", tmp_root, flush=True)


if __name__ == "__main__":
    main()
