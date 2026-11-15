# 被灌注的罪仆先倒下：光束断开，他硬直 2 秒
kill @e[tag=rpg.usb.ifx]
scoreboard players set @s rpg_ub_sk 9
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 40
data merge entity @s {NoAI:1b}
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 5
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[12027094]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 6
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:enchant ~ ~1.5 ~ 0.5 0.8 0.5 2 40
playsound minecraft:block.glass.break hostile @a[distance=..24] ~ ~ ~ 1 0.6
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……断了？","color":"#9C9A94","bold":false,"italic":false}]
