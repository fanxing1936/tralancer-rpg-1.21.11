# 六翼燃尽：烧掉第 5 片翼（wing_upper_left）。as 载体。
execute on passengers if entity @s[tag=rpg.mkm.p.wing_upper_left] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_upper_left_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
