# 第 3 轮骨刺（as/at 他）
execute rotated 45.0 0 run function rpg:michael_boss/who/line
execute rotated 90.0 0 run function rpg:michael_boss/who/line
execute rotated 135.0 0 run function rpg:michael_boss/who/line
execute rotated 180.0 0 run function rpg:michael_boss/who/line
execute rotated 225.0 0 run function rpg:michael_boss/who/line
execute rotated 270.0 0 run function rpg:michael_boss/who/line
execute rotated 315.0 0 run function rpg:michael_boss/who/line
execute rotated 360.0 0 run function rpg:michael_boss/who/line
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.mkb.hit
playsound minecraft:block.bone_block.break hostile @a[distance=..48] ~ ~ ~ 2 0.5
playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
