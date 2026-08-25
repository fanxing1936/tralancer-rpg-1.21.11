tag @s add rpg.divine.hit
execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/beam
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #four rpg_lt_max
scoreboard players add @s rpg_lt_max 1500
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
effect give @s minecraft:glowing 8 0 true
effect give @s minecraft:weakness 6 0 true
particle minecraft:flash{color:8641023} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:end_rod ~ ~1 ~ 0.45 0.7 0.45 0.04 30 force
