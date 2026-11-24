# 暴怒：每次受伤 +2%（美丽阶起 +4%），最多 5 层；8 秒不受伤清零
execute if score @s rpg_fo_dw matches 1.. run scoreboard players add @s rpg_fo_ws 1
execute if score @s rpg_fo_dw matches 1.. run scoreboard players operation @s rpg_fo_wt = #now rpg_fo
scoreboard players set @s rpg_fo_dw 0
execute if score @s rpg_fo_ws matches 6.. run scoreboard players set @s rpg_fo_ws 5
scoreboard players operation #q rpg_fo = #now rpg_fo
scoreboard players operation #q rpg_fo -= @s rpg_fo_wt
execute if score #q rpg_fo matches 160.. run scoreboard players set @s rpg_fo_ws 0
attribute @s minecraft:attack_damage modifier remove rpg:fo_sin
execute unless score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 1 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.02 add_multiplied_total
execute if score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 1 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.04 add_multiplied_total
execute unless score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 2 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.04 add_multiplied_total
execute if score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 2 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.08 add_multiplied_total
execute unless score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 3 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.06 add_multiplied_total
execute if score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 3 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.12 add_multiplied_total
execute unless score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 4 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.08 add_multiplied_total
execute if score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 4 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.16 add_multiplied_total
execute unless score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 5 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.10 add_multiplied_total
execute if score @s rpg_sef matches 5.. run execute if score @s rpg_fo_ws matches 5 run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.20 add_multiplied_total
