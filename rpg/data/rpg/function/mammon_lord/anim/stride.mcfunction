# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_mml_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_mml run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_mml run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_mml = #x rpg_mml
scoreboard players operation #dx rpg_mml -= @s rpg_mml_x
scoreboard players operation #dz rpg_mml = #z rpg_mml
scoreboard players operation #dz rpg_mml -= @s rpg_mml_z
scoreboard players operation @s rpg_mml_x = #x rpg_mml
scoreboard players operation @s rpg_mml_z = #z rpg_mml
scoreboard players operation #dx rpg_mml *= #dx rpg_mml
scoreboard players operation #dz rpg_mml *= #dz rpg_mml
scoreboard players operation #dx rpg_mml += #dz rpg_mml
execute store success score @s rpg_mml_mv if score #dx rpg_mml matches 64..
