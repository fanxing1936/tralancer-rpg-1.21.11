# 大卫的幽灵（as/at 它）：站在最近的玩家身后，面朝雅克
execute if score @s rpg_jq_t matches 1.. run scoreboard players remove @s rpg_jq_t 1
execute if score @s rpg_jq_t matches 1.. facing entity @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1] feet run return run tp @s ~ ~ ~ ~ 0
execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated as @e[tag=rpg.unit.f,distance=..1,sort=nearest,limit=1] rotated ~ 0 positioned ^-1.3 ^ ^-1.6 facing entity @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1] feet run tp @s ~ ~ ~ ~ 0
particle minecraft:end_rod ~ ~1.2 ~ 0.25 0.5 0.25 0.01 1
particle minecraft:dust{color:[0.85,0.93,1.0],scale:1.1} ~ ~1 ~ 0.3 0.7 0.3 0 1
