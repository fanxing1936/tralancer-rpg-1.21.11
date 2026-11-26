# 全灭（at 场地中心附近）
execute as @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..60,scores={rpg_dt_lt=1..}] at @s run function rpg:daath_fight/lamp/out
execute as @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60] at @s run function rpg:daath_fight/lamp/pool_out
