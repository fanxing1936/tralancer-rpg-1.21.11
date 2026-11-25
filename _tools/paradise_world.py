# -*- coding: utf-8 -*-
"""维度 rpg:paradise_lost 与它的群系「失乐园」（用户 2026-11-24：参考序章的群系，泥巴更多、水池和天空都是血色、怪物不燃烧）。

底子沿用 prologue_world（同样的地物、骸骨、枯树）；不同的是：
  * 地形起伏更大，海平面放到 78，低处积成大片水（群系水色是血色）；
  * 地表几乎全是泥与沾泥的红树根，碎石、黑石只做点缀；
  * 天、雾、云、天光全是血色；怪物照常刷，且不会在天光下燃烧（minecraft:gameplay/monsters_burn）。
"""
import copy
import os

import prologue_world as PW

ID = "paradise_lost"
NS = PW.NS
SKY, FOG, LIGHT = "#5a0606", "#6e0c0c", "#ff5a4a"
SEA = 78

SPAWN = [("zombie", 40, 2, 4), ("husk", 30, 1, 3), ("zombie_villager", 8, 1, 1), ("skeleton", 30, 1, 3), ("stray", 12, 1, 2),
         ("bogged", 18, 1, 2), ("spider", 25, 1, 3), ("cave_spider", 10, 1, 3), ("creeper", 16, 1, 2), ("witch", 8, 1, 1),
         ("pillager", 1, 1, 1), ("vindicator", 6, 1, 1), ("zombified_piglin", 10, 1, 3), ("wither_skeleton", 10, 1, 2),
         ("blaze", 5, 1, 1), ("enderman", 5, 1, 1)]


def write(rpg):
    old = PW.ID
    PW.ID = ID
    try:
        dim, bio, noise = PW.dimension_type(), PW.biome(), PW.noise_settings()
        feats, placed = PW.configured(), PW.placed()
    finally:
        PW.ID = old
    # 维度
    at = dim["attributes"]
    at.update({"minecraft:visual/sky_color": SKY, "minecraft:visual/fog_color": FOG, "minecraft:visual/sky_light_color": LIGHT,
               "minecraft:gameplay/monsters_burn": False,
               # 玩法天光：满 15 时原版拒绝所有看光的怪自然生成，只剩不看光的掠夺者；画面亮度由别的属性管
               "minecraft:gameplay/sky_light_level": 7.0})
    dim["ambient_light"] = 0.16
    dim["monster_spawn_light_level"] = 15
    dim["monster_spawn_block_light_limit"] = 15
    dim["timelines"] = "#%s:in_%s" % (NS, ID)
    # 群系
    ba = bio["attributes"]
    ba.update({"minecraft:visual/sky_color": SKY, "minecraft:visual/fog_color": FOG, "minecraft:visual/sky_light_color": LIGHT,
               "minecraft:visual/cloud_color": "#b37a1010", "minecraft:visual/water_fog_color": "#2a0202",
               "minecraft:visual/ambient_particles": [
                   {"particle": {"type": "minecraft:crimson_spore"}, "probability": 0.012},
                   {"particle": {"type": "minecraft:ash"}, "probability": 0.004}],
               "minecraft:audio/ambient_sounds": {
                   "loop": "minecraft:ambient.crimson_forest.loop",
                   "additions": {"sound": "minecraft:ambient.crimson_forest.additions", "tick_chance": 0.0111},
                   "mood": {"block_search_extent": 8, "offset": 2.0, "sound": "minecraft:ambient.crimson_forest.mood", "tick_delay": 6000}}})
    bio["effects"].update({"water_color": "#6a0606", "grass_color": "#6e5a3a", "foliage_color": "#6a4a34", "dry_foliage_color": "#6a4434"})
    bio["spawners"]["monster"] = [{"type": "minecraft:" + m, "weight": w, "minCount": a, "maxCount": b} for m, w, a, b in SPAWN]
    # 地形：起伏更大、低处积水
    noise["sea_level"] = SEA
    noise["disable_mob_generation"] = False
    add2 = noise["noise_router"]["final_density"]["argument"]["argument2"]
    add2["argument1"]["argument1"] = 0.30
    add2["argument2"]["argument1"]["argument1"] = 0.09
    noise["surface_rule"] = surface()
    PW_W = PW._w
    data = os.path.join(rpg, "data")
    PW_W(data, "%s/dimension_type/%s.json" % (NS, ID), dim)
    PW_W(data, "%s/dimension/%s.json" % (NS, ID), {
        "type": "%s:%s" % (NS, ID),
        "generator": {"type": "minecraft:noise", "settings": "%s:%s" % (NS, ID),
                      "biome_source": {"type": "minecraft:fixed", "biome": "%s:%s" % (NS, ID)}}})
    PW_W(data, "%s/worldgen/biome/%s.json" % (NS, ID), bio)
    PW_W(data, "%s/worldgen/noise_settings/%s.json" % (NS, ID), noise)
    PW_W(data, "%s/tags/timeline/in_%s.json" % (NS, ID), {"values": []})
    PW_W(data, "%s/tags/block/%s_ground.json" % (NS, ID), {"values": PW.GROUND})
    PW_W(data, "%s/worldgen/structure/%s/remains.json" % (NS, ID), {
        "type": "minecraft:nether_fossil", "biomes": "%s:%s" % (NS, ID),
        "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": PW.SURFACE_Y + 16},
                   "max_inclusive": {"absolute": PW.SURFACE_Y + 30}},
        "spawn_overrides": {}, "step": "surface_structures", "terrain_adaptation": "beard_thin"})
    PW_W(data, "%s/worldgen/structure_set/%s/remains.json" % (NS, ID), {
        "placement": {"type": "minecraft:random_spread", "salt": 1795390, "separation": 2, "spacing": 5},
        "structures": [{"structure": "%s:%s/remains" % (NS, ID), "weight": 1}]})
    # 地物：血洼更多，灵魂土焦痕少一些
    placed = copy.deepcopy(placed)
    placed["blood_puddle"]["placement"][0] = {"type": "minecraft:count", "count": 2}
    placed["soul_scorch"]["placement"][0] = {"type": "minecraft:rarity_filter", "chance": 10}
    for k, v in feats.items():
        PW_W(data, "%s/worldgen/configured_feature/%s/%s.json" % (NS, ID, k), v)
    for k, v in placed.items():
        PW_W(data, "%s/worldgen/placed_feature/%s/%s.json" % (NS, ID, k), v)
    return 8 + len(feats) + len(placed)


def surface():
    b = PW.block

    def th(noise, lo, hi, result):
        return {"type": "minecraft:condition",
                "if_true": {"type": "minecraft:noise_threshold", "noise": noise, "min_threshold": lo, "max_threshold": hi},
                "then_run": {"type": "minecraft:block", "result_state": result}}

    top = {"type": "minecraft:sequence", "sequence": [
        th("minecraft:netherrack", 0.75, 9.0, b("minecraft:nether_wart_block")),
        th("minecraft:soul_sand_layer", 0.75, 9.0, b("minecraft:blackstone")),
        th("minecraft:gravel", 0.72, 9.0, b("minecraft:coarse_dirt")),
        th("minecraft:gravel", -9.0, -0.72, b("minecraft:packed_mud")),
        th("minecraft:surface_secondary", 0.35, 9.0, b("minecraft:muddy_mangrove_roots", axis="y")),
        {"type": "minecraft:block", "result_state": b("minecraft:mud")},
    ]}
    under = {"type": "minecraft:block", "result_state": b("minecraft:mud")}
    return {"type": "minecraft:sequence", "sequence": [
        {"type": "minecraft:condition",
         "if_true": {"type": "minecraft:vertical_gradient", "random_name": "minecraft:bedrock_floor",
                     "true_at_and_below": {"above_bottom": 0}, "false_at_and_above": {"above_bottom": 5}},
         "then_run": {"type": "minecraft:block", "result_state": b("minecraft:bedrock")}},
        {"type": "minecraft:condition",
         "if_true": {"type": "minecraft:stone_depth", "offset": 0, "add_surface_depth": False,
                     "secondary_depth_range": 0, "surface_type": "floor"}, "then_run": top},
        {"type": "minecraft:condition",
         "if_true": {"type": "minecraft:stone_depth", "offset": 0, "add_surface_depth": True,
                     "secondary_depth_range": 6, "surface_type": "floor"}, "then_run": under},
    ]}
