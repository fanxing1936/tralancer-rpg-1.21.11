# 退到 7 格外
execute at @a[tag=rpg.dt.me,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^7 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..22] run tp @s ~ ~ ~
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
