# 剑痕斩开（as 他）：每一节 1.4 格内的人都挨一下
execute as @e[tag=rpg.slb.flashseg] at @s run tag @e[tag=rpg.unit.f,distance=..1.4] add rpg.slb.hit
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute as @e[tag=rpg.slb.flashseg] at @s run function rpg:saul_boss/flash/burst
kill @e[tag=rpg.slb.flashseg]
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.4 1.8
playsound minecraft:block.glass.break hostile @a[distance=..40] ~ ~ ~ 1 1.6
