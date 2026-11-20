# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_slm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_slm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_slm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_slm = #x rpg_slm
scoreboard players operation #dx rpg_slm -= @s rpg_slm_x
scoreboard players operation #dz rpg_slm = #z rpg_slm
scoreboard players operation #dz rpg_slm -= @s rpg_slm_z
scoreboard players operation @s rpg_slm_x = #x rpg_slm
scoreboard players operation @s rpg_slm_z = #z rpg_slm
scoreboard players operation #dx rpg_slm *= #dx rpg_slm
scoreboard players operation #dz rpg_slm *= #dz rpg_slm
scoreboard players operation #dx rpg_slm += #dz rpg_slm
execute store success score @s rpg_slm_mv if score #dx rpg_slm matches 64..
