tp @s ^ ^ ^0.508
execute at @s run particle minecraft:flame ~ ~0.45 ~ 0.05 0.25 0.05 0 1
execute if score @s rpg_mk_kd matches 1.. run function rpg:michael_boss_i2/fx/kind
