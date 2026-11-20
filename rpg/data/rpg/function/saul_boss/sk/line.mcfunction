execute if score @s rpg_sl_t matches 10 run execute rotated ~0 0 positioned ~ ~0.05 ~ run function rpg:saul_boss/line/warn
execute if score @s rpg_sl_t matches 30 run execute rotated ~0 0 run function rpg:saul_boss/line/strike
execute if score @s rpg_sl_t matches 30 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 24 run execute rotated ~72 0 positioned ~ ~0.05 ~ run function rpg:saul_boss/line/warn
execute if score @s rpg_sl_t matches 44 run execute rotated ~72 0 run function rpg:saul_boss/line/strike
execute if score @s rpg_sl_t matches 44 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 38 run execute rotated ~144 0 positioned ~ ~0.05 ~ run function rpg:saul_boss/line/warn
execute if score @s rpg_sl_t matches 58 run execute rotated ~144 0 run function rpg:saul_boss/line/strike
execute if score @s rpg_sl_t matches 58 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 52 run execute rotated ~216 0 positioned ~ ~0.05 ~ run function rpg:saul_boss/line/warn
execute if score @s rpg_sl_t matches 72 run execute rotated ~216 0 run function rpg:saul_boss/line/strike
execute if score @s rpg_sl_t matches 72 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 66 run execute rotated ~288 0 positioned ~ ~0.05 ~ run function rpg:saul_boss/line/warn
execute if score @s rpg_sl_t matches 86 run execute rotated ~288 0 run function rpg:saul_boss/line/strike
execute if score @s rpg_sl_t matches 86 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 100 run function rpg:saul_boss/lesson/end
execute if score @s rpg_sl_t matches 140.. run function rpg:saul_boss/sk/end
