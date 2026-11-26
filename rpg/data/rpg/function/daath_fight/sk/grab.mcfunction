execute if score @s rpg_dt_t matches 1..12 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 6..14 run execute unless entity @a[tag=rpg.dt.me,distance=..1.5] at @s run execute rotated ~ 0 positioned ^ ^ ^0.6 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23] run tp @s ~ ~ ~
execute if score @s rpg_dt_t matches 16 run function rpg:daath_fight/grab/take
execute if score @s rpg_dt_t matches 34.. run function rpg:daath_fight/sk/end
