# 第 3 道光束变粗：线上 1.6 格内 16
execute as @e[tag=rpg.usb.jb2] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[1.4f,1.4f,20f]}}
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^1.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^3.0 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^4.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^6.0 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^7.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^9.0 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^10.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^12.0 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^13.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^15.0 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^16.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^18.0 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^ ^19.5 run tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.usb.hit
execute as @e[tag=rpg.unit,tag=rpg.usb.hit,distance=..40] run damage @s 16 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.usb,limit=1]
tag @e[tag=rpg.unit,tag=rpg.usb.hit] remove rpg.usb.hit
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^1.5 ^6 run function rpg:usurper_boss/judge/spark
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^1.5 ^12 run function rpg:usurper_boss/judge/spark
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^1.5 ^18 run function rpg:usurper_boss/judge/spark
execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~24 0 positioned ^ ^1.5 ^1 run function rpg:usurper_boss/judge/flash
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1 1.2
playsound minecraft:block.beacon.deactivate hostile @a[distance=..40] ~ ~ ~ 0.8 1.8
