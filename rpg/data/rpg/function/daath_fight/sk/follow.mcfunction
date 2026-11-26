execute if score @s rpg_dt_t matches 1..9 run execute unless entity @a[tag=rpg.dt.me,distance=..1.6] at @s run execute rotated ~ 0 positioned ^ ^ ^0.62 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23] run tp @s ~ ~ ~
execute if score @s rpg_dt_t matches 1..6 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 11 run function rpg:daath/anim/enter/sw3
execute if score @s rpg_dt_t matches 14 run function rpg:daath_fight/follow/cut
execute if score @s rpg_dt_t matches 26.. run function rpg:daath_fight/sk/end
