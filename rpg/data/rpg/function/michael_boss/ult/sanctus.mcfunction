scoreboard players set @s rpg_mk_sk 15
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 190
data merge entity @s {NoAI:1b}
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1]
execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:michael/anim/enter/gong
execute if score @s rpg_mk matches 1 run execute unless score #pro rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℑ𝔰𝔞𝔦𝔞𝔥 6:3","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣哉三唱 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"圣哉，圣哉，圣哉。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk matches 2.. run execute unless score #pro rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℑ𝔰𝔞𝔦𝔞𝔥 6:3","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣哉三唱 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"圣哉，圣哉，圣哉。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1.6 0.8
execute at @s run summon minecraft:text_display ~ ~2.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.75f,5.75f,5.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 148
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 45
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute at @s run summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 148
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 16
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
