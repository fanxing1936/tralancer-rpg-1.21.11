execute if score @s rpg_sl_t matches 4 run function rpg:saul/anim/enter/left
execute if score @s rpg_sl_t matches 4 run execute rotated ~-22 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 6 run function rpg:saul/anim/enter/right
execute if score @s rpg_sl_t matches 6 run execute rotated ~10 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 8 run function rpg:saul/anim/enter/double
execute if score @s rpg_sl_t matches 8 run execute rotated ~-6 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 10 run function rpg:saul/anim/enter/left
execute if score @s rpg_sl_t matches 10 run execute rotated ~24 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 12 run function rpg:saul/anim/enter/right
execute if score @s rpg_sl_t matches 12 run execute rotated ~-16 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 14 run function rpg:saul/anim/enter/double
execute if score @s rpg_sl_t matches 14 run execute rotated ~4 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 16 run function rpg:saul/anim/enter/left
execute if score @s rpg_sl_t matches 16 run execute rotated ~18 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 18 run function rpg:saul/anim/enter/right
execute if score @s rpg_sl_t matches 18 run execute rotated ~-26 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 20 run function rpg:saul/anim/enter/double
execute if score @s rpg_sl_t matches 20 run execute rotated ~0 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 22 run function rpg:saul/anim/enter/left
execute if score @s rpg_sl_t matches 22 run execute rotated ~14 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 24 run function rpg:saul/anim/enter/right
execute if score @s rpg_sl_t matches 24 run execute rotated ~-10 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 26 run function rpg:saul/anim/enter/double
execute if score @s rpg_sl_t matches 26 run execute rotated ~26 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 28 run function rpg:saul/anim/enter/left
execute if score @s rpg_sl_t matches 28 run execute rotated ~-20 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 30 run function rpg:saul/anim/enter/right
execute if score @s rpg_sl_t matches 30 run execute rotated ~8 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 32 run function rpg:saul/anim/enter/double
execute if score @s rpg_sl_t matches 32 run execute rotated ~-2 0 run function rpg:saul_boss/thrusts/stab
execute if score @s rpg_sl_t matches 2..36 run particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ^ ^1.2 ^1.5 0.6 0.4 0.6 0 2
execute if score @s rpg_sl_t matches 43.. run function rpg:saul_boss/sk/end
