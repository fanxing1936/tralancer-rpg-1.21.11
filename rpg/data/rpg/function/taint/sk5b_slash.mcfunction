# 身上带着圣器的人走另一条 —— 见 sk5b_slash_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk5b_slash_holy
function rpg:inquest/seal/ability/record_magic
damage @s 9 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:poison 8 1 true
particle sweep_attack ~ ~1 ~ 0.4 0.4 0.4 0 4
