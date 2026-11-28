schedule function rpg:pvp/sec 20t
tag @a[tag=!rpg.dm] add rpg.ch
tag @a[tag=rpg.dm] remove rpg.ch
tag @a remove rpg.safe
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c,tag=!rpg.tw.lm] at @s unless score @s rpg_tw_ev matches 1.. run tag @a[distance=..72] add rpg.safe
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.at.camp] at @s run tag @a[distance=..12] add rpg.safe
tag @a remove rpg.dm.wanted
tag @a[scores={rpg_dm_exp=1..}] add rpg.dm.wanted
