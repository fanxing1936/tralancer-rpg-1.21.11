# 重复换装或换角色时，只替换当前载体的城镇模型乘客。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.part] run kill @s
tag @s remove rpg.tw.model.priest
tag @s remove rpg.tw.model.elder
tag @s remove rpg.tw.model.bard
tag @s remove rpg.tw.model.watchman
tag @s remove rpg.tw.model.witch
tag @s remove rpg.tw.model.edgewalker
tag @s remove rpg.tw.model.inquisitor
tag @s remove rpg.tw.model.folk_b
tag @s remove rpg.tw.model.folk_c
tag @s remove rpg.tw.model.child
tag @s remove rpg.tw.model.hollow_big
tag @s remove rpg.tw.model.hollow
tag @s add rpg.tw.model.folk_a
effect give @s minecraft:invisibility infinite 0 true
tag @e[type=minecraft:villager,tag=rpg.tw.model.dressing,distance=..1] remove rpg.tw.model.dressing
tag @s add rpg.tw.model.dressing
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/head
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/eyebrow
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/r_eyepupil
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/r_eyeiris
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/l_eyepupil
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/l_eyeiris
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/mouth
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/nose
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/hatarmorlayer
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/hatarmorside
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/arm_l
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/arm_r
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/arm_m
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/body
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/tunic
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/leg_l
execute summon minecraft:item_display run function rpg:town_models/town_folk_a/part/leg_r
tag @s remove rpg.tw.model.dressing
function rpg:town_models/town_folk_a/anim/init
function rpg:town_models/town_folk_a/anim/enter/idle
