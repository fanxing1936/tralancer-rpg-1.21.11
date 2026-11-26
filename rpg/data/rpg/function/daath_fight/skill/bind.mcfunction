scoreboard players set @s rpg_dt_sk 12
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/cast
playsound minecraft:block.chain.place hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/bind/mark
