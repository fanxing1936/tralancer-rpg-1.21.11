# 身上带着圣器的人走另一条 —— 见 sk5c_whisper_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/sk5c_whisper_holy
function rpg:inquest/seal/ability/record_magic
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:wither 10 2 true
