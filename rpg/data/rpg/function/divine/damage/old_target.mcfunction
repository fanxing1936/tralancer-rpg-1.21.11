execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/old
execute store result score @s rpg_lt_hp run data get entity @s Health 100
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #four rpg_lt_max
execute unless score @s rpg_ex_stage matches 1 if score @s rpg_lt_hp <= @s rpg_lt_max run return run function rpg:divine/damage/execute
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #five rpg_lt_max
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.8 0.5 0.1 24 force
