# 出手前：盯着你、贴上来
execute if score @s rpg_dt_t matches 1.. run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute unless entity @a[tag=rpg.dt.me,distance=..2.1] at @s run execute rotated ~ 0 positioned ^ ^ ^0.36 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23] run tp @s ~ ~ ~
