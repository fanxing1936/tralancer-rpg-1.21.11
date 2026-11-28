execute unless entity @e[tag=rpg.unit.f,distance=..25] run return 0
scoreboard players remove @s rpg_mk_b 1
execute if score @s rpg_mk_b matches 1.. run return 0
execute if score @s rpg_mk_i2 matches 1 run scoreboard players set @s rpg_mk_b 10
execute if score @s rpg_mk_i2 matches 2 run scoreboard players set @s rpg_mk_b 7
execute if score @s rpg_mk_n matches 3.. run return run function rpg:michael_boss_i2/pick
execute if score @s rpg_mk_i2 matches 1 if entity @e[tag=rpg.unit.f,distance=..5] run return run function rpg:michael_boss_i2/basic/spine
execute if score @s rpg_mk_i2 matches 2 if entity @e[tag=rpg.unit.f,distance=..3.5] run return run function rpg:michael_boss_i2/basic/rib
# 拉开了：远处不出普攻，走近；太远就直接出招
execute unless entity @e[tag=rpg.unit.f,distance=..8] run function rpg:michael_boss_i2/pick
