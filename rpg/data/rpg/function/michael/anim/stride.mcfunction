# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_mkm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_mkm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_mkm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_mkm = #x rpg_mkm
scoreboard players operation #dx rpg_mkm -= @s rpg_mkm_x
scoreboard players operation #dz rpg_mkm = #z rpg_mkm
scoreboard players operation #dz rpg_mkm -= @s rpg_mkm_z
scoreboard players operation @s rpg_mkm_x = #x rpg_mkm
scoreboard players operation @s rpg_mkm_z = #z rpg_mkm
scoreboard players operation #dx rpg_mkm *= #dx rpg_mkm
scoreboard players operation #dz rpg_mkm *= #dz rpg_mkm
scoreboard players operation #dx rpg_mkm += #dz rpg_mkm
execute store success score @s rpg_mkm_mv if score #dx rpg_mkm matches 64..
