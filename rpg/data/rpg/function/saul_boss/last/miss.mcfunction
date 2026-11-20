# 躲开了：他冲过头，整个人跪倒；4 秒护甲归零，伤害 +50%（hit/extra）
function rpg:saul/anim/enter/kneel
attribute @s minecraft:armor base set 0
tag @s add rpg.slb.weak
particle minecraft:flash{color:13193306} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.2 ~ 0.6 0.1 0.6 0 20
playsound minecraft:entity.player.attack.nodamage hostile @a[distance=..40] ~ ~ ~ 1.4 0.6
execute if score @s rpg_sl matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……好。好！看清了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl matches 2.. run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……好。好！看清了。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 16
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
