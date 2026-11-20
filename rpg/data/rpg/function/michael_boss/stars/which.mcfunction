# 你在哪个扇区（as 他）：扇区 j = 方位 [120j, 120j+120)
scoreboard players set #sec rpg_mk 0
tag @e[tag=rpg.unit] remove rpg.mkb.aim
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run tag @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] add rpg.mkb.aim
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] rotated 90 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] rotated 30 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec rpg_mk 0
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] rotated 210 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] rotated 150 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec rpg_mk 1
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] rotated 330 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] rotated 270 0 positioned ^ ^ ^100 if entity @e[tag=rpg.unit,tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec rpg_mk 2
tag @e[tag=rpg.unit] remove rpg.mkb.aim
scoreboard players operation @s rpg_mk_r = #sec rpg_mk
