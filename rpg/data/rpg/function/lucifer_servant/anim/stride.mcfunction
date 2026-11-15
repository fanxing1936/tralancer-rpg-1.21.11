# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_lcs_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_lcs run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_lcs run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_lcs = #x rpg_lcs
scoreboard players operation #dx rpg_lcs -= @s rpg_lcs_x
scoreboard players operation #dz rpg_lcs = #z rpg_lcs
scoreboard players operation #dz rpg_lcs -= @s rpg_lcs_z
scoreboard players operation @s rpg_lcs_x = #x rpg_lcs
scoreboard players operation @s rpg_lcs_z = #z rpg_lcs
scoreboard players operation #dx rpg_lcs *= #dx rpg_lcs
scoreboard players operation #dz rpg_lcs *= #dz rpg_lcs
scoreboard players operation #dx rpg_lcs += #dz rpg_lcs
execute store success score @s rpg_lcs_mv if score #dx rpg_lcs matches 64..
