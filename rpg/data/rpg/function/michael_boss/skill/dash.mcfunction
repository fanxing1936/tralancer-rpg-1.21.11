scoreboard players set @s rpg_mk_sk 11
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 40
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.dashwarn"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_r","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,6f],left_rotation:[0f,0f,0f,1f],scale:[1.2800000000000002f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.05 ~ run tp @e[tag=rpg.mkb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute if score @s rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"炽翼突进 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"烧尽。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk matches 2.. run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"炽翼突进 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"烧尽。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:text_display ~ ~1.7 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
