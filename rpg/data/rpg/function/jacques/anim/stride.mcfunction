# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_jqm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_jqm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_jqm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_jqm = #x rpg_jqm
scoreboard players operation #dx rpg_jqm -= @s rpg_jqm_x
scoreboard players operation #dz rpg_jqm = #z rpg_jqm
scoreboard players operation #dz rpg_jqm -= @s rpg_jqm_z
scoreboard players operation @s rpg_jqm_x = #x rpg_jqm
scoreboard players operation @s rpg_jqm_z = #z rpg_jqm
scoreboard players operation #dx rpg_jqm *= #dx rpg_jqm
scoreboard players operation #dz rpg_jqm *= #dz rpg_jqm
scoreboard players operation #dx rpg_jqm += #dz rpg_jqm
execute store success score @s rpg_jqm_mv if score #dx rpg_jqm matches 64..
