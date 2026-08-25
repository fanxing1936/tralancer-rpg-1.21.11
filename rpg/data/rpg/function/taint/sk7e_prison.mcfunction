# 身上带着圣器的人走另一条 —— 见 sk7e_prison_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk7e_prison_holy
effect give @s minecraft:slowness 3 255 true
effect give @s minecraft:glowing 6 0 true
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
