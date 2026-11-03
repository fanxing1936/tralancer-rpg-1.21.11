# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_bz_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_bz run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_bz run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_bz = #x rpg_bz
scoreboard players operation #dx rpg_bz -= @s rpg_bz_x
scoreboard players operation #dz rpg_bz = #z rpg_bz
scoreboard players operation #dz rpg_bz -= @s rpg_bz_z
scoreboard players operation @s rpg_bz_x = #x rpg_bz
scoreboard players operation @s rpg_bz_z = #z rpg_bz
scoreboard players operation #dx rpg_bz *= #dx rpg_bz
scoreboard players operation #dz rpg_bz *= #dz rpg_bz
scoreboard players operation #dx rpg_bz += #dz rpg_bz
execute store success score @s rpg_bz_mv if score #dx rpg_bz matches 64..
