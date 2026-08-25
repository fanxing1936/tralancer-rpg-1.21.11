tag @s remove rpg.rite.anchor.active
particle smoke ~ ~0.7 ~ 0.4 0.3 0.4 0.05 12 normal
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
function rpg:inquest/tool/cleanup
kill @s
