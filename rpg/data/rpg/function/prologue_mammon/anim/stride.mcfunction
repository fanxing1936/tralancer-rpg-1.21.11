# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_prmm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_prmm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_prmm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_prmm = #x rpg_prmm
scoreboard players operation #dx rpg_prmm -= @s rpg_prmm_x
scoreboard players operation #dz rpg_prmm = #z rpg_prmm
scoreboard players operation #dz rpg_prmm -= @s rpg_prmm_z
scoreboard players operation @s rpg_prmm_x = #x rpg_prmm
scoreboard players operation @s rpg_prmm_z = #z rpg_prmm
scoreboard players operation #dx rpg_prmm *= #dx rpg_prmm
scoreboard players operation #dz rpg_prmm *= #dz rpg_prmm
scoreboard players operation #dx rpg_prmm += #dz rpg_prmm
execute store success score @s rpg_prmm_mv if score #dx rpg_prmm matches 64..
