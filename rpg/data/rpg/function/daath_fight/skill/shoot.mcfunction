# 弓弩：弓一发满弦，弩三连；太近先退
scoreboard players set @s rpg_dt_sk 2
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if entity @a[tag=rpg.dt.me,distance=..4] run function rpg:daath_fight/shoot/back
execute if score @s rpg_dt_wc matches 8 run function rpg:daath/anim/enter/bow_draw
execute if score @s rpg_dt_wc matches 9 run function rpg:daath/anim/enter/xbow_load
execute if score @s rpg_dt_wc matches 8 run playsound minecraft:item.crossbow.loading_start hostile @a[distance=..48] ~ ~ ~ 0.8 0.8
execute if score @s rpg_dt_wc matches 9 run playsound minecraft:item.crossbow.loading_middle hostile @a[distance=..48] ~ ~ ~ 0.8 1
