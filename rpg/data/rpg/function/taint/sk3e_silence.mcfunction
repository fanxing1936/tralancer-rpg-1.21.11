# 身上带着圣器的人走另一条 —— 见 sk3e_silence_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk3e_silence_holy
effect give @s minecraft:darkness 6 0 true
effect give @s minecraft:mining_fatigue 8 3 true
effect give @s minecraft:wither 5 0 true
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
