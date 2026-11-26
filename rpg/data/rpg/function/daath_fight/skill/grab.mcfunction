scoreboard players set @s rpg_dt_sk 5
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
scoreboard players set @s rpg_dt_still 0
function rpg:daath_fight/eye/shield
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/throw
playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..48] ~ ~ ~ 0.5 1.6
