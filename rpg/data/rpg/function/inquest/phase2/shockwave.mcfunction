tag @s add rpg.phase2.source
effect give @a[distance=..10,gamemode=!spectator,gamemode=!creative] minecraft:resistance 2 4 true
execute as @a[distance=0.25..10,gamemode=!spectator,gamemode=!creative] at @e[type=minecraft:vindicator,tag=rpg.phase2.source,limit=1] facing entity @s feet run tp @s ^ ^0.35 ^10
effect give @a[distance=..11,gamemode=!spectator,gamemode=!creative] minecraft:slow_falling 3 0 true
particle explosion_emitter ~ ~1 ~ 0 0 0 0 1 force
particle gust_emitter_large ~ ~1 ~ 0 0 0 0 1 force
particle dust{color:[1.0,0.84,0.32],scale:2.4} ~ ~0.6 ~ 5.5 0.2 5.5 0.03 130 force
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 1.2 0.62
tag @s remove rpg.phase2.source
