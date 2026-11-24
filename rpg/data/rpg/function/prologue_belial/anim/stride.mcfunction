# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_prbl_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_prbl run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_prbl run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_prbl = #x rpg_prbl
scoreboard players operation #dx rpg_prbl -= @s rpg_prbl_x
scoreboard players operation #dz rpg_prbl = #z rpg_prbl
scoreboard players operation #dz rpg_prbl -= @s rpg_prbl_z
scoreboard players operation @s rpg_prbl_x = #x rpg_prbl
scoreboard players operation @s rpg_prbl_z = #z rpg_prbl
scoreboard players operation #dx rpg_prbl *= #dx rpg_prbl
scoreboard players operation #dz rpg_prbl *= #dz rpg_prbl
scoreboard players operation #dx rpg_prbl += #dz rpg_prbl
execute store success score @s rpg_prbl_mv if score #dx rpg_prbl matches 64..
