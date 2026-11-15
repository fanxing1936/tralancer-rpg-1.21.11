# 握着坟墓克星打中了一下。连击按 gametime 量间隔，不依赖每刻倒数。
execute store result score #now rpg_gb_tmp run time query gametime
scoreboard players operation #gap rpg_gb_tmp = #now rpg_gb_tmp
scoreboard players operation #gap rpg_gb_tmp -= @s rpg_gb_last
# 没蓄满的连点不算一下
execute if score @s rpg_gb_combo matches 1.. if score #gap rpg_gb_tmp matches ..11 run return 0
execute if score #gap rpg_gb_tmp matches 41.. run scoreboard players set @s rpg_gb_combo 0
scoreboard players operation @s rpg_gb_last = #now rpg_gb_tmp
scoreboard players add @s rpg_gb_combo 1
execute if score @s rpg_gb_combo matches ..2 anchored eyes positioned ^ ^-0.4 ^1.6 run particle dust{color:[1.0,0.85,0.35],scale:0.7} ~ ~ ~ 0.3 0.2 0.3 0 4
execute if score @s rpg_gb_combo matches 3.. run function rpg:item/extra/grave_bane_sweep
execute if score @s rpg_gb_combo matches 3.. run scoreboard players set @s rpg_gb_combo 0
