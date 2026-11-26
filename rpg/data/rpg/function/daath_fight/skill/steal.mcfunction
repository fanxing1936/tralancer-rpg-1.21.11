scoreboard players set @s rpg_dt_sk 6
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
execute store result score @s rpg_dt_scd run random value 500..700
function rpg:daath_fight/eye/hand
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/cast
tag @s add rpg.dt.aim
playsound minecraft:entity.evoker.prepare_wololo hostile @a[distance=..48] ~ ~ ~ 0.8 0.7
