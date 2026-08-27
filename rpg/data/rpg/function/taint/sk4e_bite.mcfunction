# 身上带着圣器的人走另一条 —— 见 sk4e_bite_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk4e_bite_holy
effect give @s minecraft:hunger 10 3 true
function rpg:inquest/seal/ability/record_magic
damage @s 11 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 1 true
