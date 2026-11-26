scoreboard players set @s rpg_dt_sk 11
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/shake
scoreboard players set @s rpg_dt_blade 160
playsound minecraft:item.firecharge.use hostile @a[distance=..48] ~ ~ ~ 1 0.6
