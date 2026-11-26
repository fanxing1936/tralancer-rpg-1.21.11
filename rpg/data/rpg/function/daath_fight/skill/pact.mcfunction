scoreboard players set @s rpg_dt_sk 19
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/shake
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..48] ~ ~ ~ 1 0.7
