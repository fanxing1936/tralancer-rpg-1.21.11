# 身上带着圣器的人走另一条 —— 见 hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:lucifer_fight/ult/hit_holy
function rpg:inquest/seal/ability/record_magic
damage @s 10 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:poison 2 0 true
effect give @s minecraft:levitation 1 1 true
