# 六翼复原（as 载体）。
execute on passengers if entity @s[tag=rpg.mkm.p.wing_lower_left] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_lower_left"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_lower_left_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_lower_left_tip"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_lower_right] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_lower_right"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_lower_right_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_lower_right_tip"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_middle_left] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_middle_left"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_middle_left_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_middle_left_tip"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_middle_right] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_middle_right"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_middle_right_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_middle_right_tip"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_upper_left] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_upper_left"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_upper_left_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_upper_left_tip"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_upper_right] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_upper_right"
execute on passengers if entity @s[tag=rpg.mkm.p.wing_upper_right_tip] run data modify entity @s item.components."minecraft:item_model" set value "rpg:michael/wing_upper_right_tip"
execute if entity @s[tag=rpg.mk.solid] run function rpg:michael/look/solid
execute if entity @s[tag=rpg.mk.fade] run function rpg:michael/look/fade
