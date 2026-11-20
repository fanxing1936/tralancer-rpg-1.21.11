# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_mkwm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_mkwm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_mkwm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_mkwm = #x rpg_mkwm
scoreboard players operation #dx rpg_mkwm -= @s rpg_mkwm_x
scoreboard players operation #dz rpg_mkwm = #z rpg_mkwm
scoreboard players operation #dz rpg_mkwm -= @s rpg_mkwm_z
scoreboard players operation @s rpg_mkwm_x = #x rpg_mkwm
scoreboard players operation @s rpg_mkwm_z = #z rpg_mkwm
scoreboard players operation #dx rpg_mkwm *= #dx rpg_mkwm
scoreboard players operation #dz rpg_mkwm *= #dz rpg_mkwm
scoreboard players operation #dx rpg_mkwm += #dz rpg_mkwm
execute store success score @s rpg_mkwm_mv if score #dx rpg_mkwm matches 64..
