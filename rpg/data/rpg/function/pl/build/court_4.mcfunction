# 伯拉河庭的建筑（positioned 中心 y=82）
place template rpg:paradise/house_large ~14 ~ ~-9 clockwise_90
fill ~9 ~1 ~-1 ~14 ~4 ~1 minecraft:air
fill ~9 ~ ~-1 ~20 ~ ~1 minecraft:polished_andesite
fill ~-5 ~ ~-5 ~5 ~ ~5 minecraft:polished_deepslate
fill ~-4 ~ ~-4 ~4 ~ ~4 minecraft:smooth_stone
setblock ~5 ~ ~5 minecraft:chiseled_stone_bricks
setblock ~5 ~ ~-5 minecraft:chiseled_stone_bricks
setblock ~-5 ~ ~5 minecraft:chiseled_stone_bricks
setblock ~-5 ~ ~-5 minecraft:chiseled_stone_bricks
setblock ~5 ~ ~0 minecraft:chiseled_stone_bricks
setblock ~-5 ~ ~0 minecraft:chiseled_stone_bricks
setblock ~0 ~ ~5 minecraft:chiseled_stone_bricks
setblock ~0 ~ ~-5 minecraft:chiseled_stone_bricks
fill ~-4 ~1 ~-4 ~4 ~1 ~-4 minecraft:stone_brick_stairs[facing=south]
fill ~-4 ~1 ~4 ~4 ~1 ~4 minecraft:stone_brick_stairs[facing=north]
fill ~-4 ~1 ~-3 ~-4 ~1 ~3 minecraft:stone_brick_stairs[facing=east]
fill ~4 ~1 ~-3 ~4 ~1 ~3 minecraft:stone_brick_stairs[facing=west]
fill ~-3 ~1 ~-3 ~3 ~1 ~3 minecraft:stone_bricks
fill ~-2 ~2 ~-2 ~2 ~2 ~-2 minecraft:stone_brick_stairs[facing=south]
fill ~-2 ~2 ~2 ~2 ~2 ~2 minecraft:stone_brick_stairs[facing=north]
fill ~-2 ~2 ~-1 ~-2 ~2 ~1 minecraft:stone_brick_stairs[facing=east]
fill ~2 ~2 ~-1 ~2 ~2 ~1 minecraft:stone_brick_stairs[facing=west]
fill ~-1 ~2 ~-1 ~1 ~2 ~1 minecraft:stone_bricks
fill ~-3 ~1 ~-3 ~3 ~1 ~3 minecraft:polished_andesite replace minecraft:stone_bricks
fill ~-1 ~2 ~-1 ~1 ~2 ~1 minecraft:polished_diorite
setblock ~ ~2 ~ minecraft:chiseled_stone_bricks
setblock ~-4 ~1 ~-4 minecraft:chiseled_stone_bricks
setblock ~-4 ~2 ~-4 minecraft:polished_deepslate
fill ~-4 ~3 ~-4 ~-4 ~5 ~-4 minecraft:deepslate_brick_wall
setblock ~-4 ~6 ~-4 minecraft:chiseled_stone_bricks
setblock ~-4 ~1 ~4 minecraft:chiseled_stone_bricks
setblock ~-4 ~2 ~4 minecraft:polished_deepslate
fill ~-4 ~3 ~4 ~-4 ~5 ~4 minecraft:deepslate_brick_wall
setblock ~-4 ~6 ~4 minecraft:chiseled_stone_bricks
setblock ~4 ~1 ~-4 minecraft:chiseled_stone_bricks
setblock ~4 ~2 ~-4 minecraft:polished_deepslate
fill ~4 ~3 ~-4 ~4 ~5 ~-4 minecraft:deepslate_brick_wall
setblock ~4 ~6 ~-4 minecraft:chiseled_stone_bricks
setblock ~4 ~1 ~4 minecraft:chiseled_stone_bricks
setblock ~4 ~2 ~4 minecraft:polished_deepslate
fill ~4 ~3 ~4 ~4 ~5 ~4 minecraft:deepslate_brick_wall
setblock ~4 ~6 ~4 minecraft:chiseled_stone_bricks
execute if block ~-9 ~4 ~-4 minecraft:air run setblock ~-9 ~4 ~-4 minecraft:light[level=13]
execute if block ~-9 ~4 ~0 minecraft:air run setblock ~-9 ~4 ~0 minecraft:light[level=13]
execute if block ~-9 ~4 ~4 minecraft:air run setblock ~-9 ~4 ~4 minecraft:light[level=13]
execute if block ~0 ~4 ~-4 minecraft:air run setblock ~0 ~4 ~-4 minecraft:light[level=13]
execute if block ~0 ~4 ~0 minecraft:air run setblock ~0 ~4 ~0 minecraft:light[level=13]
execute if block ~0 ~4 ~4 minecraft:air run setblock ~0 ~4 ~4 minecraft:light[level=13]
execute if block ~9 ~4 ~-4 minecraft:air run setblock ~9 ~4 ~-4 minecraft:light[level=13]
execute if block ~9 ~4 ~0 minecraft:air run setblock ~9 ~4 ~0 minecraft:light[level=13]
execute if block ~9 ~4 ~4 minecraft:air run setblock ~9 ~4 ~4 minecraft:light[level=13]
execute unless score #sites rpg_pl matches 1 positioned ~29 ~ ~29 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_big_none
execute unless score #sites rpg_pl matches 1 positioned ~-6 ~ ~39 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/house_small_clockwise_90
execute unless score #sites rpg_pl matches 1 positioned ~-33 ~ ~17 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_medium_180
execute unless score #sites rpg_pl matches 1 positioned ~-37 ~ ~-19 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_small_counterclockwise_90
execute unless score #sites rpg_pl matches 1 positioned ~-6 ~ ~-40 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/house_small_none
execute unless score #sites rpg_pl matches 1 positioned ~27 ~ ~-27 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_big_clockwise_90
