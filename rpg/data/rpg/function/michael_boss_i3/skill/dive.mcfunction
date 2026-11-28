scoreboard players set @s rpg_mk_sk 5
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 60
data merge entity @s {NoAI:1b,NoGravity:1b}
tag @s add rpg.mkb.air
function rpg:michael/anim/enter/rise
playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1.6 0.6
execute if score #w rpg_mk_i3 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i3/dive/mark
execute if score #w rpg_mk_i3 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i3/dive/mark
execute if score @s rpg_mk_i3 matches 1 run execute unless score #pro rpg_mk_i3 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"天降 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"我从高处来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_i3 matches 2.. run execute unless score #pro rpg_mk_i3 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"天降 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"我从高处来。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:text_display ~ ~1.8 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 33
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 52
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 54
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 56
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 58
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
