scoreboard players set @s rpg_dt_sk 9
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/mighty
playsound minecraft:entity.illusioner.prepare_mirror hostile @a[distance=..48] ~ ~ ~ 1 1.2
