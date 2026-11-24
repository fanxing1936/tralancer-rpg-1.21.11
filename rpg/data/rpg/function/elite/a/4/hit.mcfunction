execute store result score #h rpg_el run data get entity @s Health 10
scoreboard players add #h rpg_el 40
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_el
particle minecraft:damage_indicator ~ ~1.5 ~ 0.3 0.3 0.3 0 4
