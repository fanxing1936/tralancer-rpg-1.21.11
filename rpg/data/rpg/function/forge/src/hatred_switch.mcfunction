damage @s 1 rpg:forge_bonus
execute store result score @s damage_action run data get entity @s Health
particle minecraft:damage_indicator ~ ~1.2 ~ 0.2 0.2 0.2 0 2
