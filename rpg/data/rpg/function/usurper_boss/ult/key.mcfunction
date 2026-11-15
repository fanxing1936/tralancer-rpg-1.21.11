scoreboard players set @s rpg_ub_sk 5
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 150
# 所罗门之钥（as/at 载体）：脚下巨大的六芒星，六个角上各一个白金安全圈（光柱标出）；4 秒后爆开，之后他跪地 3 秒、护甲归零
data merge entity @s {NoAI:1b}
function rpg:usurper/anim/enter/enchant
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"所罗门之钥","color":"#E6DFCF","bold":false,"italic":false},{"text":"","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:item_display ~ ~0.02 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[5975151]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[30f,1f,30f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv","rpg.usb.keyhex"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[12027094]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[28f,1f,28f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagon","minecraft:custom_model_data":{colors:[12027094]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[30f,1f,30f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 2
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/swirl","minecraft:custom_model_data":{colors:[15259135]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:marker ~0.00 ~ ~11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.safe"]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~0.00 ~0.12 ~11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.0f,1f,5.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~0.00 ~0.15 ~11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~0.00 ~ ~11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:marker ~-9.53 ~ ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.safe"]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~-9.53 ~0.12 ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.0f,1f,5.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~-9.53 ~0.15 ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-9.53 ~ ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:marker ~-9.53 ~ ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.safe"]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~-9.53 ~0.12 ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.0f,1f,5.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~-9.53 ~0.15 ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-9.53 ~ ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:marker ~-0.00 ~ ~-11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.safe"]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~-0.00 ~0.12 ~-11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.0f,1f,5.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~-0.00 ~0.15 ~-11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~-0.00 ~ ~-11.00 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:marker ~9.53 ~ ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.safe"]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~9.53 ~0.12 ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.0f,1f,5.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~9.53 ~0.15 ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~9.53 ~ ~-5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:marker ~9.53 ~ ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.safe"]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~9.53 ~0.12 ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.0f,1f,5.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~9.53 ~0.15 ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.keyv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~9.53 ~ ~5.50 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
playsound minecraft:block.end_portal.spawn hostile @a[distance=..40] ~ ~ ~ 0.8 1.4
playsound rpg:usurper.prepare hostile @a[distance=..40] ~ ~ ~ 1.2 0.7
