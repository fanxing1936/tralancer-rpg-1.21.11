# 飞行的肋骨（at 它）：1.4 格内 10
execute as @e[tag=rpg.unit.f,distance=..1.6] run damage @s 10 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
particle minecraft:flame ~ ~1.2 ~ 0.2 0.2 0.2 0.01 2
particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~1.2 ~ 0.2 0.2 0.2 0 1
