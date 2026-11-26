scoreboard players set @s rpg_dt_sk 15
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/mighty
playsound minecraft:block.end_portal.spawn hostile @a[distance=..48] ~ ~ ~ 0.6 1.2
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..40,limit=1] run function rpg:daath_fight/seal/mark
