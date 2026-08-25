# 身上带着圣器的人走另一条 —— 见 sk5e_surge_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk5e_surge_holy
execute facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^-2.8
effect give @s minecraft:poison 6 1 true
damage @s 7 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
