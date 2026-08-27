# 身上带着圣器的人走另一条 —— 见 sk1b_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk1b_hit_holy
function rpg:inquest/seal/ability/record_magic
damage @s 8 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:slowness 3 1 true
