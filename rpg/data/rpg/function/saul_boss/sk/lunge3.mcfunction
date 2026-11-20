execute if score @s rpg_sl_t matches 1 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 1 run execute positioned ~ ~0.05 ~ run function rpg:saul_boss/lunge/warn
execute if score @s rpg_sl_t matches 8..15 run function rpg:saul_boss/lunge/step
execute if score @s rpg_sl_t matches 8 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 15 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 16 run function rpg:saul_boss/strike/lunge
execute if score @s rpg_sl_t matches 21 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 21 run execute positioned ~ ~0.05 ~ run function rpg:saul_boss/lunge/warn
execute if score @s rpg_sl_t matches 28..35 run function rpg:saul_boss/lunge/step
execute if score @s rpg_sl_t matches 28 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 35 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 36 run function rpg:saul_boss/strike/lunge
execute if score @s rpg_sl_t matches 41 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 41 run execute positioned ~ ~0.05 ~ run function rpg:saul_boss/lunge/warn
execute if score @s rpg_sl_t matches 48..55 run function rpg:saul_boss/lunge/step
execute if score @s rpg_sl_t matches 48 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 55 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 56 run function rpg:saul_boss/strike/lunge
execute if score @s rpg_sl_t matches 64.. run function rpg:saul_boss/sk/end
