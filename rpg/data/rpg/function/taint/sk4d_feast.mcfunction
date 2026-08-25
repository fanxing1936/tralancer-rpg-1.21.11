# 身上带着圣器的人走另一条 —— 见 sk4d_feast_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk4d_feast_holy
effect give @s minecraft:hunger 12 4 true
effect give @s minecraft:nausea 7 0 true
effect give @s minecraft:poison 6 1 true
damage @s 4 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
