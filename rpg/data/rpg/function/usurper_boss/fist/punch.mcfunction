execute facing entity @e[tag=rpg.unit.f,distance=..6,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s if block ^ ^0.5 ^0.6 #minecraft:replaceable if block ^ ^1.5 ^0.6 #minecraft:replaceable run tp @s ^ ^ ^0.6
execute at @s positioned ^ ^ ^1.6 run execute as @e[tag=rpg.unit.f,distance=..1.8] run damage @s 6 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.usb,limit=1]
execute at @s positioned ^ ^1.3 ^1.5 run function rpg:usurper_boss/fist/punch_fx
playsound minecraft:entity.player.attack.strong hostile @a[distance=..24] ~ ~ ~ 1 0.7
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..24] ~ ~ ~ 0.4 1.8
