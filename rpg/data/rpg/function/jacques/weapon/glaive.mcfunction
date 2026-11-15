# 只显示一把武器：glaive（as 载体）。由 add_jacques_model.py 生成。
execute on passengers if entity @s[tag=rpg.jqm.p.glaive] run data modify entity @s item.components."minecraft:item_model" set value "rpg:jacques/glaive"
execute on passengers if entity @s[tag=rpg.jqm.p.harp1] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.jqm.p.harp2] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.jqm.p.harp3] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.jqm.p.harp4] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
