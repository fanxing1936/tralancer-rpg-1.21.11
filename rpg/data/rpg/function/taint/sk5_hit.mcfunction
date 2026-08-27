# 身上带着圣器的人走另一条 —— 见 sk5_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk5_hit_holy
effect give @s minecraft:poison 10 1 true
effect give @s minecraft:wither 6 0 true
function rpg:inquest/seal/ability/record_magic
damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
