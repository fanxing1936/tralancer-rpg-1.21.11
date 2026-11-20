# 身上有圣焰（as/at 玩家）
scoreboard players remove @s rpg_mk_ft 1
execute if score @s rpg_mk_ft matches ..0 run scoreboard players set @s rpg_mk_fl 0
execute if score @s rpg_mk_fl matches 1.. run particle minecraft:small_flame ~ ~1 ~ 0.3 0.5 0.3 0.01 1
execute if score @s rpg_mk_fl matches 2.. run particle minecraft:flame ~ ~1.2 ~ 0.3 0.5 0.3 0.01 1
execute if score @s rpg_mk_fu matches 1.. run scoreboard players remove @s rpg_mk_fu 1
execute if score @s rpg_mk_fu matches 1.. run particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.03 4
execute if score @s rpg_mk_fu matches 0 run function rpg:michael_boss/flame/burst
execute if score @s rpg_mk_r matches 1.. run function rpg:michael_boss/flame/burn
execute unless score @s rpg_mk_fl matches 1.. unless score @s rpg_mk_fu matches 1.. unless score @s rpg_mk_r matches 1.. run function rpg:michael_boss/flame/out
