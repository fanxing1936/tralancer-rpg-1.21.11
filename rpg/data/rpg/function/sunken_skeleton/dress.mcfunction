# 利维坦麾下的罪仆换上沉没骷髅外观（as 罪仆，at 其脚下）。只加 rpg.sk 标签、隐身与部件，
# 手上的物品不换，只把它的模型设成空的。
tag @s add rpg.sk
tag @s add rpg.sk.dressing
effect give @s minecraft:invisibility infinite 0 true
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.body","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/body"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-0.875f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.head","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/head"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.24032f,0.03125f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.right_arm","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/right_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.3125f,-0.81651f,0.1607f],left_rotation:[-0.34202f,0f,0f,0.93969f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.left_arm","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/left_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.3125f,-0.86954f,0.05198f],left_rotation:[-0.10453f,0f,0f,0.99452f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.weapon","rpg.sk.new"],item_display:"thirdperson_righthand",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.375f,-1.02343f,0.4975f],left_rotation:[0.42262f,0f,0f,0.90631f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.right_leg","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/right_leg"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.125f,-1.625f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.left_leg","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/left_leg"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.125f,-1.625f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.sk.new,distance=..1] run ride @s mount @e[tag=rpg.sk.dressing,limit=1]
# 手里的原版物品复制到 weapon 部件上画出来，载体自己的那份只把模型设成空的
item replace entity @e[type=minecraft:item_display,tag=rpg.sk.new,tag=rpg.sk.p.weapon,distance=..1,limit=1] contents from entity @s weapon.mainhand
item modify entity @s weapon.mainhand {function:"minecraft:set_components",components:{"minecraft:item_model":"rpg:empty"}}
tag @e[type=minecraft:item_display,tag=rpg.sk.new,distance=..1] remove rpg.sk.new
tag @s remove rpg.sk.dressing
scoreboard players set @s rpg_sk 0
function rpg:sunken_skeleton/anim/init
# 原作：沉没骷髅现身时会怪笑一声
playsound rpg:sunken_skeleton.novelty hostile @a[distance=..24] ~ ~ ~ 1 1
