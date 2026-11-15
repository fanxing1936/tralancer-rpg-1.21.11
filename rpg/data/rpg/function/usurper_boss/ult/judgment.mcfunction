scoreboard players set @s rpg_ub_sk 16
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 92
# 伪圣审判（as/at 载体）
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:prime_enchanter/anim/enter/summon
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.jdir"]}
execute as @e[tag=rpg.usb.fxnew] at @s rotated as @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 100
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.03 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[12095535]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 86
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/swirl","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 86
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"伪圣审判","color":"#E6DFCF","bold":false,"italic":false},{"text":"","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1.4 0.7
