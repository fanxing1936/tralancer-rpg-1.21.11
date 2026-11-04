# 亚巴顿换装（as 降临者，at 其脚下）。只加 rpg.ab 标签与六个部件，不碰其他标签与数值。
tag @s add rpg.ab
tag @s add rpg.ab.dressing
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.body","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/body"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0f,-1.12344f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.head","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/head"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0.01215f,-0.12742f,0.00086f],left_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.right_arm","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/right_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[-0.39827f,-0.96841f,0.12507f],left_rotation:[-0.10433f,0.00638f,-0.06071f,0.99267f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.right_fist","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/right_fist"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[-0.47818f,-1.61918f,0.26444f],left_rotation:[-0.03084f,0.70643f,-0.11671f,0.69741f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.left_arm","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/left_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0.39897f,-0.9741f,0.09411f],left_rotation:[-0.07831f,-0.00479f,0.06086f,0.99506f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.left_fist","rpg.ab.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/left_fist"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:{translation:[0.47966f,-1.63123f,0.19897f],left_rotation:[-0.09841f,0.70023f,-0.01234f,0.707f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.ab.new,distance=..1] run ride @s mount @e[type=minecraft:vindicator,tag=rpg.ab.dressing,limit=1]
tag @e[type=minecraft:item_display,tag=rpg.ab.new,distance=..1] remove rpg.ab.new
tag @s remove rpg.ab.dressing
function rpg:abaddon/anim/init
playsound rpg:abaddon.intro_foley hostile @a[distance=..32] ~ ~ ~ 1.2 1
playsound rpg:abaddon.intro hostile @a[distance=..48] ~ ~ ~ 1.2 1
function rpg:abaddon/anim/enter/spread
