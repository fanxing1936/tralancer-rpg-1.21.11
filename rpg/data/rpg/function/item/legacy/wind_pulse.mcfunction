particle minecraft:gust_emitter_small ~ ~1 ~ 0.45 0.55 0.45 0.08 3 force
particle minecraft:dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:1.7} ~ ~1 ~ 0.7 0.8 0.7 0.04 18 force
execute as @e[distance=..1.7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:levitation 2 1 true
execute as @e[distance=..1.7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:wind_charged 4 0 true
execute as @e[distance=..1.7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 3 minecraft:magic by @a[tag=rpg.wind.source,limit=1]
