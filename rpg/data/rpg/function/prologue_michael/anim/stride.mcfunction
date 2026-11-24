# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_prmi_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_prmi run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_prmi run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_prmi = #x rpg_prmi
scoreboard players operation #dx rpg_prmi -= @s rpg_prmi_x
scoreboard players operation #dz rpg_prmi = #z rpg_prmi
scoreboard players operation #dz rpg_prmi -= @s rpg_prmi_z
scoreboard players operation @s rpg_prmi_x = #x rpg_prmi
scoreboard players operation @s rpg_prmi_z = #z rpg_prmi
scoreboard players operation #dx rpg_prmi *= #dx rpg_prmi
scoreboard players operation #dz rpg_prmi *= #dz rpg_prmi
scoreboard players operation #dx rpg_prmi += #dz rpg_prmi
execute store success score @s rpg_prmi_mv if score #dx rpg_prmi matches 64..
