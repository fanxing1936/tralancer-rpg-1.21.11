execute unless entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..60] run return run function rpg:daath_fight/sk/end
execute facing entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..60,limit=1] feet rotated ~ 0 run rotate @s ~ ~
execute unless entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..1.2] at @s run execute rotated ~ 0 positioned ^ ^ ^0.3 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23] run tp @s ~ ~ ~
execute if entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..1.2] run return run function rpg:daath_fight/douse/cut
execute if score @s rpg_dt_t matches 100.. run function rpg:daath_fight/sk/end
