# 把你身上的增益全部抹掉 —— 他见不得你比他好。
effect clear @s minecraft:strength
effect clear @s minecraft:speed
effect clear @s minecraft:resistance
effect clear @s minecraft:regeneration
effect clear @s minecraft:absorption
effect clear @s minecraft:fire_resistance
function rpg:inquest/seal/ability/record_magic
damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:speed 6 1 true
