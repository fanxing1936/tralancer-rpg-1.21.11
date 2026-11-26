# 眩晕：#rpg_dt_gcd 借来记多久
execute if score @s rpg_dt_t matches 1..400 run particle minecraft:crit ~ ~2.1 ~ 0.3 0.1 0.3 0.1 1
scoreboard players remove @s rpg_dt_i 1
execute if score @s rpg_dt_i matches ..0 run function rpg:daath_fight/sk/end
