scoreboard players set @s rpg_mk_sk 16
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 212
data merge entity @s {NoAI:1b,NoGravity:1b}
tag @s add rpg.mkb.air
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..]
function rpg:michael/anim/enter/rise
execute if score @s rpg_mk_i1 matches 1 run execute unless score #pro rpg_mk_i1 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℜ𝔢𝔳𝔢𝔩𝔞𝔱𝔦𝔬𝔫 11:15","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第七号角 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"第七位天使吹号。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_i1 matches 2.. run execute unless score #pro rpg_mk_i1 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℜ𝔢𝔳𝔢𝔩𝔞𝔱𝔦𝔬𝔫 11:15","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第七号角 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"第七位天使吹号。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.6
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run summon minecraft:item_display ~ ~9 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_trumpet","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[14f,1f,14f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 170
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 16
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run summon minecraft:text_display ~ ~7.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.5f,5.5f,5.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 170
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 45
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
