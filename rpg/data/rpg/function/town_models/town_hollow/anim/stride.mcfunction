# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_tw_m12_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_tw_m12 run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_tw_m12 run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_tw_m12 = #x rpg_tw_m12
scoreboard players operation #dx rpg_tw_m12 -= @s rpg_tw_m12_x
scoreboard players operation #dz rpg_tw_m12 = #z rpg_tw_m12
scoreboard players operation #dz rpg_tw_m12 -= @s rpg_tw_m12_z
scoreboard players operation @s rpg_tw_m12_x = #x rpg_tw_m12
scoreboard players operation @s rpg_tw_m12_z = #z rpg_tw_m12
scoreboard players operation #dx rpg_tw_m12 *= #dx rpg_tw_m12
scoreboard players operation #dz rpg_tw_m12 *= #dz rpg_tw_m12
scoreboard players operation #dx rpg_tw_m12 += #dz rpg_tw_m12
execute store success score @s rpg_tw_m12_mv if score #dx rpg_tw_m12 matches 64..
