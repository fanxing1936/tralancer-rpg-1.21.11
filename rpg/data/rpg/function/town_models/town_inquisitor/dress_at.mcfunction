# 重复换装或换角色时，只替换当前载体的城镇模型乘客。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.part] run kill @s
tag @s remove rpg.tw.model.priest
tag @s remove rpg.tw.model.elder
tag @s remove rpg.tw.model.bard
tag @s remove rpg.tw.model.watchman
tag @s remove rpg.tw.model.witch
tag @s remove rpg.tw.model.edgewalker
tag @s remove rpg.tw.model.folk_a
tag @s remove rpg.tw.model.folk_b
tag @s remove rpg.tw.model.folk_c
tag @s remove rpg.tw.model.child
tag @s remove rpg.tw.model.hollow_big
tag @s remove rpg.tw.model.hollow
tag @s add rpg.tw.model.inquisitor
effect give @s minecraft:invisibility infinite 0 true
tag @e[type=minecraft:vindicator,tag=rpg.tw.model.dressing,distance=..1] remove rpg.tw.model.dressing
tag @s add rpg.tw.model.dressing
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/head
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/r_leg
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/r_leg_armor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/l_leg
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/l_leg_armor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/l_arm
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/l_arm_armor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/r_arm
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/r_arm_armor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/mouth
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/l_eye_pupil
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/l_eye_iris
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/r_eye_pupil
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/r_eye_iris
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/body
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/body_armor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/armor_darkarmor_darkarmor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/armor_helmet_darkarmor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/armor_l_shoulderpad_darkarmor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/armor_r_shoulderpad_darkarmor
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_head_000
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_head_002
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_head_011
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_head_012
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_head_armor_013
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_armor_darkarmor_darkarmor_026
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_armor_darkarmor_darkarmor_027
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_armor_l_shoulderpad_darkarmor_032
execute summon minecraft:item_display run function rpg:town_models/town_inquisitor/part/town_inquisitor_armor_r_shoulderpad_darkarmor_034
tag @s remove rpg.tw.model.dressing
function rpg:town_models/town_inquisitor/anim/init
function rpg:town_models/town_inquisitor/anim/enter/idle
