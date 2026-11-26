# 灯下打中它：四下还一件
execute if score @s rpg_dt_sw matches ..0 if score @s rpg_dt_sa matches ..0 run return 0
scoreboard players add @s rpg_dt_sp 1
particle minecraft:crit ~ ~1.3 ~ 0.3 0.3 0.3 0.3 8
execute if score @s rpg_dt_sp matches 4.. if score @s rpg_dt_sw matches 1.. run return run function rpg:daath_fight/steal/lose_w
execute if score @s rpg_dt_sp matches 4.. if score @s rpg_dt_sa matches 1.. run function rpg:daath_fight/steal/lose_a
