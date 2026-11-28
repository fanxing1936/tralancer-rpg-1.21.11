# 重复换装或换角色时，只替换当前载体的城镇模型乘客。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.part] run kill @s
tag @s remove rpg.tw.model.priest
tag @s remove rpg.tw.model.elder
tag @s remove rpg.tw.model.bard
tag @s remove rpg.tw.model.watchman
tag @s remove rpg.tw.model.witch
tag @s remove rpg.tw.model.edgewalker
tag @s remove rpg.tw.model.inquisitor
tag @s remove rpg.tw.model.folk_a
tag @s remove rpg.tw.model.folk_b
tag @s remove rpg.tw.model.folk_c
tag @s remove rpg.tw.model.child
tag @s remove rpg.tw.model.hollow
tag @s add rpg.tw.model.hollow_big
effect give @s minecraft:invisibility infinite 0 true
tag @e[type=minecraft:zombie,tag=rpg.tw.model.dressing,distance=..1] remove rpg.tw.model.dressing
tag @s add rpg.tw.model.dressing
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/head
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/staff
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/l_shoulderpad
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/r_shouldpad
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/cape
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/l_arm
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/r_arm
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/body
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/l_leg
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/r_leg
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_staff_002
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_staff_007
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_staff_008
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_crown_009
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_l_arm_013
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_r_leg_020
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_body_023
execute summon minecraft:item_display run function rpg:town_models/town_hollow_big/part/town_hollow_big_staff_024
tag @s remove rpg.tw.model.dressing
function rpg:town_models/town_hollow_big/anim/init
function rpg:town_models/town_hollow_big/anim/enter/idle
