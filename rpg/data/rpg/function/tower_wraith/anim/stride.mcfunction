# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_tw_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_tw run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_tw run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_tw = #x rpg_tw
scoreboard players operation #dx rpg_tw -= @s rpg_tw_x
scoreboard players operation #dz rpg_tw = #z rpg_tw
scoreboard players operation #dz rpg_tw -= @s rpg_tw_z
scoreboard players operation @s rpg_tw_x = #x rpg_tw
scoreboard players operation @s rpg_tw_z = #z rpg_tw
scoreboard players operation #dx rpg_tw *= #dx rpg_tw
scoreboard players operation #dz rpg_tw *= #dz rpg_tw
scoreboard players operation #dx rpg_tw += #dz rpg_tw
execute store success score @s rpg_tw_mv if score #dx rpg_tw matches 64..
