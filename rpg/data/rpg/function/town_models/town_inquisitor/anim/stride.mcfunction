# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_tw_m6_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_tw_m6 run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_tw_m6 run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_tw_m6 = #x rpg_tw_m6
scoreboard players operation #dx rpg_tw_m6 -= @s rpg_tw_m6_x
scoreboard players operation #dz rpg_tw_m6 = #z rpg_tw_m6
scoreboard players operation #dz rpg_tw_m6 -= @s rpg_tw_m6_z
scoreboard players operation @s rpg_tw_m6_x = #x rpg_tw_m6
scoreboard players operation @s rpg_tw_m6_z = #z rpg_tw_m6
scoreboard players operation #dx rpg_tw_m6 *= #dx rpg_tw_m6
scoreboard players operation #dz rpg_tw_m6 *= #dz rpg_tw_m6
scoreboard players operation #dx rpg_tw_m6 += #dz rpg_tw_m6
execute store success score @s rpg_tw_m6_mv if score #dx rpg_tw_m6 matches 64..
