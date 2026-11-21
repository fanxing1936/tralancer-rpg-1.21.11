$damage @s $(n) rpg:forge_bonus by @a[tag=rpg.fg.atk,limit=1]
execute store result score @s damage_action run data get entity @s Health
