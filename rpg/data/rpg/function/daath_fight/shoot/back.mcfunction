function rpg:daath/anim/enter/roll_b
execute positioned ^ ^ ^-5 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23] run tp @s ~ ~ ~
playsound minecraft:entity.player.attack.nodamage hostile @a[distance=..48] ~ ~ ~ 0.8 0.8
