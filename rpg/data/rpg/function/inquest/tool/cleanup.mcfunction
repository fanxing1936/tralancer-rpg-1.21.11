tag @s add rpg.rite.prop.owner
execute as @e[type=minecraft:item_display,tag=rpg.rite.prop,tag=!rpg.rite.prop.linger,distance=..18] if score @s rpg_rite_id = @e[tag=rpg.rite.prop.owner,limit=1] rpg_rite_id run kill @s
tag @s remove rpg.rite.prop.owner
