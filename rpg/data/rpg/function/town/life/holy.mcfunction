# 每秒（as 玩家）
effect give @s minecraft:resistance 3 0 true
scoreboard players operation #e rpg_tl = #gt rpg_tl
scoreboard players operation #e rpg_tl -= @s rpg_tl_born
execute if score #e rpg_tl matches 48000.. run return run function rpg:town/life/holy_end
execute if score @s rpg_sef matches 2.. run function rpg:town/life/holy_end
