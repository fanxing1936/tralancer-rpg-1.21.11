# 身上带着圣器的人走另一条 —— 见 sk6d_gaze_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk6d_gaze_holy
tp @s ~ ~ ~ facing entity @e[tag=rpg.dm.cast,limit=1] eyes
effect give @s minecraft:nausea 6 0 true
effect give @s minecraft:weakness 5 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
