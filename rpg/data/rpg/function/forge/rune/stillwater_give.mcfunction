execute store result score #t rpg_fg run data get entity @s AbsorptionAmount
execute if score #t rpg_fg matches 1.. run return 0
effect clear @s minecraft:absorption
effect give @s minecraft:absorption 30 0 true
particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0.02 10
