execute if score @s rpg_dt_t matches 24 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/warn0
execute if score @s rpg_dt_t matches 46 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/flip0
execute if score @s rpg_dt_t matches 54 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/warn1
execute if score @s rpg_dt_t matches 76 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/flip1
execute if score @s rpg_dt_t matches 84 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/warn2
execute if score @s rpg_dt_t matches 106 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/flip2
execute if score @s rpg_dt_t matches 114 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/warn3
execute if score @s rpg_dt_t matches 136 run execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run function rpg:daath_fight/shatter/flip3
execute if score @s rpg_dt_t matches 24..140 run particle minecraft:end_rod ~ ~0.5 ~ 1.2 0.2 1.2 0.01 2
execute if score @s rpg_dt_t matches 150 run data merge entity @s {Invulnerable:0b}
execute if score @s rpg_dt_t matches 150 run function rpg:daath/anim/enter/kneel
execute if score @s rpg_dt_t matches 190.. run function rpg:daath_fight/sk/end
