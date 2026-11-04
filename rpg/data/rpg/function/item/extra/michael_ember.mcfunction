# 未引燃的圣焰 100 刻后熄灭
scoreboard players remove @s rpg_mi_ttl 1
particle dust{color:[1.0,0.2,0.0],scale:0.8} ~ ~1.2 ~ 0.25 0.35 0.25 0 1
execute if score @s rpg_mi_ttl matches ..0 run scoreboard players reset @s rpg_mi_flame
execute if score @s rpg_mi_ttl matches ..0 run tag @s remove rpg.mi.marked
