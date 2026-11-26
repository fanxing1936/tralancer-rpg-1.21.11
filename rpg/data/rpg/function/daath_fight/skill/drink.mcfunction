tag @s remove rpg.dt.want_drink
scoreboard players set @s rpg_dt_sk 7
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
tag @s add rpg.dt.drk
scoreboard players set @s rpg_dt_i 0
function rpg:daath/anim/enter/drink
