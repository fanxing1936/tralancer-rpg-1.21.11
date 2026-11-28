execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.folk_c.part] run rotate @s ~ 0
function rpg:town_models/town_folk_c/anim/tick
execute unless predicate rpg:town_models/town_folk_c/invisible run effect give @s minecraft:invisibility infinite 0 true
