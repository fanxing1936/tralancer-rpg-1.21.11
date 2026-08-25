# 身上带着圣器的人走另一条 —— 见 sk5d_hunt_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk5d_hunt_holy
effect give @s minecraft:glowing 6 0 true
effect give @s minecraft:poison 7 1 true
damage @s 8 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
