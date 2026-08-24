# 身上带着圣器的人走另一条 —— 见 sk3b_sleep_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk3b_sleep_holy
effect give @s minecraft:slowness 8 3 true
effect give @s minecraft:mining_fatigue 8 2 true
effect give @s minecraft:weakness 8 1 true
damage @s 2 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
