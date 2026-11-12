# 身上带着圣器的人走另一条 —— 见 shock_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:lucifer_fight/morph/shock_holy
function rpg:inquest/seal/ability/record_magic
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet if block ^ ^ ^-2.5 #minecraft:replaceable if block ^ ^1 ^-2.5 #minecraft:replaceable run tp @s ^ ^ ^-2.5
