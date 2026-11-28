stopsound @a[distance=..48] record rpg:bgm.michael1
stopsound @a[distance=..48] record rpg:bgm.michael2
stopsound @a[distance=..48] music
execute as @e[tag=rpg.unit,distance=..48] at @s run playsound rpg:bgm.michael1 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_mk_i4 1647
