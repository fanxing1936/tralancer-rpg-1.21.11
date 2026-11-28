execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.edgewalker.part] run rotate @s ~ 0
function rpg:town_models/town_edgewalker/anim/tick
execute unless predicate rpg:town_models/town_edgewalker/invisible run effect give @s minecraft:invisibility infinite 0 true
