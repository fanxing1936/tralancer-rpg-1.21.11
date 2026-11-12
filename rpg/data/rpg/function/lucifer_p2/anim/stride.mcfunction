# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_lu2_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_lu2 run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_lu2 run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_lu2 = #x rpg_lu2
scoreboard players operation #dx rpg_lu2 -= @s rpg_lu2_x
scoreboard players operation #dz rpg_lu2 = #z rpg_lu2
scoreboard players operation #dz rpg_lu2 -= @s rpg_lu2_z
scoreboard players operation @s rpg_lu2_x = #x rpg_lu2
scoreboard players operation @s rpg_lu2_z = #z rpg_lu2
scoreboard players operation #dx rpg_lu2 *= #dx rpg_lu2
scoreboard players operation #dz rpg_lu2 *= #dz rpg_lu2
scoreboard players operation #dx rpg_lu2 += #dz rpg_lu2
execute store success score @s rpg_lu2_mv if score #dx rpg_lu2 matches 64..
