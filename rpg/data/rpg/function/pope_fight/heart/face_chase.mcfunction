# 凝视：光束慢慢转向目标，一直走动就追不上。
execute at @s positioned ^1.31 ^1.97 ^3.00 rotated ~ 0 positioned ^1000 ^ ^ if entity @a[tag=rpg.pf.tgt,limit=1,distance=..999.5] at @s run return run tp @s ~ ~ ~ ~-1.5 0
execute at @s positioned ^1.31 ^1.97 ^3.00 rotated ~ 0 positioned ^-1000 ^ ^ if entity @a[tag=rpg.pf.tgt,limit=1,distance=..999.5] at @s run tp @s ~ ~ ~ ~1.5 0
