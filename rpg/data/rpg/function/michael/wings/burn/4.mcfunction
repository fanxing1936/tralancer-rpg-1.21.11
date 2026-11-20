# 六翼燃尽：烧掉第 4 片翼（wing_middle_right）。as 载体。
execute on passengers if entity @s[tag=rpg.mkm.p.wing_middle_right] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_middle_right_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
