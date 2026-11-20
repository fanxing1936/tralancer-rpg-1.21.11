# 最后一刺（as/at 他）：身前 6 格
scoreboard players set #d rpg_sl 4
function rpg:saul_boss/line/path
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 16 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute positioned ^ ^1.35 ^0.9 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,3.0f],left_rotation:[0f,0f,0f,1f],scale:[0.12f,0.12f,6.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^1.35 ^0.9 run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 20
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ^ ^1.35 ^6.6 0.15 0.15 0.15 0.3 4
summon minecraft:text_display ^ ^1.3 ^3 {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 4
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:flash{color:15660282} ^ ^1.3 ^3 0 0 0 0 1 force
