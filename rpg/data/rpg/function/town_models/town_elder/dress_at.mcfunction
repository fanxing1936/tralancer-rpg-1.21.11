# 重复换装或换角色时，只替换当前载体的城镇模型乘客。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.tw.model.part] run kill @s
tag @s remove rpg.tw.model.priest
tag @s remove rpg.tw.model.bard
tag @s remove rpg.tw.model.watchman
tag @s remove rpg.tw.model.witch
tag @s remove rpg.tw.model.edgewalker
tag @s remove rpg.tw.model.inquisitor
tag @s remove rpg.tw.model.folk_a
tag @s remove rpg.tw.model.folk_b
tag @s remove rpg.tw.model.folk_c
tag @s remove rpg.tw.model.child
tag @s remove rpg.tw.model.hollow_big
tag @s remove rpg.tw.model.hollow
tag @s add rpg.tw.model.elder
effect give @s minecraft:invisibility infinite 0 true
tag @e[type=minecraft:villager,tag=rpg.tw.model.dressing,distance=..1] remove rpg.tw.model.dressing
tag @s add rpg.tw.model.dressing
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/head
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/eyebrow
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/r_eyepupil
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/r_eyeiris
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/l_eyepupil
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/l_eyeiris
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/mouth
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/nose
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/hatarmorlayer
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/hatarmorside
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/arm_l
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/arm_r
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/arm_m
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/body
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/tunic
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/leg_l
execute summon minecraft:item_display run function rpg:town_models/town_elder/part/leg_r
tag @s remove rpg.tw.model.dressing
function rpg:town_models/town_elder/anim/init
function rpg:town_models/town_elder/anim/enter/idle
