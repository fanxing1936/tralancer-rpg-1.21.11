# 一招结束
scoreboard players set @s rpg_dt_sk 0
scoreboard players set @s rpg_dt_t 0
tag @s remove rpg.dt.drk
tag @s remove rpg.dt.hid
data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}
tag @a remove rpg.dt.hit
