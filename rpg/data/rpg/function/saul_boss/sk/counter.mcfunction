execute if score @s rpg_sl_t matches 3 run function rpg:saul_boss/strike/counter
execute if score @s rpg_sl_t matches 6 run function rpg:saul_boss/strike/counter
execute if score @s rpg_sl matches 2 run execute if score @s rpg_sl_t matches 9 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl matches 2 run execute if score @s rpg_sl_t matches 12 run function rpg:saul_boss/strike/counter
execute if score @s rpg_sl_t matches 17.. run function rpg:saul_boss/sk/end
