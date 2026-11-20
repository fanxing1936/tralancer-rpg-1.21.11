# 米迦勒手里拿双肋骨（as 载体）。
tag @s add rpg.mk.rib
execute on passengers if entity @s[tag=rpg.mkm.p.spine] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.mkm.p.rib] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/rib"
execute on passengers if entity @s[tag=rpg.mkm.p.rib_attack] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/rib_attack"
execute if entity @s[tag=rpg.mk.solid] run function rpg:michael/look/solid
execute if entity @s[tag=rpg.mk.fade] run function rpg:michael/look/fade
function rpg:michael/anim/enter/idle
