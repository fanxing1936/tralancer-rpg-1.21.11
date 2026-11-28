execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.watchman.part] run rotate @s ~ 0
function rpg:town_models/town_watchman/anim/tick
execute unless predicate rpg:town_models/town_watchman/invisible run effect give @s minecraft:invisibility infinite 0 true
