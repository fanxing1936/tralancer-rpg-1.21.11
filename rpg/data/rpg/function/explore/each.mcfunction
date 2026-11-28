# 每秒（as/at 玩家）
execute if score @s rpg_x_cd matches 1.. run scoreboard players remove @s rpg_x_cd 1
execute if dimension minecraft:overworld run function rpg:explore/biome
function rpg:explore/dist
function rpg:explore/intel_check
function rpg:explore/mastery_check
execute if score @s rpg_x_do matches 1.. run function rpg:explore/do
execute if dimension rpg:paradise_lost run function rpg:explore/pl_ring
execute unless dimension rpg:paradise_lost run scoreboard players set @s rpg_x_pr 0
