# 拉回场地中心（as 他）
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1]
execute at @s run particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~ ~1 ~ 0.4 0.7 0.4 0 20
execute at @s run playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1 0.6
