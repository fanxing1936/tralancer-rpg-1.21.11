# 传送出去（as/at 它）
scoreboard players set @s rpg_mk_ws 1
scoreboard players set @s rpg_mk_wt 0
function rpg:watchling/anim/enter/tp_out
particle minecraft:reverse_portal ~ ~1.4 ~ 0.4 0.9 0.4 0.05 20
