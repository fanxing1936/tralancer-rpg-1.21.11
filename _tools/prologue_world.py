# -*- coding: utf-8 -*-
"""序章维度 rpg:armageddon 与它唯一的生物群系「哈米吉多顿」（方案书 · 维度与生物群系）。

用户 2026-11-22：焦土（方块混铺）、枯色植被（枯草，最多一些倒下的没有叶子的树）、遍地骸骨与血迹、
血色水洼、赤橙色的天空（神圣武器那一系，天堂的颜色）。

1.21.11 的写法（对照客户端 jar 里的原版文件）：天空、雾、云、天光、环境粒子写在群系的 `attributes`
（minecraft:visual/*）；水色、草色、叶色、枯叶色仍在 `effects`。维度类型用固定时间、不挂昼夜时间线，
天色停在一刻。地形是噪声生成器 + 自己的地形设定：y=80 上下几格起伏的盆地，没有洞穴、矿物、含水层。
中央战场另用结构放下去（prologue_arena.py），这里只管周围到天边的地面。
"""
import json
import os

NS = "rpg"
ID = "armageddon"
SURFACE_Y = 80

GROUND = ["minecraft:muddy_mangrove_roots", "minecraft:coarse_dirt", "minecraft:rooted_dirt", "minecraft:gravel", "minecraft:soul_soil",
          "minecraft:mud", "minecraft:packed_mud", "minecraft:blackstone", "minecraft:basalt", "minecraft:dirt",
          "minecraft:magma_block", "minecraft:stone"]


def _w(root, rel, obj):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def block(name, **props):
    d = {"Name": name}
    if props:
        d["Properties"] = {k: str(v) for k, v in props.items()}
    return d


def dimension_type():
    return {
        "ambient_light": 0.12,
        "attributes": {
            "minecraft:gameplay/bed_rule": {"can_set_spawn": "never", "can_sleep": "never", "explodes": False},
            "minecraft:gameplay/respawn_anchor_works": False,
            "minecraft:gameplay/can_start_raid": False,
            "minecraft:visual/sky_color": "#c85024",
            "minecraft:visual/fog_color": "#d87034",
            "minecraft:visual/sky_light_color": "#ffb47a",
        },
        "coordinate_scale": 1.0,
        "has_ceiling": False,
        # 固定时刻：天色不随昼夜变。注意下雨、雷暴会把所有维度的天空一起压暗（实测），
        # 所以序章开始时把天气设为晴天（prologue 的 start 里）
        "has_fixed_time": True,
        "has_skylight": True,
        "height": 256,
        "infiniburn": "#minecraft:infiniburn_overworld",
        "logical_height": 256,
        "min_y": 0,
        "monster_spawn_block_light_limit": 0,
        "monster_spawn_light_level": 0,
        "skybox": "overworld",
        "timelines": "#%s:in_%s" % (NS, ID),   # 空标签：没有昼夜轨道
    }


def biome():
    feats = [[] for _ in range(11)]
    p = "%s:%s/" % (NS, ID)
    feats[1] = [p + "blood_puddle"]
    feats[6] = [p + "wart_disk", p + "soul_scorch"]
    # 骸骨主要靠原版的化石结构（用户 2026-11-22「骨头多调用遗骸那个结构」）：
    # 露在地面的下界化石是本维度自己的结构（write 里的 structure / structure_set），大的脊骨、头骨化石半埋在地表
    feats[3] = [p + "fossil"]
    feats[9] = [p + "fallen_tree", p + "stump", p + "dry_grass", p + "dead_bush",
                p + "skulls", p + "blood_splatter"]
    return {
        "has_precipitation": False,
        "temperature": 2.0,
        "downfall": 0.0,
        "attributes": {
            "minecraft:visual/sky_color": "#c85024",
            "minecraft:visual/fog_color": "#d87034",
            "minecraft:visual/water_fog_color": "#3d0505",
            "minecraft:visual/cloud_color": "#b3ffc46b",
            "minecraft:visual/sky_light_color": "#ffb47a",
            "minecraft:visual/ambient_particles": [
                {"particle": {"type": "minecraft:white_ash"}, "probability": 0.02},
                {"particle": {"type": "minecraft:ash"}, "probability": 0.004}],
            "minecraft:audio/ambient_sounds": {
                "loop": "minecraft:ambient.basalt_deltas.loop",
                "additions": {"sound": "minecraft:ambient.basalt_deltas.additions", "tick_chance": 0.0111},
                "mood": {"block_search_extent": 8, "offset": 2.0, "sound": "minecraft:ambient.basalt_deltas.mood",
                         "tick_delay": 6000}},
        },
        "effects": {"water_color": "#7a0e0e", "grass_color": "#8a7a52", "foliage_color": "#7a6a48",
                    "dry_foliage_color": "#7a6448"},
        "spawners": {k: [] for k in ("monster", "creature", "ambient", "axolotls", "underground_water_creature",
                                     "water_creature", "water_ambient", "misc")},
        "spawn_costs": {},
        "carvers": [],
        "features": feats,
    }


def noise_settings():
    zero = 0.0
    final = {"type": "minecraft:interpolated", "argument": {
        "type": "minecraft:add",
        # y=48 处 +1、y=112 处 -1：密度在 y≈80 穿过 0，就是地面
        "argument1": {"type": "minecraft:y_clamped_gradient", "from_y": SURFACE_Y - 32, "to_y": SURFACE_Y + 32,
                      "from_value": 1.0, "to_value": -1.0},
        "argument2": {"type": "minecraft:add",
                      "argument1": {"type": "minecraft:mul", "argument1": 0.18,
                                    "argument2": {"type": "minecraft:noise", "noise": "minecraft:surface",
                                                  "xz_scale": 0.6, "y_scale": 0.0}},
                      "argument2": {"type": "minecraft:add",
                                    "argument1": {"type": "minecraft:mul", "argument1": 0.06,
                                                  "argument2": {"type": "minecraft:noise",
                                                                "noise": "minecraft:surface_secondary",
                                                                "xz_scale": 2.0, "y_scale": 0.0}},
                                    # 细碎起伏：把整齐的台阶打散
                                    "argument2": {"type": "minecraft:mul", "argument1": 0.04,
                                                  "argument2": {"type": "minecraft:noise", "noise": "minecraft:gravel",
                                                                "xz_scale": 6.0, "y_scale": 0.0}}}}}}

    def th(noise, lo, hi, result):
        return {"type": "minecraft:condition",
                "if_true": {"type": "minecraft:noise_threshold", "noise": noise, "min_threshold": lo, "max_threshold": hi},
                "then_run": {"type": "minecraft:block", "result_state": result}}

    top = {"type": "minecraft:sequence", "sequence": [
        th("minecraft:netherrack", 0.62, 9.0, block("minecraft:magma_block")),       # 极少的余烬
        # 用户 2026-11-22：泥巴（mud）与沾泥的红树根（muddy_mangrove_roots）为主要地基，其余只做点缀
        th("minecraft:surface", 0.5, 9.0, block("minecraft:soul_soil")),            # 烧黑的地方
        th("minecraft:soul_sand_layer", 0.6, 9.0, block("minecraft:blackstone")),
        th("minecraft:gravel", 0.5, 9.0, block("minecraft:gravel")),
        th("minecraft:patch", 0.35, 9.0, block("minecraft:coarse_dirt")),
        th("minecraft:gravel", -9.0, -0.6, block("minecraft:packed_mud")),
        th("minecraft:surface", -9.0, -0.55, block("minecraft:rooted_dirt")),
        th("minecraft:surface_secondary", 0.0, 9.0, block("minecraft:muddy_mangrove_roots", axis="y")),
        {"type": "minecraft:block", "result_state": block("minecraft:mud")},
    ]}
    under = {"type": "minecraft:sequence", "sequence": [
        th("minecraft:surface", 0.42, 9.0, block("minecraft:soul_soil")),
        {"type": "minecraft:block", "result_state": block("minecraft:mud")},
    ]}
    surface_rule = {"type": "minecraft:sequence", "sequence": [
        {"type": "minecraft:condition",
         "if_true": {"type": "minecraft:vertical_gradient", "random_name": "minecraft:bedrock_floor",
                     "true_at_and_below": {"above_bottom": 0}, "false_at_and_above": {"above_bottom": 5}},
         "then_run": {"type": "minecraft:block", "result_state": block("minecraft:bedrock")}},
        {"type": "minecraft:condition",
         "if_true": {"type": "minecraft:stone_depth", "offset": 0, "add_surface_depth": False,
                     "secondary_depth_range": 0, "surface_type": "floor"},
         "then_run": top},
        {"type": "minecraft:condition",
         "if_true": {"type": "minecraft:stone_depth", "offset": 0, "add_surface_depth": True,
                     "secondary_depth_range": 0, "surface_type": "floor"},
         "then_run": under},
    ]}
    router = {k: zero for k in ("barrier", "continents", "depth", "erosion", "fluid_level_floodedness",
                                "fluid_level_spread", "lava", "ridges", "temperature", "vegetation",
                                "vein_gap", "vein_ridged", "vein_toggle")}
    router["final_density"] = final
    router["preliminary_surface_level"] = float(SURFACE_Y)
    return {
        "sea_level": -64, "disable_mob_generation": True, "aquifers_enabled": False, "ore_veins_enabled": False,
        "legacy_random_source": False,
        "default_block": block("minecraft:stone"), "default_fluid": block("minecraft:water", level=0),
        "noise": {"min_y": 0, "height": 256, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": router, "spawn_target": [], "surface_rule": surface_rule,
    }


def _air_on_solid():
    return {"type": "minecraft:all_of", "predicates": [
        {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
        {"type": "minecraft:solid", "offset": [0, -1, 0]}]}


def _patch(tries, spread, provider, predicate=None):
    return {"type": "minecraft:random_patch", "config": {
        "tries": tries, "xz_spread": spread, "y_spread": 1,
        "feature": {"feature": {"type": "minecraft:simple_block", "config": {"to_place": provider}},
                    "placement": [{"type": "minecraft:block_predicate_filter",
                                   "predicate": predicate or _air_on_solid()}]}}}


def _weighted(entries):
    return {"type": "minecraft:weighted_state_provider",
            "entries": [{"data": d, "weight": w} for d, w in entries]}


def configured():
    dirt_like = ["minecraft:muddy_mangrove_roots", "minecraft:coarse_dirt", "minecraft:rooted_dirt", "minecraft:gravel", "minecraft:mud",
                 "minecraft:packed_mud", "minecraft:dirt"]
    wire = []
    for n, e, s, w, wt in (("none", "none", "none", "none", 3), ("side", "none", "side", "none", 2),
                           ("none", "side", "none", "side", 2), ("side", "side", "none", "none", 1),
                           ("none", "none", "side", "side", 1), ("side", "side", "side", "side", 1)):
        wire.append((block("minecraft:redstone_wire", north=n, east=e, south=s, west=w, power=0), wt))
    return {
        "blood_puddle": {"type": "minecraft:waterlogged_vegetation_patch", "config": {
            "depth": 1, "extra_bottom_block_chance": 0.0, "extra_edge_column_chance": 0.25,
            "ground_state": {"type": "minecraft:simple_state_provider", "state": block("minecraft:mud")},
            "replaceable": "#%s:%s_ground" % (NS, ID), "surface": "floor", "vegetation_chance": 0.0,
            "vegetation_feature": {"feature": "minecraft:patch_dry_grass", "placement": []},
            "vertical_range": 4, "xz_radius": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 2}}},
        "wart_disk": {"type": "minecraft:disk", "config": {
            "half_height": 0, "radius": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 2},
            "state_provider": {"fallback": {"type": "minecraft:simple_state_provider",
                                            "state": block("minecraft:nether_wart_block")}, "rules": []},
            "target": {"type": "minecraft:matching_blocks", "blocks": dirt_like}}},
        "soul_scorch": {"type": "minecraft:disk", "config": {
            "half_height": 0, "radius": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 4},
            "state_provider": {"fallback": {"type": "minecraft:simple_state_provider",
                                            "state": block("minecraft:soul_soil")}, "rules": []},
            "target": {"type": "minecraft:matching_blocks", "blocks": dirt_like}}},
        # 倒下的树：原版 fallen_tree，树干换成烧黑的深色橡木，不要蘑菇、不要藤蔓，没有叶子
        "fallen_tree": {"type": "minecraft:fallen_tree", "config": {
            "log_decorators": [], "stump_decorators": [],
            "log_length": {"type": "minecraft:uniform", "min_inclusive": 3, "max_inclusive": 6},
            "trunk_provider": {"type": "minecraft:simple_state_provider",
                               "state": block("minecraft:dark_oak_log", axis="y")}}},
        "stump": {"type": "minecraft:block_column", "config": {
            "direction": "up", "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            "prioritize_tip": False,
            "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 2},
                        "provider": {"type": "minecraft:simple_state_provider",
                                     "state": block("minecraft:dark_oak_log", axis="y")}}]}},
        "fossil": {"type": "minecraft:fossil", "config": {
            "fossil_processors": "minecraft:fossil_rot", "overlay_processors": "minecraft:fossil_rot",
            "fossil_structures": ["minecraft:fossil/spine_%d" % i for i in range(1, 5)]
                                 + ["minecraft:fossil/skull_%d" % i for i in range(1, 5)],
            "overlay_structures": ["minecraft:fossil/spine_%d" % i for i in range(1, 5)]
                                  + ["minecraft:fossil/skull_%d" % i for i in range(1, 5)],
            "max_empty_corners_allowed": 7}},
        "skulls": _patch(3, 3, _weighted([(block("minecraft:skeleton_skull", rotation=r), 1)
                                          for r in (0, 2, 5, 7, 10, 13)])),
        "blood_splatter": _patch(24, 4, _weighted(wire), {"type": "minecraft:all_of", "predicates": [
            {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            {"type": "minecraft:would_survive", "state": block("minecraft:redstone_wire")}]}),
    }


def placed():
    def surf(feature, extra, hm="WORLD_SURFACE_WG"):
        return {"feature": "%s:%s/%s" % (NS, ID, feature) if ":" not in feature else feature,
                "placement": extra + [{"type": "minecraft:in_square"},
                                      {"type": "minecraft:heightmap", "heightmap": hm},
                                      {"type": "minecraft:biome"}]}

    down = {"type": "minecraft:random_offset", "xz_spread": 0, "y_spread": -1}
    sapling = {"type": "minecraft:block_predicate_filter",
               "predicate": {"type": "minecraft:would_survive", "state": block("minecraft:oak_sapling", stage=0)}}
    d = {
        "blood_puddle": surf("blood_puddle", [{"type": "minecraft:rarity_filter", "chance": 3}]),
        "wart_disk": surf("wart_disk", [{"type": "minecraft:rarity_filter", "chance": 3}]),
        "soul_scorch": surf("soul_scorch", [{"type": "minecraft:rarity_filter", "chance": 4}]),
        "fallen_tree": surf("fallen_tree", [{"type": "minecraft:rarity_filter", "chance": 5}], "MOTION_BLOCKING"),
        "stump": surf("stump", [{"type": "minecraft:rarity_filter", "chance": 7}], "MOTION_BLOCKING"),
        "dry_grass": surf("minecraft:patch_dry_grass", [{"type": "minecraft:count", "count": 2}], "MOTION_BLOCKING"),
        "dead_bush": surf("minecraft:patch_dead_bush", [{"type": "minecraft:rarity_filter", "chance": 2}],
                          "MOTION_BLOCKING"),
        "fossil": surf("fossil", [{"type": "minecraft:rarity_filter", "chance": 5}]),
        "skulls": surf("skulls", [{"type": "minecraft:rarity_filter", "chance": 4}], "MOTION_BLOCKING"),
        "blood_splatter": surf("blood_splatter", [{"type": "minecraft:count", "count": 2}], "MOTION_BLOCKING"),
    }
    # 圆盘要落在地表方块那一层，而不是地表上方的空气
    for k in ("wart_disk", "soul_scorch"):
        d[k]["placement"].insert(-1, down)
    # 大化石半埋：从地表往下沉 2～4 格
    d["fossil"]["placement"].insert(-1, {"type": "minecraft:random_offset", "xz_spread": 0,
                                         "y_spread": {"type": "minecraft:uniform", "min_inclusive": -4, "max_inclusive": -2}})
    d["fallen_tree"]["placement"].insert(-1, sapling)
    d["stump"]["placement"].insert(-1, sapling)
    return d


def write(rpg):
    data = os.path.join(rpg, "data")
    _w(data, "%s/dimension_type/%s.json" % (NS, ID), dimension_type())
    _w(data, "%s/dimension/%s.json" % (NS, ID), {
        "type": "%s:%s" % (NS, ID),
        "generator": {"type": "minecraft:noise", "settings": "%s:%s" % (NS, ID),
                      "biome_source": {"type": "minecraft:fixed", "biome": "%s:%s" % (NS, ID)}}})
    _w(data, "%s/worldgen/biome/%s.json" % (NS, ID), biome())
    _w(data, "%s/worldgen/noise_settings/%s.json" % (NS, ID), noise_settings())
    _w(data, "%s/tags/timeline/in_%s.json" % (NS, ID), {"values": []})
    _w(data, "%s/tags/block/%s_ground.json" % (NS, ID), {"values": GROUND})
    # 露在地面的骸骨：原版下界化石，换成本维度自己的结构与分布（原版每 2 个区块一具，太密）
    _w(data, "%s/worldgen/structure/%s/remains.json" % (NS, ID), {
        "type": "minecraft:nether_fossil", "biomes": "%s:%s" % (NS, ID),
        "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": SURFACE_Y + 16},
                   "max_inclusive": {"absolute": SURFACE_Y + 30}},
        "spawn_overrides": {}, "step": "surface_structures", "terrain_adaptation": "beard_thin"})
    _w(data, "%s/worldgen/structure_set/%s/remains.json" % (NS, ID), {
        "placement": {"type": "minecraft:random_spread", "salt": 1795322, "separation": 1, "spacing": 3},
        "structures": [{"structure": "%s:%s/remains" % (NS, ID), "weight": 1}]})
    for k, v in configured().items():
        _w(data, "%s/worldgen/configured_feature/%s/%s.json" % (NS, ID, k), v)
    for k, v in placed().items():
        _w(data, "%s/worldgen/placed_feature/%s/%s.json" % (NS, ID, k), v)
    return 8 + len(configured()) + len(placed())
