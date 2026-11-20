# 影步（as/at 他）：原处散成蛛丝，到印上现身
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.40 ~1.00 ~0.00 1.000 0.000 0.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.35 ~1.00 ~0.20 0.866 0.000 0.500 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.20 ~1.00 ~0.35 0.500 0.000 0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.00 ~1.00 ~0.40 0.000 0.000 1.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.20 ~1.00 ~0.35 -0.500 0.000 0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.35 ~1.00 ~0.20 -0.866 0.000 0.500 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.40 ~1.00 ~0.00 -1.000 0.000 0.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.35 ~1.00 ~-0.20 -0.866 0.000 -0.500 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.20 ~1.00 ~-0.35 -0.500 0.000 -0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.00 ~1.00 ~-0.40 -0.000 0.000 -1.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.20 ~1.00 ~-0.35 0.500 0.000 -0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.35 ~1.00 ~-0.20 0.866 0.000 -0.500 0.25 0 force
execute as @e[tag=rpg.slb.stepto,limit=1,sort=nearest] at @s if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1,sort=nearest] ~ ~ ~
kill @e[tag=rpg.slb.stepto]
execute at @s run particle minecraft:flash{color:13193306} ~ ~1.2 ~ 0 0 0 0 1 force
execute at @s run playsound minecraft:entity.enderman.teleport hostile @a[distance=..24] ~ ~ ~ 1 0.7
