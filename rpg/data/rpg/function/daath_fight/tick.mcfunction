# 每刻入口（add_daath.py）
execute as @a[scores={rpg_dt_cd=1..}] run scoreboard players remove @s rpg_dt_cd 1
execute as @a[scores={rpg_dt=1..}] at @s run function rpg:daath_fight/pl/tick
execute in rpg:daath if entity @a[distance=0..] run function rpg:daath_fight/dim
