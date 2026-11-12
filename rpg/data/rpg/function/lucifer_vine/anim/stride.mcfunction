# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_luv_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_luv run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_luv run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_luv = #x rpg_luv
scoreboard players operation #dx rpg_luv -= @s rpg_luv_x
scoreboard players operation #dz rpg_luv = #z rpg_luv
scoreboard players operation #dz rpg_luv -= @s rpg_luv_z
scoreboard players operation @s rpg_luv_x = #x rpg_luv
scoreboard players operation @s rpg_luv_z = #z rpg_luv
scoreboard players operation #dx rpg_luv *= #dx rpg_luv
scoreboard players operation #dz rpg_luv *= #dz rpg_luv
scoreboard players operation #dx rpg_luv += #dz rpg_luv
execute store success score @s rpg_luv_mv if score #dx rpg_luv matches 64..
