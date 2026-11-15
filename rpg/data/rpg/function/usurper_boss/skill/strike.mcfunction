scoreboard players set @s rpg_ub_sk 12
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 52
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:prime_enchanter/anim/enter/forward_strike
# 地上先画出冲锋线
execute positioned ~ ~0.08 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,6.5f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,0.02f,13f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew] positioned as @s rotated as @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
playsound minecraft:entity.breeze.charge hostile @a[distance=..32] ~ ~ ~ 1 0.8
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣光突进 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"让开。","color":"#9C9A94","bold":false,"italic":false}]
