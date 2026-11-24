scoreboard players set @s rpg_mk_sk 20
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 232
tag @s add rpg.mkb.burnt
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:1b}
tag @s add rpg.mkb.air
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1]
function rpg:michael/anim/enter/rise
title @a[distance=..48] times 2 6 20
title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute as @e[tag=rpg.mkb.pillar] at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/core","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
execute unless score #pro rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" 𝔔𝔲𝔦𝔰 𝔲𝔱 𝔇𝔢𝔲𝔰","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"六翼燃尽 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"谁似神？","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 2 0.5
playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 2 0.4
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 24
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 21
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
