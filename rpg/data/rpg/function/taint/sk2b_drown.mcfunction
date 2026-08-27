# 身上带着圣器的人走另一条 —— 见 sk2b_drown_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk2b_drown_holy
effect give @s minecraft:slowness 6 2 true
effect give @s minecraft:mining_fatigue 6 2 true
function rpg:inquest/seal/ability/record_drown
damage @s 4 minecraft:drown by @e[tag=rpg.dm.cast,limit=1]
