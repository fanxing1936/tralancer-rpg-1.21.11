# 每秒（rpg:explore/load 起的循环）
schedule function rpg:explore/sec 20t
execute as @a[gamemode=!spectator] at @s run function rpg:explore/each
execute in minecraft:overworld as @e[type=#rpg:elite_pool,tag=!rpg.ow.s,tag=!rpg.tw.ev] at @s run function rpg:explore/mob
