# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_tw_m11_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_tw_m11 run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_tw_m11 run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_tw_m11 = #x rpg_tw_m11
scoreboard players operation #dx rpg_tw_m11 -= @s rpg_tw_m11_x
scoreboard players operation #dz rpg_tw_m11 = #z rpg_tw_m11
scoreboard players operation #dz rpg_tw_m11 -= @s rpg_tw_m11_z
scoreboard players operation @s rpg_tw_m11_x = #x rpg_tw_m11
scoreboard players operation @s rpg_tw_m11_z = #z rpg_tw_m11
scoreboard players operation #dx rpg_tw_m11 *= #dx rpg_tw_m11
scoreboard players operation #dz rpg_tw_m11 *= #dz rpg_tw_m11
scoreboard players operation #dx rpg_tw_m11 += #dz rpg_tw_m11
execute store success score @s rpg_tw_m11_mv if score #dx rpg_tw_m11 matches 64..
