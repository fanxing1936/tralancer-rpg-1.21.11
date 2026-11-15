# 附魔灌注（as/at 载体）。没有罪仆在近处就改用封印。
execute unless entity @e[tag=rpg.usb.unit,distance=..20] run return run function rpg:usurper_boss/skill/seal
tag @e[tag=rpg.usb.unit,distance=..20,sort=nearest,limit=1] add rpg.usb.infused
scoreboard players set @s rpg_ub_sk 2
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 120
data merge entity @s {NoAI:1b}
function rpg:usurper/anim/enter/enchant
execute as @e[tag=rpg.usb.infused] run effect give @s minecraft:resistance 7 1 true
execute as @e[tag=rpg.usb.infused] run effect give @s minecraft:speed 7 1 true
execute as @e[tag=rpg.usb.infused] at @s run function rpg:usurper_boss/infuse/runes
# 原作附魔光束：滚动的云纹光柱，从他胸前连到罪仆，每 2 刻按距离重新拉长
summon minecraft:item_display ~ ~1.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.ibeam","rpg.usb.ifx"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[12027094]}}},brightness:{sky:15,block:15},teleport_duration:2,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 125
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.ifx"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/swirl","minecraft:custom_model_data":{colors:[12027094]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,1f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 125
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 4
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
playsound rpg:usurper.beam hostile @a[distance=..32] ~ ~ ~ 1 1
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"附魔灌注 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"把七十二柱的力，灌给我的仆从。","color":"#9C9A94","bold":false,"italic":false}]
