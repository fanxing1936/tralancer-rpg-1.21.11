# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_mis_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_mis run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_mis run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_mis = #x rpg_mis
scoreboard players operation #dx rpg_mis -= @s rpg_mis_x
scoreboard players operation #dz rpg_mis = #z rpg_mis
scoreboard players operation #dz rpg_mis -= @s rpg_mis_z
scoreboard players operation @s rpg_mis_x = #x rpg_mis
scoreboard players operation @s rpg_mis_z = #z rpg_mis
scoreboard players operation #dx rpg_mis *= #dx rpg_mis
scoreboard players operation #dz rpg_mis *= #dz rpg_mis
scoreboard players operation #dx rpg_mis += #dz rpg_mis
execute store success score @s rpg_mis_mv if score #dx rpg_mis matches 64..
