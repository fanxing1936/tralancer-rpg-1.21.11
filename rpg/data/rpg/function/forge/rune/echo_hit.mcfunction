$damage @s $(n) rpg:forge_bonus by @a[tag=rpg.fg.eo,limit=1]
execute store result score @s damage_action run data get entity @s Health
particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2
playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 0.8 1.3
