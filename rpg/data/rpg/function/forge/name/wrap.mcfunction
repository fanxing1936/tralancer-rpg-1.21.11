data modify storage rpg:forge nm.old set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_name"
$data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_name" set value {text:"",italic:0b,extra:[{text:"$(g)",font:"rpg:forge_src",color:"#FFFFFF",italic:0b},{text:" ",italic:0b},""]}
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_name".extra[2] set from storage rpg:forge nm.old
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.ng set value 1b
