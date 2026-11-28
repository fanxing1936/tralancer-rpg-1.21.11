# 每秒：等故乡的人、进镇标题、安全区（rpg:town/load 起的循环）
schedule function rpg:town/sec 20t
execute as @a[tag=rpg.tw.wait] run function rpg:town/home/go
execute as @a[tag=rpg.ob] unless score @s rpg_tw_home matches 1.. run function rpg:town/home/early
execute as @a[gamemode=!spectator] at @s run function rpg:town/where
execute as @a[scores={rpg_ob=100..}] unless score @s rpg_tw_home matches 1.. run function rpg:town/home/legacy
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] at @s unless score @s rpg_tw_ev matches 1.. run function rpg:town/safe
execute in minecraft:overworld run function rpg:town/lm/wake
