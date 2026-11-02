# 沉没罪仆动画（as 载体）。rpg_sk_anim = 当前片段，rpg_sk_t = 已播放刻数。
execute unless score @s rpg_sk_anim matches 0.. run function rpg:sunken_skeleton/anim/init
# 水平位移（百分之一格）的平方 >= 4 记为在走；停下 4 刻后才回 idle，免得来回抖
execute store result score #x rpg_sk run data get entity @s Pos[0] 100
execute store result score #z rpg_sk run data get entity @s Pos[2] 100
scoreboard players operation #dx rpg_sk = #x rpg_sk
scoreboard players operation #dx rpg_sk -= @s rpg_sk_x
scoreboard players operation #dz rpg_sk = #z rpg_sk
scoreboard players operation #dz rpg_sk -= @s rpg_sk_z
scoreboard players operation @s rpg_sk_x = #x rpg_sk
scoreboard players operation @s rpg_sk_z = #z rpg_sk
scoreboard players operation #dx rpg_sk *= #dx rpg_sk
scoreboard players operation #dz rpg_sk *= #dz rpg_sk
scoreboard players operation #dx rpg_sk += #dz rpg_sk
execute if score #dx rpg_sk matches 4.. run scoreboard players set @s rpg_sk_mv 4
execute if score #dx rpg_sk matches ..3 if score @s rpg_sk_mv matches 1.. run scoreboard players remove @s rpg_sk_mv 1
execute if score @s rpg_sk_anim matches 0 if score @s rpg_sk_mv matches 1.. run return run function rpg:sunken_skeleton/anim/enter/walk
execute if score @s rpg_sk_anim matches 1 if score @s rpg_sk_mv matches 0 run return run function rpg:sunken_skeleton/anim/enter/idle
execute if score @s rpg_sk_anim matches 0 run return run function rpg:sunken_skeleton/anim/idle/tick
execute if score @s rpg_sk_anim matches 1 run return run function rpg:sunken_skeleton/anim/walk/tick
execute if score @s rpg_sk_anim matches 2 run return run function rpg:sunken_skeleton/anim/attack/tick
execute if score @s rpg_sk_anim matches 3 run return run function rpg:sunken_skeleton/anim/shoot/tick
