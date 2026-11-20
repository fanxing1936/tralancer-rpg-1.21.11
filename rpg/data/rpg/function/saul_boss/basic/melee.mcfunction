scoreboard players add @s rpg_sl_n 1
execute facing entity @e[tag=rpg.unit.f,distance=..5,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl matches 2 run return run function rpg:saul_boss/basic/mad
execute if score @s rpg_sl_cb matches 0 run function rpg:saul_boss/skill/thrust
execute if score @s rpg_sl_cb matches 1 run function rpg:saul_boss/skill/right
execute if score @s rpg_sl_cb matches 2 run function rpg:saul_boss/skill/final
scoreboard players add @s rpg_sl_cb 1
execute if score @s rpg_sl_cb matches 3.. run scoreboard players set @s rpg_sl_cb 0
