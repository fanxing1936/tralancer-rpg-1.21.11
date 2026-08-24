# 身上带着圣器的人走另一条 —— 见 sk4_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk4_hit_holy
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:hunger 8 1 true
effect give @s minecraft:slowness 2 0 true
