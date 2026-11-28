execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.hollow_big.part] run rotate @s ~ 0
function rpg:town_models/town_hollow_big/anim/tick
execute unless score @s rpg_tw_m11_anim matches 2 run function rpg:town_models/town_hollow_big/attack_probe
execute unless predicate rpg:town_models/town_hollow_big/invisible run effect give @s minecraft:invisibility infinite 0 true
