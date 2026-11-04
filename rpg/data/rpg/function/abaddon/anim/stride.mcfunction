# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_ab_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_ab run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_ab run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_ab = #x rpg_ab
scoreboard players operation #dx rpg_ab -= @s rpg_ab_x
scoreboard players operation #dz rpg_ab = #z rpg_ab
scoreboard players operation #dz rpg_ab -= @s rpg_ab_z
scoreboard players operation @s rpg_ab_x = #x rpg_ab
scoreboard players operation @s rpg_ab_z = #z rpg_ab
scoreboard players operation #dx rpg_ab *= #dx rpg_ab
scoreboard players operation #dz rpg_ab *= #dz rpg_ab
scoreboard players operation #dx rpg_ab += #dz rpg_ab
execute store success score @s rpg_ab_mv if score #dx rpg_ab matches 64..
