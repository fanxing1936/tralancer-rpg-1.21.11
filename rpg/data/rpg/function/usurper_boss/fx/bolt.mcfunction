# 书页弹：每刻前进，碰到人就打，撞墙就散；每 3 刻在身后留一颗星芒
tp @s ^ ^ ^0.9
execute positioned ~ ~-1 ~ if entity @e[tag=rpg.unit.f,distance=..1.2] run return run function rpg:usurper_boss/fx/bolt_hit
execute unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:usurper_boss/fx/bolt_pop
scoreboard players operation #m rpg_ub = @s rpg_ub_life
scoreboard players set #k rpg_ub 3
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 positioned ^ ^ ^-0.6 run function rpg:usurper_boss/fx/bolt_trail
particle minecraft:enchant ~ ~ ~ 0.1 0.1 0.1 0.6 2
