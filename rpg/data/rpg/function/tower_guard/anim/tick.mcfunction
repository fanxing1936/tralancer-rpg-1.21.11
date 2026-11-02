# 圣卫动画（as 载体）。rpg_tg_anim = 当前片段，rpg_tg_t = 已播放刻数。
execute unless score @s rpg_tg_anim matches 0.. run function rpg:tower_guard/anim/init
# 水平位移（百分之一格）的平方 >= 4 记为在走；停下 4 刻后才回 idle，免得来回抖
execute store result score #x rpg_tg run data get entity @s Pos[0] 100
execute store result score #z rpg_tg run data get entity @s Pos[2] 100
scoreboard players operation #dx rpg_tg = #x rpg_tg
scoreboard players operation #dx rpg_tg -= @s rpg_tg_x
scoreboard players operation #dz rpg_tg = #z rpg_tg
scoreboard players operation #dz rpg_tg -= @s rpg_tg_z
scoreboard players operation @s rpg_tg_x = #x rpg_tg
scoreboard players operation @s rpg_tg_z = #z rpg_tg
scoreboard players operation #dx rpg_tg *= #dx rpg_tg
scoreboard players operation #dz rpg_tg *= #dz rpg_tg
scoreboard players operation #dx rpg_tg += #dz rpg_tg
execute if score #dx rpg_tg matches 4.. run scoreboard players set @s rpg_tg_mv 4
execute if score #dx rpg_tg matches ..3 if score @s rpg_tg_mv matches 1.. run scoreboard players remove @s rpg_tg_mv 1
execute if score @s rpg_tg_anim matches 0 if score @s rpg_tg_mv matches 1.. run return run function rpg:tower_guard/anim/enter/walk
execute if score @s rpg_tg_anim matches 1 if score @s rpg_tg_mv matches 0 run return run function rpg:tower_guard/anim/enter/idle
execute if score @s rpg_tg_anim matches 0 run return run function rpg:tower_guard/anim/idle/tick
execute if score @s rpg_tg_anim matches 1 run return run function rpg:tower_guard/anim/walk/tick
execute if score @s rpg_tg_anim matches 2 run return run function rpg:tower_guard/anim/attack/tick
execute if score @s rpg_tg_anim matches 3 run return run function rpg:tower_guard/anim/charge/tick
execute if score @s rpg_tg_anim matches 4 run return run function rpg:tower_guard/anim/normal_stop/tick
execute if score @s rpg_tg_anim matches 5 run return run function rpg:tower_guard/anim/collide_stop/tick
execute if score @s rpg_tg_anim matches 6 run return run function rpg:tower_guard/anim/shield_break/tick
execute if score @s rpg_tg_anim matches 7 run return run function rpg:tower_guard/anim/stun/tick
