scoreboard players set #folkt rpg_tl 0
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c,tag=!rpg.tw.lm] at @s if entity @a[distance=..160] run function rpg:town/life/folk_check
