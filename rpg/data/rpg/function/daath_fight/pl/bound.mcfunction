# 场地没有墙：走出去就从对面走回来
execute unless entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..120] run return run function rpg:daath_fight/pl/strayed
execute if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23.6] run return 0
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..120,limit=1,sort=nearest] facing entity @s feet rotated ~ 0 positioned ^ ^ ^-22 run tp @s ~ ~0.1 ~
execute at @s run particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~0.3 ~ 0.6 0.2 0.6 0 16
execute at @s run playsound minecraft:block.glass.hit player @s ~ ~ ~ 0.6 0.6
execute unless entity @s[tag=rpg.dt.walk] as @e[type=minecraft:vindicator,tag=rpg.dtb,distance=..80,limit=1,sort=nearest] at @s run function rpg:daath_fight/say_walk
tag @s add rpg.dt.walk
