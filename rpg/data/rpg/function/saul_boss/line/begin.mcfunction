# 站回中心之后（as/at 他）
execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:saul/anim/enter/mighty
tag @e[tag=rpg.unit] remove rpg.slb.failed
playsound minecraft:block.bell.use hostile @a[distance=..40] ~ ~ ~ 1.2 0.8
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔯𝔰𝔥𝔞𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第一课 · 直线 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"看好了，斯塔福德。剑走直线。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 100
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 1
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
