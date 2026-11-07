# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_pp_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_pp run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_pp run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_pp = #x rpg_pp
scoreboard players operation #dx rpg_pp -= @s rpg_pp_x
scoreboard players operation #dz rpg_pp = #z rpg_pp
scoreboard players operation #dz rpg_pp -= @s rpg_pp_z
scoreboard players operation @s rpg_pp_x = #x rpg_pp
scoreboard players operation @s rpg_pp_z = #z rpg_pp
scoreboard players operation #dx rpg_pp *= #dx rpg_pp
scoreboard players operation #dz rpg_pp *= #dz rpg_pp
scoreboard players operation #dx rpg_pp += #dz rpg_pp
execute store success score @s rpg_pp_mv if score #dx rpg_pp matches 64..
