# 拉回场地中心（as 他）
tp @s @e[type=minecraft:marker,tag=rpg.slb.center,limit=1]
execute at @s run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.4 0.7 0.4 0 20
execute at @s run playsound minecraft:entity.enderman.teleport hostile @a[distance=..32] ~ ~ ~ 1 0.6
