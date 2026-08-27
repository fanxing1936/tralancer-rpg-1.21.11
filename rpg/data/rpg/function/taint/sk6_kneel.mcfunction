# 身上带着圣器的人走另一条 —— 见 sk6_kneel_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk6_kneel_holy
effect give @s minecraft:slowness 3 3 true
effect give @s minecraft:weakness 3 1 true
effect give @s minecraft:mining_fatigue 3 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 4 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
