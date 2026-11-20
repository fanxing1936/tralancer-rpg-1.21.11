# 回身双斩（as/at 他）：身前 3 格
execute positioned ^ ^ ^1.6 run tag @e[tag=rpg.unit.f,distance=..2.2] add rpg.slb.hit
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 11 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute positioned ^ ^1.1 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crescent","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.slb.fxnew] positioned as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 10
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:text_display ^ ^1.3 ^1.6 {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 13
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:sweep_attack ^ ^1 ^1.8 0.8 0.2 0.8 0 3
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ^ ^1.2 ^1.8 0.6 0.3 0.6 0 8
