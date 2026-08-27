# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
xp add @s -80 points
effect give @s minecraft:slowness 2 2 true
function rpg:inquest/seal/ability/record_magic
damage @s 24 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
