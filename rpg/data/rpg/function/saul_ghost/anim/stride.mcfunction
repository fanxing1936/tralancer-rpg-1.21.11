# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_slgm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_slgm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_slgm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_slgm = #x rpg_slgm
scoreboard players operation #dx rpg_slgm -= @s rpg_slgm_x
scoreboard players operation #dz rpg_slgm = #z rpg_slgm
scoreboard players operation #dz rpg_slgm -= @s rpg_slgm_z
scoreboard players operation @s rpg_slgm_x = #x rpg_slgm
scoreboard players operation @s rpg_slgm_z = #z rpg_slgm
scoreboard players operation #dx rpg_slgm *= #dx rpg_slgm
scoreboard players operation #dz rpg_slgm *= #dz rpg_slgm
scoreboard players operation #dx rpg_slgm += #dz rpg_slgm
execute store success score @s rpg_slgm_mv if score #dx rpg_slgm matches 64..
