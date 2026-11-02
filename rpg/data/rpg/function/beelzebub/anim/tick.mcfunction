# 别西卜动画（as 载体）。rpg_bz_anim = 当前片段，rpg_bz_t = 已播放刻数。
execute unless score @s rpg_bz_anim matches 0.. run function rpg:beelzebub/anim/init
# 水平位移（百分之一格）的平方 >= 4 记为在走；停下 4 刻后才回 idle，免得来回抖
execute store result score #x rpg_bz run data get entity @s Pos[0] 100
execute store result score #z rpg_bz run data get entity @s Pos[2] 100
scoreboard players operation #dx rpg_bz = #x rpg_bz
scoreboard players operation #dx rpg_bz -= @s rpg_bz_x
scoreboard players operation #dz rpg_bz = #z rpg_bz
scoreboard players operation #dz rpg_bz -= @s rpg_bz_z
scoreboard players operation @s rpg_bz_x = #x rpg_bz
scoreboard players operation @s rpg_bz_z = #z rpg_bz
scoreboard players operation #dx rpg_bz *= #dx rpg_bz
scoreboard players operation #dz rpg_bz *= #dz rpg_bz
scoreboard players operation #dx rpg_bz += #dz rpg_bz
execute if score #dx rpg_bz matches 4.. run scoreboard players set @s rpg_bz_mv 4
execute if score #dx rpg_bz matches ..3 if score @s rpg_bz_mv matches 1.. run scoreboard players remove @s rpg_bz_mv 1
execute if score @s rpg_bz_anim matches 0 if score @s rpg_bz_mv matches 1.. run return run function rpg:beelzebub/anim/enter/walk
execute if score @s rpg_bz_anim matches 1 if score @s rpg_bz_mv matches 0 run return run function rpg:beelzebub/anim/enter/idle
execute if score @s rpg_bz_anim matches 0 run return run function rpg:beelzebub/anim/idle/tick
execute if score @s rpg_bz_anim matches 1 run return run function rpg:beelzebub/anim/walk/tick
execute if score @s rpg_bz_anim matches 2 run return run function rpg:beelzebub/anim/cast/tick
execute if score @s rpg_bz_anim matches 3 run return run function rpg:beelzebub/anim/summon/tick
execute if score @s rpg_bz_anim matches 4 run return run function rpg:beelzebub/anim/rise/tick
