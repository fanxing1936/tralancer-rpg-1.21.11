execute unless data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:attribute_modifiers" run item modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents {function:"minecraft:set_attributes",replace:false,modifiers:[{attribute:"minecraft:armor",id:"rpg:forge/bonus",amount:0,operation:"add_value",slot:"armor"}]}
scoreboard players set #b rpg_fg 0
scoreboard players set #s rpg_fg 0
data modify storage rpg:forge it set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:attribute_modifiers"
function rpg:forge/base/armor_loop
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.base int 1 run scoreboard players get #b rpg_fg
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.tough int 1 run scoreboard players get #s rpg_fg
