execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.elder.part] run rotate @s ~ 0
function rpg:town_models/town_elder/anim/tick
execute unless predicate rpg:town_models/town_elder/invisible run effect give @s minecraft:invisibility infinite 0 true
