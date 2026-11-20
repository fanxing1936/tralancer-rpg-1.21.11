execute if score @s rpg_sl_t matches 3 run execute at @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] rotated as @e[tag=rpg.unit.ns,sort=nearest,limit=1] rotated ~ 0 positioned ^ ^ ^-2.4 run function rpg:saul_boss/step/mark
execute if score @s rpg_sl_t matches 11 run function rpg:saul_boss/step/go
execute if score @s rpg_sl_t matches 12 run execute facing entity @e[tag=rpg.unit.f,distance=..6,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 12 run function rpg:saul/anim/enter/double
execute if score @s rpg_sl_t matches 15 run function rpg:saul_boss/step/strike
execute if score @s rpg_sl_t matches 32.. run function rpg:saul_boss/sk/end
