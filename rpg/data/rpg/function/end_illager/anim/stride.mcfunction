# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_ei_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_ei run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_ei run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_ei = #x rpg_ei
scoreboard players operation #dx rpg_ei -= @s rpg_ei_x
scoreboard players operation #dz rpg_ei = #z rpg_ei
scoreboard players operation #dz rpg_ei -= @s rpg_ei_z
scoreboard players operation @s rpg_ei_x = #x rpg_ei
scoreboard players operation @s rpg_ei_z = #z rpg_ei
scoreboard players operation #dx rpg_ei *= #dx rpg_ei
scoreboard players operation #dz rpg_ei *= #dz rpg_ei
scoreboard players operation #dx rpg_ei += #dz rpg_ei
execute store success score @s rpg_ei_mv if score #dx rpg_ei matches 64..
