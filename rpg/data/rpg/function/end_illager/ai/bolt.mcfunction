# 圣光弹（as/at 弹）：前进，碰到人就打，撞墙或飞够了就散
scoreboard players remove @s rpg_ei_life 1
execute if score @s rpg_ei_life matches ..0 run return run function rpg:end_illager/ai/bolt_pop
tp @s ^ ^ ^0.7
execute positioned ~ ~-1 ~ if entity @e[tag=rpg.unit.f,distance=..1.1] run return run function rpg:end_illager/ai/bolt_hit
execute unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:end_illager/ai/bolt_pop
particle minecraft:dust{color:[1.0,0.95,0.66],scale:1.0} ~ ~ ~ 0.05 0.05 0.05 0 2 normal
particle minecraft:end_rod ~ ~ ~ 0 0 0 0.01 1 normal
