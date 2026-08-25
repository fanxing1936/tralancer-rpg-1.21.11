# 身上带着圣器的人走另一条 —— 见 sk1e_reject_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk1e_reject_holy
execute facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^-3
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:slowness 4 1 true
