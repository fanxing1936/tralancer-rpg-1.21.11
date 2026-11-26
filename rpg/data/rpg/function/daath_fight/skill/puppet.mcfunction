scoreboard players set @s rpg_dt_sk 14
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/gong
playsound minecraft:entity.illusioner.cast_spell hostile @a[distance=..48] ~ ~ ~ 1 0.8
