# 你在哪个扇区（as 他）：扇区 j = 方位 [120j, 120j+120)
scoreboard players set #sec rpg_mk_i1 0
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.aim
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run tag @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] add rpg.mkb.aim
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 90 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 30 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec rpg_mk_i1 0
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 210 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 150 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec rpg_mk_i1 1
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 330 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] rotated 270 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec rpg_mk_i1 2
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.aim
scoreboard players operation @s rpg_mk_r = #sec rpg_mk_i1
