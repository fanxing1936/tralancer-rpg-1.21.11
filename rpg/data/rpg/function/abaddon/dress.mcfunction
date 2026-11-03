# 亚巴顿换装（as 降临者，at 其脚下）。只加 rpg.ab 标签与六个部件，不碰其他标签与数值。
tag @s add rpg.ab
tag @s add rpg.ab.dressing
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.body","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/body"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0f,-0.81406f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.head","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/head"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0.01215f,0.18195f,0.00086f],left_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.right_arm","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/right_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[-0.37033f,-0.8571f,0.08954f],left_rotation:[-0.08713f,0.00228f,-0.02608f,0.99585f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.right_fist","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/right_fist"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[-0.41108f,-1.63464f,0.22683f],left_rotation:[-0.76578f,0.02005f,-0.01683f,0.64257f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.left_arm","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/left_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0.37053f,-0.86108f,0.06284f],left_rotation:[-0.06103f,-0.0016f,0.02613f,0.99779f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.left_fist","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/left_fist"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0.4116f,-1.64474f,0.15919f],left_rotation:[-0.7487f,-0.01961f,0.01735f,0.66239f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.ab.new,distance=..1] run ride @s mount @e[type=minecraft:vindicator,tag=rpg.ab.dressing,limit=1]
tag @e[type=minecraft:item_display,tag=rpg.ab.new,distance=..1] remove rpg.ab.new
tag @s remove rpg.ab.dressing
function rpg:abaddon/anim/init
playsound rpg:abaddon.intro_foley hostile @a[distance=..32] ~ ~ ~ 1.2 1
playsound rpg:abaddon.intro hostile @a[distance=..48] ~ ~ ~ 1.2 1
function rpg:abaddon/anim/enter/spread
