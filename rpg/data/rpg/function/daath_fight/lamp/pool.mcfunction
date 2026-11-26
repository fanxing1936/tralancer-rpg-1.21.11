# 光圈（as/at 圆心）
scoreboard players remove @s rpg_dt_lt 1
execute if score @s rpg_dt_lt matches ..0 run return run function rpg:daath_fight/lamp/pool_out
particle minecraft:end_rod ~ ~1.4 ~ 2 1 2 0.005 1
