scoreboard players set @s rpg_jq_t 30
function rpg:david/anim/enter/throw
execute positioned ~ ~1.6 ~ run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.stone"],text:{text:"",font:"rpg:usurper_fx",color:"#D8ECFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 44
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~1.6 ~ 0.2 0.2 0.2 0.05 10
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#D8ECFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~0.40 ~1.60 ~0.00 1.000 0.000 0.000 0.15 0 force
particle minecraft:end_rod ~0.35 ~1.60 ~0.20 0.866 0.000 0.500 0.15 0 force
particle minecraft:end_rod ~0.20 ~1.60 ~0.35 0.500 0.000 0.866 0.15 0 force
particle minecraft:end_rod ~0.00 ~1.60 ~0.40 0.000 0.000 1.000 0.15 0 force
particle minecraft:end_rod ~-0.20 ~1.60 ~0.35 -0.500 0.000 0.866 0.15 0 force
particle minecraft:end_rod ~-0.35 ~1.60 ~0.20 -0.866 0.000 0.500 0.15 0 force
particle minecraft:end_rod ~-0.40 ~1.60 ~0.00 -1.000 0.000 0.000 0.15 0 force
particle minecraft:end_rod ~-0.35 ~1.60 ~-0.20 -0.866 0.000 -0.500 0.15 0 force
particle minecraft:end_rod ~-0.20 ~1.60 ~-0.35 -0.500 0.000 -0.866 0.15 0 force
particle minecraft:end_rod ~-0.00 ~1.60 ~-0.40 -0.000 0.000 -1.000 0.15 0 force
particle minecraft:end_rod ~0.20 ~1.60 ~-0.35 0.500 0.000 -0.866 0.15 0 force
particle minecraft:end_rod ~0.35 ~1.60 ~-0.20 0.866 0.000 -0.500 0.15 0 force
tellraw @a[distance=..48] ["",{"text":"〖大卫〗","color":"#D8ECFF","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……歌利亚也是这么高大。","color":"#E6DFCF","bold":false,"italic":false}]
