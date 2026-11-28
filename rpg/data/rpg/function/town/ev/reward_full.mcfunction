# 奖励（as 参与者）：#kind 1 驱魔 2 战斗 3 世界观
scoreboard players operation #t rpg_tl = #run rpg_te
function rpg:town/life/rep_add {n:20}
function rpg:events/bt/town_event
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
execute if score #kind rpg_te matches 1 run function rpg:alc/give/holy
execute if score #kind rpg_te matches 1 run loot give @s loot rpg:potion/blank_rite
execute if score #kind rpg_te matches 2 run loot give @s loot rpg:loot/loot
execute if score #kind rpg_te matches 2 run loot give @s loot rpg:forge/item/forge_stone
execute if score #kind rpg_te matches 3 run loot give @s loot rpg:world/sin_shard_6
execute if score #kind rpg_te matches 3 if entity @s[tag=rpg.dm] run loot give @s loot rpg:world/sin_shard_6
execute if score #kind rpg_te matches 3 if entity @s[tag=rpg.dm] run loot give @s loot rpg:world/currency
