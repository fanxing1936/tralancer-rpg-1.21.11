execute unless entity @e[tag=rpg.unit.f,distance=..25] run return 0
scoreboard players remove @s rpg_sl_b 1
execute if score @s rpg_sl_b matches 1.. run return 0
execute if score @s rpg_sl matches 1 run scoreboard players set @s rpg_sl_b 10
execute if score @s rpg_sl matches 2 run scoreboard players set @s rpg_sl_b 7
execute if score @s rpg_sl_n matches 3.. run return run function rpg:saul_boss/pick
execute if entity @e[tag=rpg.unit.f,distance=..4] run return run function rpg:saul_boss/basic/melee
# 拉开了：远处不出普攻，走近；太远就直接突刺
execute unless entity @e[tag=rpg.unit.f,distance=..6] run function rpg:saul_boss/pick
