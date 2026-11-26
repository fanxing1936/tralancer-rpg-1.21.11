# 夺走的东西 40 秒后自己还
execute if score @s rpg_dt_sw matches 1.. run scoreboard players remove @s rpg_dt_sw 1
execute if score @s rpg_dt_sw matches 1 run function rpg:daath_fight/steal/lose_w
execute if score @s rpg_dt_sa matches 1.. run scoreboard players remove @s rpg_dt_sa 1
execute if score @s rpg_dt_sa matches 1 run function rpg:daath_fight/steal/lose_a
