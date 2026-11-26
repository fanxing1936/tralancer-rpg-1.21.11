execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/end/mergefx
execute on passengers run data merge entity @s {view_range:0f}
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/arena/tree_lit
