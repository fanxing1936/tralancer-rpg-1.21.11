# 身上带着圣器的人走另一条 —— 见 ult2_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult2_hit_holy
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^3
effect give @s minecraft:slowness 8 3 true
effect give @s minecraft:mining_fatigue 8 2 true
damage @s 17 minecraft:drown by @e[tag=rpg.dm.cast,limit=1]
