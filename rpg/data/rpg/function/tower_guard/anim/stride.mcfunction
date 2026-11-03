# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_tg_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_tg run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_tg run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_tg = #x rpg_tg
scoreboard players operation #dx rpg_tg -= @s rpg_tg_x
scoreboard players operation #dz rpg_tg = #z rpg_tg
scoreboard players operation #dz rpg_tg -= @s rpg_tg_z
scoreboard players operation @s rpg_tg_x = #x rpg_tg
scoreboard players operation @s rpg_tg_z = #z rpg_tg
scoreboard players operation #dx rpg_tg *= #dx rpg_tg
scoreboard players operation #dz rpg_tg *= #dz rpg_tg
scoreboard players operation #dx rpg_tg += #dz rpg_tg
execute store success score @s rpg_tg_mv if score #dx rpg_tg matches 64..
