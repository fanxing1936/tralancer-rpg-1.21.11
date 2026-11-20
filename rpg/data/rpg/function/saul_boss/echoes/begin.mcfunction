# 站回中心（as/at 他）：四个残影站到东南西北 10 格外，朝着中心
function rpg:saul/anim/enter/mighty
tag @e[tag=rpg.unit] remove rpg.slb.failed
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔯𝔰𝔥𝔞𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第三课 · 残影 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"第三课。剑没有定形——看清每一个我。","color":"#9C9A94","bold":false,"italic":false}]
execute rotated 0 0 positioned ^ ^ ^10 rotated ~180 0 run function rpg:saul_boss/echoes/one0
execute rotated 90 0 positioned ^ ^ ^10 rotated ~180 0 run function rpg:saul_boss/echoes/one1
execute rotated 180 0 positioned ^ ^ ^10 rotated ~180 0 run function rpg:saul_boss/echoes/one2
execute rotated 270 0 positioned ^ ^ ^10 rotated ~180 0 run function rpg:saul_boss/echoes/one3
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 124
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 1
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
