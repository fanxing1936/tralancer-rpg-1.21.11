# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_sml_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_sml run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_sml run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_sml = #x rpg_sml
scoreboard players operation #dx rpg_sml -= @s rpg_sml_x
scoreboard players operation #dz rpg_sml = #z rpg_sml
scoreboard players operation #dz rpg_sml -= @s rpg_sml_z
scoreboard players operation @s rpg_sml_x = #x rpg_sml
scoreboard players operation @s rpg_sml_z = #z rpg_sml
scoreboard players operation #dx rpg_sml *= #dx rpg_sml
scoreboard players operation #dz rpg_sml *= #dz rpg_sml
scoreboard players operation #dx rpg_sml += #dz rpg_sml
execute store success score @s rpg_sml_mv if score #dx rpg_sml matches 64..
