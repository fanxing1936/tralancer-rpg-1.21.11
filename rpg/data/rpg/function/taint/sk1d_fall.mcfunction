# 身上带着圣器的人走另一条 —— 见 sk1d_fall_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk1d_fall_holy
effect give @s minecraft:levitation 2 1 true
effect give @s minecraft:weakness 5 1 true
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
