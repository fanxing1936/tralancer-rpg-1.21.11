# 万蛇加冕：先预警再爆发，和实战节奏一致。
execute as @e[type=minecraft:vindicator,scores={rpg_dm_lord=1},limit=1,sort=nearest] at @s run function rpg:taint/ult1_warn
schedule function promo:lucifer/ult_fire 40t
