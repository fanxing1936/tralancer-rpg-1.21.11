# 身上带着圣器的人走另一条 —— 见 hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:lucifer_fight/tempt/hit_holy
effect give @s minecraft:nausea 4 0 true
