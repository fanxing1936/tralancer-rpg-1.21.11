# 第 2 段 Boss 音乐。先停掉原版配乐和上一段。
stopsound @a[distance=..48] music
stopsound @a[distance=..48] record minecraft:boss3
stopsound @a[distance=..48] record minecraft:boss2
stopsound @a[distance=..48] record minecraft:boss1
execute as @a[distance=..48] at @s run playsound minecraft:boss2 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_pf 1876
scoreboard players set #track rpg_pf 2
