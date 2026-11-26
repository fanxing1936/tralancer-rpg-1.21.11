execute if score @s rpg_dt_t matches 1..8 run execute if score @s rpg_dt_i matches 0 run function rpg:daath_fight/dodge/0
execute if score @s rpg_dt_t matches 1..8 run execute if score @s rpg_dt_i matches 1 run function rpg:daath_fight/dodge/1
execute if score @s rpg_dt_t matches 1..8 run execute if score @s rpg_dt_i matches 2 run function rpg:daath_fight/dodge/2
particle minecraft:smoke ~ ~0.6 ~ 0.3 0.4 0.3 0.01 2
execute if score @s rpg_dt_t matches 13.. run function rpg:daath_fight/sk/end
