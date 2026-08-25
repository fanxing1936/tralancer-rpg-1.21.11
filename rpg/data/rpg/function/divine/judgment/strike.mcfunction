execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/judgment
effect clear @s minecraft:regeneration
effect clear @s minecraft:resistance
effect clear @s minecraft:absorption
effect clear @s minecraft:strength
effect clear @s minecraft:speed
effect clear @s minecraft:invisibility
effect clear @s minecraft:fire_resistance
effect give @s minecraft:glowing 10 0 true
effect give @s minecraft:weakness 8 1 true
execute store result score @s rpg_lt_hp run data get entity @s Health 100
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #five rpg_lt_max
execute unless score @s rpg_ex_stage matches 1 if score @s rpg_lt_hp <= @s rpg_lt_max run return run function rpg:divine/damage/execute
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #five rpg_lt_max
scoreboard players add @s rpg_lt_max 1000
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
particle minecraft:flash{color:15594751} ~ ~1 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.38,0.85,0.91],to_color:[1.0,0.95,0.66],scale:2.0} ~ ~1 ~ 0.65 0.85 0.65 0.08 48 force
particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.7 0.5 0.12 36 force
