execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/field
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max *= #three rpg_lt_max
scoreboard players operation @s rpg_lt_max /= #twenty rpg_lt_max
scoreboard players add @s rpg_lt_max 1000
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
effect give @s minecraft:slowness 8 2 true
effect give @s minecraft:weakness 8 1 true
effect give @s minecraft:glowing 8 0 true
particle minecraft:enchanted_hit ~ ~1 ~ 0.8 0.8 0.8 0.12 35 force
particle minecraft:end_rod ~ ~0.8 ~ 0.6 0.7 0.6 0.04 24 force
