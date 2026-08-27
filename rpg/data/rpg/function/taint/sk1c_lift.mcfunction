# 身上带着圣器的人走另一条 —— 见 sk1c_lift_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk1c_lift_holy
effect give @s minecraft:levitation 3 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
