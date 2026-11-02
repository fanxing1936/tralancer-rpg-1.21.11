# 利维坦动画（as 载体）。rpg_lv_anim = 当前片段，rpg_lv_t = 已播放刻数。
execute unless score @s rpg_lv_anim matches 0.. run function rpg:leviathan/anim/init
# 水平位移（百分之一格）的平方 >= 4 记为在走；停下 4 刻后才回 idle，免得来回抖
execute store result score #x rpg_lv run data get entity @s Pos[0] 100
execute store result score #z rpg_lv run data get entity @s Pos[2] 100
scoreboard players operation #dx rpg_lv = #x rpg_lv
scoreboard players operation #dx rpg_lv -= @s rpg_lv_x
scoreboard players operation #dz rpg_lv = #z rpg_lv
scoreboard players operation #dz rpg_lv -= @s rpg_lv_z
scoreboard players operation @s rpg_lv_x = #x rpg_lv
scoreboard players operation @s rpg_lv_z = #z rpg_lv
scoreboard players operation #dx rpg_lv *= #dx rpg_lv
scoreboard players operation #dz rpg_lv *= #dz rpg_lv
scoreboard players operation #dx rpg_lv += #dz rpg_lv
execute if score #dx rpg_lv matches 4.. run scoreboard players set @s rpg_lv_mv 4
execute if score #dx rpg_lv matches ..3 if score @s rpg_lv_mv matches 1.. run scoreboard players remove @s rpg_lv_mv 1
execute if score @s rpg_lv_anim matches 0 if score @s rpg_lv_mv matches 1.. run return run function rpg:leviathan/anim/enter/walk
execute if score @s rpg_lv_anim matches 1 if score @s rpg_lv_mv matches 0 run return run function rpg:leviathan/anim/enter/idle
execute if score @s rpg_lv_anim matches 0 run return run function rpg:leviathan/anim/idle/tick
execute if score @s rpg_lv_anim matches 1 run return run function rpg:leviathan/anim/walk/tick
execute if score @s rpg_lv_anim matches 2 run return run function rpg:leviathan/anim/cast/tick
execute if score @s rpg_lv_anim matches 3 run return run function rpg:leviathan/anim/summon/tick
execute if score @s rpg_lv_anim matches 4 run return run function rpg:leviathan/anim/rise/tick
