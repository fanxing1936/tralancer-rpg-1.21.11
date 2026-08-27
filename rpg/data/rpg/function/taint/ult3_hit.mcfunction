# 身上带着圣器的人走另一条 —— 见 ult3_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult3_hit_holy
effect give @s minecraft:wither 8 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 20 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
particle soul ~ ~1 ~ 0.35 0.5 0.35 0.06 24 force
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
