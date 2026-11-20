execute if score @s rpg_sl_t matches 3..9 run execute unless entity @e[tag=rpg.unit.f,distance=..1.4] if block ^ ^0.5 ^0.8 #minecraft:replaceable if block ^ ^1.5 ^0.8 #minecraft:replaceable unless block ^ ^-0.5 ^0.8 #minecraft:replaceable run tp @s ^ ^ ^0.35
execute if score @s rpg_sl_t matches 10 run function rpg:saul_boss/strike/final
execute if score @s rpg_sl_t matches 22.. run function rpg:saul_boss/sk/end
