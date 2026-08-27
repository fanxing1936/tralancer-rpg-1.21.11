# 身上带着圣器的人走另一条 —— 见 sk3c_maw_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk3c_maw_holy
effect give @s minecraft:wither 6 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
