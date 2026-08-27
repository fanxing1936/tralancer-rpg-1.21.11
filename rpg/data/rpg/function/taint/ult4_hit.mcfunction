# 身上带着圣器的人走另一条 —— 见 ult4_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult4_hit_holy
effect give @s minecraft:hunger 14 4 true
effect give @s minecraft:weakness 8 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 18 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
