# 身上带着圣器的人走另一条 —— 见 ult7_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult7_hit_holy
xp add @s -80 points
effect give @s minecraft:slowness 5 2 true
function rpg:inquest/seal/ability/record_magic
damage @s 24 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
