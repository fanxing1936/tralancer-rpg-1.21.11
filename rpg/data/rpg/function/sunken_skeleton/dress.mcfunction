# 利维坦麾下的罪仆换上沉没骷髅外观（as 罪仆，at 其脚下）。只加 rpg.sk 标签、隐身与部件，
# 手上的物品不换，只把它的模型设成空的。
tag @s add rpg.sk
tag @s add rpg.sk.dressing
effect give @s minecraft:invisibility infinite 0 true
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.r_leg","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/r_leg"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.1826f,-1.58717f,-0.16194f],left_rotation:[-0.60778f,-0.10644f,-0.20413f,0.76001f],scale:[8.75214f,8.75214f,8.75214f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.l_leg","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/l_leg"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.11934f,-1.60615f,0.05472f],left_rotation:[0.69083f,-0.15083f,0.15083f,0.69083f],scale:[8.75214f,8.75214f,8.75214f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.l_arm","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/l_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.30956f,-0.8118f,0.18273f],left_rotation:[0.6421f,-0.138f,0.18503f,0.73105f],scale:[8.75214f,8.75214f,8.75214f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.r_arm","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/r_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.2975f,-0.80743f,-0.20669f],left_rotation:[-0.60378f,-0.19517f,-0.24512f,0.73299f],scale:[8.75214f,8.75214f,8.75214f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.body","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/body"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.02983f,-0.8841f,-0.01368f],left_rotation:[0.69083f,-0.15083f,0.15083f,0.69083f],scale:[8.75214f,8.75214f,8.75214f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.sunken_skeleton_head_004","rpg.sk.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/sunken_skeleton_head_004"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.12357f,0.06769f,-0.07921f],left_rotation:[0.70611f,0.0376f,-0.0376f,0.70611f],scale:[8.75214f,8.75214f,8.75214f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.weapon","rpg.sk.new"],item_display:"thirdperson_righthand",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.32244f,-1.12625f,-0.28505f],left_rotation:[0.70711f,0f,0f,0.70711f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
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
