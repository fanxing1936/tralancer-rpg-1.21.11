# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_mms_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_mms run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_mms run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_mms = #x rpg_mms
scoreboard players operation #dx rpg_mms -= @s rpg_mms_x
scoreboard players operation #dz rpg_mms = #z rpg_mms
scoreboard players operation #dz rpg_mms -= @s rpg_mms_z
scoreboard players operation @s rpg_mms_x = #x rpg_mms
scoreboard players operation @s rpg_mms_z = #z rpg_mms
scoreboard players operation #dx rpg_mms *= #dx rpg_mms
scoreboard players operation #dz rpg_mms *= #dz rpg_mms
scoreboard players operation #dx rpg_mms += #dz rpg_mms
execute store success score @s rpg_mms_mv if score #dx rpg_mms matches 64..
