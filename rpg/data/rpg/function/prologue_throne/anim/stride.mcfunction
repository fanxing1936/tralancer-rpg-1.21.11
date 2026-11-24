# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_prth_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_prth run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_prth run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_prth = #x rpg_prth
scoreboard players operation #dx rpg_prth -= @s rpg_prth_x
scoreboard players operation #dz rpg_prth = #z rpg_prth
scoreboard players operation #dz rpg_prth -= @s rpg_prth_z
scoreboard players operation @s rpg_prth_x = #x rpg_prth
scoreboard players operation @s rpg_prth_z = #z rpg_prth
scoreboard players operation #dx rpg_prth *= #dx rpg_prth
scoreboard players operation #dz rpg_prth *= #dz rpg_prth
scoreboard players operation #dx rpg_prth += #dz rpg_prth
execute store success score @s rpg_prth_mv if score #dx rpg_prth matches 64..
