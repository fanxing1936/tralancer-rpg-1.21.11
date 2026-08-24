# 身上带着圣器的人走另一条 —— 见 sk_none_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk_none_hit_holy
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:blindness 3 0 true
