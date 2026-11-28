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
tag @s remove rpg.tw.model.hollow_big
tag @s add rpg.tw.model.hollow
effect give @s minecraft:invisibility infinite 0 true
tag @e[type=minecraft:zombie,tag=rpg.tw.model.dressing,distance=..1] remove rpg.tw.model.dressing
tag @s add rpg.tw.model.dressing
execute summon minecraft:item_display run function rpg:town_models/town_hollow/part/r_leg
execute summon minecraft:item_display run function rpg:town_models/town_hollow/part/l_leg
execute summon minecraft:item_display run function rpg:town_models/town_hollow/part/l_arm
execute summon minecraft:item_display run function rpg:town_models/town_hollow/part/r_arm
execute summon minecraft:item_display run function rpg:town_models/town_hollow/part/head
execute summon minecraft:item_display run function rpg:town_models/town_hollow/part/body
tag @s remove rpg.tw.model.dressing
function rpg:town_models/town_hollow/anim/init
function rpg:town_models/town_hollow/anim/enter/idle
