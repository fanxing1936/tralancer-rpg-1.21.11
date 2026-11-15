# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_usm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_usm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_usm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_usm = #x rpg_usm
scoreboard players operation #dx rpg_usm -= @s rpg_usm_x
scoreboard players operation #dz rpg_usm = #z rpg_usm
scoreboard players operation #dz rpg_usm -= @s rpg_usm_z
scoreboard players operation @s rpg_usm_x = #x rpg_usm
scoreboard players operation @s rpg_usm_z = #z rpg_usm
scoreboard players operation #dx rpg_usm *= #dx rpg_usm
scoreboard players operation #dz rpg_usm *= #dz rpg_usm
scoreboard players operation #dx rpg_usm += #dz rpg_usm
execute store success score @s rpg_usm_mv if score #dx rpg_usm matches 64..
