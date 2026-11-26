scoreboard players set @s rpg_dt_sk 4
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
scoreboard players set @s rpg_dt_far 0
function rpg:daath_fight/eye/step
function rpg:daath/anim/enter/vanish
playsound rpg:daath.splinter hostile @a[distance=..48] ~ ~ ~ 1 1
