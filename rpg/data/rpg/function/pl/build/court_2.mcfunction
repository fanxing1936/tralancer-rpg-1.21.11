# 基训河庭的建筑（positioned 中心 y=82）
place template rpg:paradise/tower_large ~-7 ~ ~-7 none
fill ~-7 ~1 ~-1 ~-2 ~4 ~1 minecraft:air
fill ~-20 ~ ~-1 ~-2 ~ ~1 minecraft:polished_andesite
fill ~-3 ~ ~-3 ~3 ~ ~3 minecraft:polished_deepslate
fill ~-2 ~ ~-2 ~2 ~ ~2 minecraft:smooth_stone
setblock ~3 ~ ~3 minecraft:chiseled_stone_bricks
setblock ~3 ~ ~-3 minecraft:chiseled_stone_bricks
setblock ~-3 ~ ~3 minecraft:chiseled_stone_bricks
setblock ~-3 ~ ~-3 minecraft:chiseled_stone_bricks
setblock ~3 ~ ~0 minecraft:chiseled_stone_bricks
setblock ~-3 ~ ~0 minecraft:chiseled_stone_bricks
setblock ~0 ~ ~3 minecraft:chiseled_stone_bricks
setblock ~0 ~ ~-3 minecraft:chiseled_stone_bricks
fill ~-2 ~1 ~-2 ~2 ~1 ~-2 minecraft:stone_brick_stairs[facing=south]
fill ~-2 ~1 ~2 ~2 ~1 ~2 minecraft:stone_brick_stairs[facing=north]
fill ~-2 ~1 ~-1 ~-2 ~1 ~1 minecraft:stone_brick_stairs[facing=east]
fill ~2 ~1 ~-1 ~2 ~1 ~1 minecraft:stone_brick_stairs[facing=west]
fill ~-1 ~1 ~-1 ~1 ~1 ~1 minecraft:stone_bricks
fill ~-1 ~1 ~-1 ~1 ~1 ~1 minecraft:polished_diorite
setblock ~ ~1 ~ minecraft:chiseled_stone_bricks
setblock ~-2 ~1 ~-2 minecraft:chiseled_stone_bricks
fill ~-2 ~2 ~-2 ~-2 ~3 ~-2 minecraft:deepslate_brick_wall
setblock ~-2 ~4 ~-2 minecraft:chiseled_stone_bricks
setblock ~-2 ~1 ~2 minecraft:chiseled_stone_bricks
fill ~-2 ~2 ~2 ~-2 ~3 ~2 minecraft:deepslate_brick_wall
setblock ~-2 ~4 ~2 minecraft:chiseled_stone_bricks
setblock ~2 ~1 ~-2 minecraft:chiseled_stone_bricks
fill ~2 ~2 ~-2 ~2 ~3 ~-2 minecraft:deepslate_brick_wall
setblock ~2 ~4 ~-2 minecraft:chiseled_stone_bricks
setblock ~2 ~1 ~2 minecraft:chiseled_stone_bricks
fill ~2 ~2 ~2 ~2 ~3 ~2 minecraft:deepslate_brick_wall
setblock ~2 ~4 ~2 minecraft:chiseled_stone_bricks
execute if block ~-4 ~4 ~-4 minecraft:air run setblock ~-4 ~4 ~-4 minecraft:light[level=13]
execute if block ~-4 ~4 ~0 minecraft:air run setblock ~-4 ~4 ~0 minecraft:light[level=13]
execute if block ~-4 ~4 ~4 minecraft:air run setblock ~-4 ~4 ~4 minecraft:light[level=13]
execute if block ~0 ~4 ~-4 minecraft:air run setblock ~0 ~4 ~-4 minecraft:light[level=13]
execute if block ~0 ~4 ~0 minecraft:air run setblock ~0 ~4 ~0 minecraft:light[level=13]
execute if block ~0 ~4 ~4 minecraft:air run setblock ~0 ~4 ~4 minecraft:light[level=13]
execute if block ~4 ~4 ~-4 minecraft:air run setblock ~4 ~4 ~-4 minecraft:light[level=13]
execute if block ~4 ~4 ~0 minecraft:air run setblock ~4 ~4 ~0 minecraft:light[level=13]
execute if block ~4 ~4 ~4 minecraft:air run setblock ~4 ~4 ~4 minecraft:light[level=13]
execute unless score #sites rpg_pl matches 1 positioned ~-30 ~ ~-30 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_medium_180
execute unless score #sites rpg_pl matches 1 positioned ~15 ~ ~-37 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/house_small_counterclockwise_90
execute unless score #sites rpg_pl matches 1 positioned ~38 ~ ~0 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_small_none
execute unless score #sites rpg_pl matches 1 positioned ~14 ~ ~33 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/tower_small_clockwise_90
execute unless score #sites rpg_pl matches 1 positioned ~-29 ~ ~29 positioned over motion_blocking_no_leaves run function rpg:pl/build/site/house_small_180
