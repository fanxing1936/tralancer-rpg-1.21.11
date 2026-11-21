stopsound @a[distance=..48] record rpg:bgm.saul1
stopsound @a[distance=..48] record rpg:bgm.saul2
stopsound @a[distance=..48] music
execute as @e[tag=rpg.unit,distance=..48] at @s run playsound rpg:bgm.saul2 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_sl 2241
