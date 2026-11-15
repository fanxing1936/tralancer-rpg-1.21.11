# 一道白金光线（as 签了新约的玩家，at 其胸前，朝向他）：只是演出，不扣权柄
scoreboard players set #d rpg_ub 0
function rpg:usurper_boss/morph/step
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.mline"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/bolt_beam","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.mline] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.mline] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d rpg_ub
execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.mline] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d rpg_ub
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 11
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~ ~0.6 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
