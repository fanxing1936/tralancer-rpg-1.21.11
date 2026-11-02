# 先锋罪仆动画（as 载体）。rpg_vg_anim = 当前片段，rpg_vg_t = 已播放刻数。
execute unless score @s rpg_vg_anim matches 0.. run function rpg:vanguard/anim/init
# 水平位移（百分之一格）的平方 >= 4 记为在走；停下 4 刻后才回 idle，免得来回抖
execute store result score #x rpg_vg run data get entity @s Pos[0] 100
execute store result score #z rpg_vg run data get entity @s Pos[2] 100
scoreboard players operation #dx rpg_vg = #x rpg_vg
scoreboard players operation #dx rpg_vg -= @s rpg_vg_x
scoreboard players operation #dz rpg_vg = #z rpg_vg
scoreboard players operation #dz rpg_vg -= @s rpg_vg_z
scoreboard players operation @s rpg_vg_x = #x rpg_vg
scoreboard players operation @s rpg_vg_z = #z rpg_vg
scoreboard players operation #dx rpg_vg *= #dx rpg_vg
scoreboard players operation #dz rpg_vg *= #dz rpg_vg
scoreboard players operation #dx rpg_vg += #dz rpg_vg
execute if score #dx rpg_vg matches 4.. run scoreboard players set @s rpg_vg_mv 4
execute if score #dx rpg_vg matches ..3 if score @s rpg_vg_mv matches 1.. run scoreboard players remove @s rpg_vg_mv 1
execute if score @s rpg_vg_anim matches 0 if score @s rpg_vg_mv matches 1.. run return run function rpg:vanguard/anim/enter/walk
execute if score @s rpg_vg_anim matches 1 if score @s rpg_vg_mv matches 0 run return run function rpg:vanguard/anim/enter/idle
execute if score @s rpg_vg_anim matches 0 run return run function rpg:vanguard/anim/idle/tick
execute if score @s rpg_vg_anim matches 1 run return run function rpg:vanguard/anim/walk/tick
execute if score @s rpg_vg_anim matches 2 run return run function rpg:vanguard/anim/attack/tick
execute if score @s rpg_vg_anim matches 3 run return run function rpg:vanguard/anim/break/tick
