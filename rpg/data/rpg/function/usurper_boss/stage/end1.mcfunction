# 一阶段打完：变身（篡夺圣灵）。无敌、站定，约 6 秒后进入二阶段。
function rpg:usurper_boss/refill
tag @s add rpg.usb.morph
# 收掉一阶段的招式、特效和召役
scoreboard players set @s rpg_ub_sk 0
attribute @s minecraft:armor base set 8
kill @e[tag=rpg.usb.fx]
execute as @e[tag=rpg.usb.unit] run function rpg:usurper_boss/clear_unit
execute as @e[tag=rpg.unit,tag=rpg.usb.rw] run function rpg:usurper_boss/rewrite/clear
scoreboard players set @s rpg_ub_c 0
data merge entity @s {NoAI:1b,Invulnerable:1b}
function rpg:usurper/anim/enter/enchant
bossbar set rpg:usurper_boss value 1000
bossbar set rpg:usurper_boss name {"text":"\ue200\ue1f4\ue1f0\ue1f8","font":"rpg:usurper_boss"}
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"篡夺 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"把圣灵的权柄……交出来。","color":"#9C9A94","bold":false,"italic":false}]
# 致命一击被死亡保护挡下：原作不死图腾在他身前转一下再碎
execute positioned ^ ^0.6 ^1.3 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.totem"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/totem","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,12f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 18
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.8 0.4 0.4 40
playsound minecraft:item.totem.use hostile @a[distance=..48] ~ ~ ~ 1 1
