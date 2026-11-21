stopsound @a[distance=..48] record rpg:bgm.jacques1
stopsound @a[distance=..48] record rpg:bgm.jacques2
stopsound @a[distance=..48] music
execute as @e[tag=rpg.unit,distance=..48] at @s run playsound rpg:bgm.jacques2 record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_jq 5675
