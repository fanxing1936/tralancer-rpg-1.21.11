# 身上带着圣器的人走另一条 —— 见 sk3d_still_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk3d_still_holy
effect give @s minecraft:slowness 3 255 true
effect give @s minecraft:weakness 6 2 true
damage @s 4 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
