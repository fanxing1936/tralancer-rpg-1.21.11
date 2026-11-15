tag @s add rpg.lub.shit
execute at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.05 12
function rpg:inquest/seal/ability/record_magic
damage @s 10 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
data merge entity @s {Fire:80s}
