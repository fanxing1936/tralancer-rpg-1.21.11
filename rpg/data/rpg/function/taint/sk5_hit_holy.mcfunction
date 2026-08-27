# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:poison 5 1 true
effect give @s minecraft:wither 3 0 true
function rpg:inquest/seal/ability/record_magic
damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
