# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
function rpg:inquest/seal/ability/record_magic
damage @s 9 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:poison 4 1 true
particle sweep_attack ~ ~1 ~ 0.4 0.4 0.4 0 4
