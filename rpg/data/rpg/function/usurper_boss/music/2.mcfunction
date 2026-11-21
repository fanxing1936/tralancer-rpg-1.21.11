stopsound @a[distance=..48] record rpg:bgm.usurper1
stopsound @a[distance=..48] record rpg:bgm.usurper2
execute as @e[tag=rpg.unit,distance=..48] at @s run playsound rpg:bgm.usurper2 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_ub 1056
