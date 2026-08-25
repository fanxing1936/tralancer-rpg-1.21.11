# 身上带着圣器的人走另一条 —— 见 sk2e_pressure_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk2e_pressure_holy
effect give @s minecraft:slowness 6 3 true
effect give @s minecraft:mining_fatigue 6 2 true
damage @s 7 minecraft:drown by @e[tag=rpg.dm.cast,limit=1]
