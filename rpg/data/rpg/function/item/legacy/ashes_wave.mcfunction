particle minecraft:sweep_attack ~ ~ ~ 0.8 0.6 0.8 0 16 force
particle minecraft:large_smoke ~ ~ ~ 0.8 0.7 0.8 0.08 28 force
particle minecraft:squid_ink ~ ~ ~ 0.5 0.5 0.5 0.06 18 force
particle minecraft:ash ~ ~ ~ 0.8 0.65 0.8 0.05 30 force
particle minecraft:dust_color_transition{from_color:[0.35,0.42,0.12],to_color:[0.08,0.08,0.05],scale:1.7} ~ ~ ~ 0.65 0.55 0.65 0.04 22 force
execute as @e[distance=..1.8,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:wither 4 1 true
execute as @e[distance=..1.8,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 6 minecraft:magic by @a[tag=rpg.ashes.source,limit=1]
