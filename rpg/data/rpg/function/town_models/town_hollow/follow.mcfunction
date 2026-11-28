execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.hollow.part] run rotate @s ~ 0
function rpg:town_models/town_hollow/anim/tick
execute unless score @s rpg_tw_m12_anim matches 2 run function rpg:town_models/town_hollow/attack_probe
execute unless predicate rpg:town_models/town_hollow/invisible run effect give @s minecraft:invisibility infinite 0 true
