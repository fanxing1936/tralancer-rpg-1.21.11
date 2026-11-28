tag @s add rpg.te.down
data merge entity @s {NoAI:1b,Invulnerable:1b}
execute at @s run particle minecraft:crit ~ ~1.5 ~ 0.3 0.3 0.3 0.1 12
execute if entity @s[tag=rpg.te.inq] run function rpg:town/ev/w/inq_down
