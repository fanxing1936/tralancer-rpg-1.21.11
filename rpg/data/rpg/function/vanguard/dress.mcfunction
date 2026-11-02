# 别西卜麾下的罪仆换上先锋外观（as 罪仆，at 其脚下）。只加 rpg.vg 标签、隐身与部件，
# 手上的物品不换，只把它的模型设成空的。
tag @s add rpg.vg
tag @s add rpg.vg.dressing
effect give @s minecraft:invisibility infinite 0 true
item modify entity @s weapon.mainhand {function:"minecraft:set_components",components:{"minecraft:item_model":"rpg:empty"}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.body","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/body"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-1.125f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.head","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/head"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-0.15625f,0.01562f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.right_arm","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/right_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.32867f,-0.85623f,0.09365f],left_rotation:[-0.19069f,0.00666f,-0.03426f,0.98103f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.left_arm","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/left_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.34476f,-0.80796f,0.16728f],left_rotation:[-0.357f,-0.03123f,0.08137f,0.93003f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.shield","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/shield"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.46376f,-0.90173f,0.57168f],left_rotation:[0f,0.25882f,0f,0.96593f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.glaive","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/glaive"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.30225f,-1.25825f,0.41968f],left_rotation:[0.53244f,0.07714f,-0.17624f,0.82432f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.right_leg","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/right_leg"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.125f,-1.625f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.left_leg","rpg.vg.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/left_leg"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.125f,-1.625f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.vg.new,distance=..1] run ride @s mount @e[tag=rpg.vg.dressing,limit=1]
tag @e[type=minecraft:item_display,tag=rpg.vg.new,distance=..1] remove rpg.vg.new
tag @s remove rpg.vg.dressing
scoreboard players set @s rpg_vg 0
function rpg:vanguard/anim/init
# 原作：先锋现身时会嘶鸣一声
playsound rpg:vanguard.idle hostile @a[distance=..24] ~ ~ ~ 1 1
