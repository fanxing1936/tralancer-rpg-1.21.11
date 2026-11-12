# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
function rpg:inquest/seal/ability/record_magic
damage @s 12 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:slowness 2 1 true
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet if block ^ ^ ^-3 #minecraft:replaceable if block ^ ^1 ^-3 #minecraft:replaceable run tp @s ^ ^ ^-3
