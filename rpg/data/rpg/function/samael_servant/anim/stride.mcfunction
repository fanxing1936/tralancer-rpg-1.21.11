# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_sms_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_sms run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_sms run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_sms = #x rpg_sms
scoreboard players operation #dx rpg_sms -= @s rpg_sms_x
scoreboard players operation #dz rpg_sms = #z rpg_sms
scoreboard players operation #dz rpg_sms -= @s rpg_sms_z
scoreboard players operation @s rpg_sms_x = #x rpg_sms
scoreboard players operation @s rpg_sms_z = #z rpg_sms
scoreboard players operation #dx rpg_sms *= #dx rpg_sms
scoreboard players operation #dz rpg_sms *= #dz rpg_sms
scoreboard players operation #dx rpg_sms += #dz rpg_sms
execute store success score @s rpg_sms_mv if score #dx rpg_sms matches 64..
