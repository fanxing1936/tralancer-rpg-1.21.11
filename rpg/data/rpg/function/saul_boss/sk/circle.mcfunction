execute if score @s rpg_sl_t matches 30 run function rpg:saul_boss/circle/band0
execute if score @s rpg_sl_t matches 45 run function rpg:saul_boss/circle/band1
execute if score @s rpg_sl_t matches 60 run function rpg:saul_boss/circle/band2
execute if score @s rpg_sl_t matches 68 run function rpg:saul_boss/lesson/end
execute if score @s rpg_sl_t matches 72 run attribute @s minecraft:armor base set 0
execute if score @s rpg_sl_t matches 72 run function rpg:saul/anim/enter/stun
execute if score @s rpg_sl_t matches 72..112 run particle minecraft:end_rod ~ ~2.2 ~ 0.25 0.05 0.25 0.01 1
execute if score @s rpg_sl_t matches 112.. run function rpg:saul_boss/stagger/end
