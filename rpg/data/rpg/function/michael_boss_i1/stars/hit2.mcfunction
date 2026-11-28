# 扇区 2 落下（at 中心）：扇区里的人各 8
execute rotated 330 0 positioned ^ ^ ^100 as @e[tag=rpg.unit.f,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 270 0 positioned ^ ^ ^100 if entity @s[distance=..100] run damage @s 8 minecraft:in_fire by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
