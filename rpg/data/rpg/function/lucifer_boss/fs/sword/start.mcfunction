scoreboard players set @s rpg_l2_st 3
scoreboard players set @s rpg_l2_t 0
scoreboard players set @s rpg_l2_sk 8
function rpg:lucifer_fight/hold
scoreboard players set @s rpg_dm_cd 30
function rpg:lucifer_p2/play/jungleabomination_summon
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"火焰的剑 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"基路伯和四面转动发火焰的剑，要把守生命树的道路。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:item.firecharge.use hostile @a[distance=..40] ~ ~ ~ 1.4 0.5
tag @e[tag=rpg.unit] remove rpg.lub.shit
summon minecraft:item_display ~ ~1.2 ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lub.sword"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16742954]}}},brightness:{sky:15,block:15},teleport_duration:1,view_range:3f,interpolation_duration:6,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,8.5f],scale:[0.05f,0.4f,11f]}}
execute as @e[tag=rpg.lu2f.pnew,tag=rpg.lub.sword] at @s rotated as @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 11
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 92
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crown_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 16
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 20
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
