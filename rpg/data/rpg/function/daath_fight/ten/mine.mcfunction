# 真身：站到第 #i 个的位置；只有它有白眼睛
execute if score @s rpg_dt_i matches 0 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~0.00 ~ ~-15.50
execute if score @s rpg_dt_i matches 0 run kill @e[type=minecraft:item_display,tag=rpg.dt.t0,distance=..60]
execute if score @s rpg_dt_i matches 1 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~9.11 ~ ~-12.54
execute if score @s rpg_dt_i matches 1 run kill @e[type=minecraft:item_display,tag=rpg.dt.t1,distance=..60]
execute if score @s rpg_dt_i matches 2 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~14.74 ~ ~-4.79
execute if score @s rpg_dt_i matches 2 run kill @e[type=minecraft:item_display,tag=rpg.dt.t2,distance=..60]
execute if score @s rpg_dt_i matches 3 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~14.74 ~ ~4.79
execute if score @s rpg_dt_i matches 3 run kill @e[type=minecraft:item_display,tag=rpg.dt.t3,distance=..60]
execute if score @s rpg_dt_i matches 4 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~9.11 ~ ~12.54
execute if score @s rpg_dt_i matches 4 run kill @e[type=minecraft:item_display,tag=rpg.dt.t4,distance=..60]
execute if score @s rpg_dt_i matches 5 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~0.00 ~ ~15.50
execute if score @s rpg_dt_i matches 5 run kill @e[type=minecraft:item_display,tag=rpg.dt.t5,distance=..60]
execute if score @s rpg_dt_i matches 6 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~-9.11 ~ ~12.54
execute if score @s rpg_dt_i matches 6 run kill @e[type=minecraft:item_display,tag=rpg.dt.t6,distance=..60]
execute if score @s rpg_dt_i matches 7 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~-14.74 ~ ~4.79
execute if score @s rpg_dt_i matches 7 run kill @e[type=minecraft:item_display,tag=rpg.dt.t7,distance=..60]
execute if score @s rpg_dt_i matches 8 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~-14.74 ~ ~-4.79
execute if score @s rpg_dt_i matches 8 run kill @e[type=minecraft:item_display,tag=rpg.dt.t8,distance=..60]
execute if score @s rpg_dt_i matches 9 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~-9.11 ~ ~-12.54
execute if score @s rpg_dt_i matches 9 run kill @e[type=minecraft:item_display,tag=rpg.dt.t9,distance=..60]
data merge entity @s {Invulnerable:0b}
execute at @s run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {view_range:1.5f}
tag @s remove rpg.dt.hid
tag @s add rpg.dt.seek
function rpg:daath/anim/enter/guard
