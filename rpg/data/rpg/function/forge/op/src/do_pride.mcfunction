data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.src set value "pride"
function rpg:forge/render
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:forge/ui/done
playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.7 1.3
