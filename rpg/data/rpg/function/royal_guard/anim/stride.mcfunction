# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_rg_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_rg run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_rg run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_rg = #x rpg_rg
scoreboard players operation #dx rpg_rg -= @s rpg_rg_x
scoreboard players operation #dz rpg_rg = #z rpg_rg
scoreboard players operation #dz rpg_rg -= @s rpg_rg_z
scoreboard players operation @s rpg_rg_x = #x rpg_rg
scoreboard players operation @s rpg_rg_z = #z rpg_rg
scoreboard players operation #dx rpg_rg *= #dx rpg_rg
scoreboard players operation #dz rpg_rg *= #dz rpg_rg
scoreboard players operation #dx rpg_rg += #dz rpg_rg
execute store success score @s rpg_rg_mv if score #dx rpg_rg matches 64..
