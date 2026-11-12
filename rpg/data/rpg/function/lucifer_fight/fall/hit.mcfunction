# 身上带着圣器的人走另一条 —— 见 hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:lucifer_fight/fall/hit_holy
function rpg:inquest/seal/ability/record_magic
damage @s 12 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:slowness 3 1 true
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet if block ^ ^ ^-3 #minecraft:replaceable if block ^ ^1 ^-3 #minecraft:replaceable run tp @s ^ ^ ^-3
