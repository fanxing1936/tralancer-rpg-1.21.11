execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1 1.3
