# 身上带着圣器的人走另一条 —— 见 sk7d_interest_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk7d_interest_holy
xp add @s -15 points
effect give @s minecraft:weakness 6 1 true
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
