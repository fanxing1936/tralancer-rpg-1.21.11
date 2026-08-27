# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:hunger 6 4 true
effect give @s minecraft:nausea 3 0 true
effect give @s minecraft:poison 3 1 true
function rpg:inquest/seal/ability/record_magic
damage @s 4 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
