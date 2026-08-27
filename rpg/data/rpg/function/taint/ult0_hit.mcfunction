# 身上带着圣器的人走另一条 —— 见 ult0_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult0_hit_holy
effect give @s minecraft:darkness 8 0 true
effect give @s minecraft:blindness 4 0 true
effect give @s minecraft:wither 7 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 18 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
