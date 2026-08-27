# 身上带着圣器的人走另一条 —— 见 sk6b_daze_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk6b_daze_holy
effect give @s minecraft:nausea 8 0 true
effect give @s minecraft:levitation 1 0 true
function rpg:inquest/seal/ability/record_magic
damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
