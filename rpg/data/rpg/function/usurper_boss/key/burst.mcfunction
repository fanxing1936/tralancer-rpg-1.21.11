# 爆开（as/at 载体）：圈内、安全圈外的人受伤；他跪地，护甲归零
execute as @e[type=minecraft:marker,tag=rpg.usb.safe] at @s run tag @e[tag=rpg.unit,distance=..2.5] add rpg.usb.safe
execute as @e[tag=rpg.unit.f,distance=..40,tag=!rpg.usb.safe] run damage @s 26 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.usb,limit=1]
tag @e[tag=rpg.unit] remove rpg.usb.safe
kill @e[tag=rpg.usb.keyv]
kill @e[type=minecraft:marker,tag=rpg.usb.safe]
particle minecraft:flash{color:12027094} ~ ~1 ~ 0 0 0 0 1 force
summon minecraft:item_display ~ ~0.12 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[15259135]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[32f,1f,32f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 6
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/cracks","minecraft:custom_model_data":{colors:[5975151]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 60
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~ ~2 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 5
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#B784D6"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 4
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~5.6 ~0.8 ~2.1 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~2.5 ~1.4 ~5.4 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-2.1 ~2.0 ~5.6 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-5.4 ~0.8 ~2.5 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-5.6 ~1.4 ~-2.1 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-2.5 ~2.0 ~-5.4 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~2.1 ~0.8 ~-5.6 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~5.4 ~1.4 ~-2.5 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:enchant ~ ~1 ~ 7 0.5 7 2 200 force
playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.2 0.7
playsound rpg:usurper.close hostile @a[distance=..40] ~ ~ ~ 1.4 0.6
attribute @s minecraft:armor base set 0
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……","color":"#9C9A94","bold":false,"italic":false}]
