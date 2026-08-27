# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:hunger 7 4 true
effect give @s minecraft:weakness 4 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 18 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
