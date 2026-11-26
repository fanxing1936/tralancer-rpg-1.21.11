scoreboard players set @s rpg_dt_sk 17
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
tag @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60,limit=1,sort=nearest] add rpg.dt.goal
function rpg:daath/anim/enter/walk
