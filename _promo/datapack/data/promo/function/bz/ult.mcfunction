# 万蝇饕宴：先预警再爆发，和实战节奏一致。
execute as @e[type=minecraft:vindicator,tag=rpg.bz,limit=1,sort=nearest] at @s run function rpg:taint/ult4_warn
schedule function promo:bz/ult_fire 40t
