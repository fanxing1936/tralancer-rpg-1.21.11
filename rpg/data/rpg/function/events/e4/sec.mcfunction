execute as @e[tag=rpg.ev.gob] at @s run particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0 3
execute unless entity @e[tag=rpg.ev.gob] run function rpg:events/end
