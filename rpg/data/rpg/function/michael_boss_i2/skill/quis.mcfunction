scoreboard players set @s rpg_mk_sk 4
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 44
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:michael/anim/enter/mighty
execute positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.quiswarn"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,8f],left_rotation:[0f,0f,0f,1f],scale:[1.4400000000000002f,1f,16f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.05 ~ run tp @e[tag=rpg.mkb.fxnew,limit=1,distance=0..] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 22
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute if score @s rpg_mk_i2 matches 1 run execute unless score #pro rpg_mk_i2 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"骨刺 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"谁似神？","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_i2 matches 2.. run execute unless score #pro rpg_mk_i2 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"骨刺 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"谁似神？","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.bone_block.hit hostile @a[distance=..24] ~ ~ ~ 1 0.6
