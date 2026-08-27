# 身上带着圣器的人走另一条 —— 见 ult1_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult1_hit_holy
effect give @s minecraft:levitation 2 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 18 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
