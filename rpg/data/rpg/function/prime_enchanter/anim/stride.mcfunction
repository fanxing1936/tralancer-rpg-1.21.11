# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_pe_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_pe run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_pe run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_pe = #x rpg_pe
scoreboard players operation #dx rpg_pe -= @s rpg_pe_x
scoreboard players operation #dz rpg_pe = #z rpg_pe
scoreboard players operation #dz rpg_pe -= @s rpg_pe_z
scoreboard players operation @s rpg_pe_x = #x rpg_pe
scoreboard players operation @s rpg_pe_z = #z rpg_pe
scoreboard players operation #dx rpg_pe *= #dx rpg_pe
scoreboard players operation #dz rpg_pe *= #dz rpg_pe
scoreboard players operation #dx rpg_pe += #dz rpg_pe
execute store success score @s rpg_pe_mv if score #dx rpg_pe matches 64..
