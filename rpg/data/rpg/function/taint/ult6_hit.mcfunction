# 身上带着圣器的人走另一条 —— 见 ult6_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult6_hit_holy
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2.5
effect give @s minecraft:slowness 7 4 true
effect give @s minecraft:weakness 7 2 true
effect give @s minecraft:nausea 8 0 true
damage @s 17 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
