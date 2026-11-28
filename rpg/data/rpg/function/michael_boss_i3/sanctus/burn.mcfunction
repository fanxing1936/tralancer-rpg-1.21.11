$tag @s add rpg.mkb.sw$(id)
damage @s 12 minecraft:in_fire by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
particle minecraft:flame ~ ~0.5 ~ 0.3 0.3 0.3 0.05 10
