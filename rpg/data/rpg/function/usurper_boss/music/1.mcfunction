stopsound @a[distance=..48] record minecraft:boss2
stopsound @a[distance=..48] record minecraft:boss3
execute as @e[tag=rpg.unit,distance=..48] at @s run playsound minecraft:boss2 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_ub 1876
