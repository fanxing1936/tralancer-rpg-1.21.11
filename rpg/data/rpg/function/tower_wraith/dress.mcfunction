# 亚巴顿麾下的罪仆换上塔中幽魂外观（as 罪仆，at 其脚下）。只加 rpg.tw 标签、隐身与部件，
# 手上的物品不换，只把它的模型设成空的。
tag @s add rpg.tw
tag @s add rpg.tw.dressing
effect give @s minecraft:invisibility infinite 0 true
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.body","rpg.tw.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/body"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-1.24531f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.head","rpg.tw.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/head"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-0.5625f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.brim","rpg.tw.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/brim"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-0.33308f,-0.55026f],left_rotation:[0.5373f,0f,0f,0.84339f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.banner","rpg.tw.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/banner"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0f,-1.48488f,-0.27937f],left_rotation:[0.06976f,0f,0f,0.99756f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.right_arm","rpg.tw.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/right_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.36552f,-1.10205f,0.22022f],left_rotation:[-0.21591f,-0.0151f,0.0681f,0.97392f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.left_arm","rpg.tw.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/left_arm"}},item_display:"none",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[0.36401f,-1.11282f,0.19521f],left_rotation:[-0.19034f,0.01331f,-0.06847f,0.97924f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.weapon","rpg.tw.new"],item_display:"thirdperson_righthand",teleport_duration:2,interpolation_duration:2,view_range:1f,transformation:{translation:[-0.42022f,-1.22929f,0.43404f],left_rotation:[0.53599f,0.03748f,0.05883f,0.84134f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.tw.new,distance=..1] run ride @s mount @e[tag=rpg.tw.dressing,limit=1]
# 手里的原版物品复制到 weapon 部件上画出来，载体自己的那份只把模型设成空的
item replace entity @e[type=minecraft:item_display,tag=rpg.tw.new,tag=rpg.tw.p.weapon,distance=..1,limit=1] contents from entity @s weapon.mainhand
item modify entity @s weapon.mainhand {function:"minecraft:set_components",components:{"minecraft:item_model":"rpg:empty"}}
tag @e[type=minecraft:item_display,tag=rpg.tw.new,distance=..1] remove rpg.tw.new
tag @s remove rpg.tw.dressing
scoreboard players set @s rpg_tw 0
function rpg:tower_wraith/anim/init
# 原作：塔中幽魂是瞬移现身的
playsound rpg:tower_wraith.appear hostile @a[distance=..24] ~ ~ ~ 1 1
