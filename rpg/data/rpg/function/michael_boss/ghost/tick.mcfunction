# 补放的死亡特效（as 战场中心），在最后的位置：聚光、一闪散开、余光，然后结算
scoreboard players add #ghost rpg_mk 1
execute if score #ghost rpg_mk matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1] run function rpg:michael_boss/vfx/death/halo
execute if score #ghost rpg_mk matches 4 at @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1] run function rpg:michael_boss/vfx/death/gather
execute if score #ghost rpg_mk matches 20 at @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1] run function rpg:michael_boss/vfx/death
execute if score #ghost rpg_mk matches 20 run title @a[distance=..48] times 0 3 0
execute if score #ghost rpg_mk matches 20 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score #ghost rpg_mk matches 22 run title @a[distance=..48] times 0 3 0
execute if score #ghost rpg_mk matches 22 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score #ghost rpg_mk matches 24 run title @a[distance=..48] times 0 3 0
execute if score #ghost rpg_mk matches 24 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score #ghost rpg_mk matches 26 run title @a[distance=..48] times 0 2 14
execute if score #ghost rpg_mk matches 26 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score #ghost rpg_mk matches 46 at @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1] run function rpg:michael_boss/vfx/death/after
execute if score #ghost rpg_mk matches 26..86 at @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1] run particle minecraft:end_rod ~ ~6 ~ 2.5 1.5 2.5 0 1
execute as @e[tag=rpg.mkb.fx,distance=..120] at @s run function rpg:michael_boss/fx/tick
execute if score #ghost rpg_mk matches 112.. run function rpg:michael_boss/victory
