stopsound @a[distance=..48] record minecraft:boss1
stopsound @a[distance=..48] record minecraft:boss3
stopsound @a[distance=..48] music
execute as @e[tag=rpg.unit,distance=..48] at @s run playsound minecraft:boss1 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_jq 2943
