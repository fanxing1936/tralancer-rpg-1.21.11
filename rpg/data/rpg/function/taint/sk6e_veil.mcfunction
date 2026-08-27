# 身上带着圣器的人走另一条 —— 见 sk6e_veil_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk6e_veil_holy
effect give @s minecraft:darkness 6 0 true
effect give @s minecraft:slowness 6 2 true
effect give @s minecraft:glowing 6 0 true
function rpg:inquest/seal/ability/record_magic
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
