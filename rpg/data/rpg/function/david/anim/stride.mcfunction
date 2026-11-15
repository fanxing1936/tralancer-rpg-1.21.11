# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_jqdm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_jqdm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_jqdm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_jqdm = #x rpg_jqdm
scoreboard players operation #dx rpg_jqdm -= @s rpg_jqdm_x
scoreboard players operation #dz rpg_jqdm = #z rpg_jqdm
scoreboard players operation #dz rpg_jqdm -= @s rpg_jqdm_z
scoreboard players operation @s rpg_jqdm_x = #x rpg_jqdm
scoreboard players operation @s rpg_jqdm_z = #z rpg_jqdm
scoreboard players operation #dx rpg_jqdm *= #dx rpg_jqdm
scoreboard players operation #dz rpg_jqdm *= #dz rpg_jqdm
scoreboard players operation #dx rpg_jqdm += #dz rpg_jqdm
execute store success score @s rpg_jqdm_mv if score #dx rpg_jqdm matches 64..
