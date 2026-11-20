# 六翼燃尽：烧掉第 2 片翼（wing_lower_right）。as 载体。
execute on passengers if entity @s[tag=rpg.mkm.p.wing_lower_right] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_lower_right_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
