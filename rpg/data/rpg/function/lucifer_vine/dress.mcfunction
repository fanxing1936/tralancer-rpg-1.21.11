# 藤蔓换装（as 根，at 根）：挂上部件，从破土的第一帧开始。
tag @s add rpg.luv
tag @s add rpg.luv.dressing
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.luv.part","rpg.luv.p.lucifer_vine_bnd_vineroot_000","rpg.luv.new_part"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_vine/lucifer_vine_bnd_vineroot_000"}},item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:2f,transformation:{translation:[0f,-4.09246f,-0.00318f],left_rotation:[0.70711f,0f,0f,0.70711f],scale:[7.19492f,7.19492f,7.19492f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.luv.part","rpg.luv.p.lucifer_vine_bnd_vine_01_001","rpg.luv.new_part"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_vine/lucifer_vine_bnd_vine_01_001"}},item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:2f,transformation:{translation:[0f,-2.85133f,-0.00422f],left_rotation:[0.70711f,0f,0f,0.70711f],scale:[7.19492f,7.19492f,7.19492f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.luv.part","rpg.luv.p.lucifer_vine_bnd_vine_02_002","rpg.luv.new_part"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_vine/lucifer_vine_bnd_vine_02_002"}},item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:2f,transformation:{translation:[0f,-1.66417f,-0.00284f],left_rotation:[0.70711f,0f,0f,0.70711f],scale:[7.19492f,7.19492f,7.19492f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.luv.new_part,distance=..1] run ride @s mount @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv.dressing,limit=1]
tag @e[type=minecraft:item_display,tag=rpg.luv.new_part,distance=..1] remove rpg.luv.new_part
tag @s remove rpg.luv.dressing
function rpg:lucifer_vine/anim/init
function rpg:lucifer_vine/anim/enter/burst
