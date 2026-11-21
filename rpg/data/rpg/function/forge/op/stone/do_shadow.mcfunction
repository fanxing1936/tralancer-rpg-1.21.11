data modify storage rpg:forge g.o set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.stone
execute unless data storage rpg:forge g{o:"none"} run function rpg:forge/op/stone/refund
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.stone set value "shadow"
function rpg:forge/render
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:forge/ui/done
