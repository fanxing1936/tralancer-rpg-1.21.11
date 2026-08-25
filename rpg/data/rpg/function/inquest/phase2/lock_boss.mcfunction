execute unless entity @s[tag=rpg.rite.locked] run attribute @s minecraft:knockback_resistance modifier remove rpg:rite_lock
execute unless entity @s[tag=rpg.rite.locked] run attribute @s minecraft:knockback_resistance modifier add rpg:rite_lock 1 add_value
tag @s add rpg.rite.locked
data merge entity @s {Motion:[0d,0d,0d],FallDistance:0f,NoAI:1b}
tag @s add rpg.rite.lock.source
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.lock.source,limit=1] rpg_rite_id at @s run tp @e[type=minecraft:vindicator,tag=rpg.rite.lock.source,limit=1] ~ ~ ~
tag @s remove rpg.rite.lock.source
