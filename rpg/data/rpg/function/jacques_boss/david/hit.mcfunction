# 石子命中（as/at 雅克）：打断大招，眩晕 3 秒、护甲归零
kill @e[tag=rpg.jqb.stone]
kill @e[tag=rpg.jqb.ult]
kill @e[type=minecraft:marker,tag=rpg.jqb.stake]
function rpg:jacques_boss/skill/stagger
summon minecraft:text_display ~ ~1.7 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#D8ECFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~1.7 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F2F2F2"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 10
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 3
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~1.7 ~ 0.3 0.3 0.3 0.2 30
particle minecraft:flash{color:14216447} ~ ~1.7 ~ 0 0 0 0 1 force
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[14216447]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~0.40 ~1.70 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:end_rod ~0.39 ~1.70 ~0.10 0.966 0.000 0.259 0.5 0 force
particle minecraft:end_rod ~0.35 ~1.70 ~0.20 0.866 0.000 0.500 0.5 0 force
particle minecraft:end_rod ~0.28 ~1.70 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:end_rod ~0.20 ~1.70 ~0.35 0.500 0.000 0.866 0.5 0 force
particle minecraft:end_rod ~0.10 ~1.70 ~0.39 0.259 0.000 0.966 0.5 0 force
particle minecraft:end_rod ~0.00 ~1.70 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:end_rod ~-0.10 ~1.70 ~0.39 -0.259 0.000 0.966 0.5 0 force
particle minecraft:end_rod ~-0.20 ~1.70 ~0.35 -0.500 0.000 0.866 0.5 0 force
particle minecraft:end_rod ~-0.28 ~1.70 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:end_rod ~-0.35 ~1.70 ~0.20 -0.866 0.000 0.500 0.5 0 force
particle minecraft:end_rod ~-0.39 ~1.70 ~0.10 -0.966 0.000 0.259 0.5 0 force
particle minecraft:end_rod ~-0.40 ~1.70 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:end_rod ~-0.39 ~1.70 ~-0.10 -0.966 0.000 -0.259 0.5 0 force
particle minecraft:end_rod ~-0.35 ~1.70 ~-0.20 -0.866 0.000 -0.500 0.5 0 force
particle minecraft:end_rod ~-0.28 ~1.70 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:end_rod ~-0.20 ~1.70 ~-0.35 -0.500 0.000 -0.866 0.5 0 force
particle minecraft:end_rod ~-0.10 ~1.70 ~-0.39 -0.259 0.000 -0.966 0.5 0 force
particle minecraft:end_rod ~-0.00 ~1.70 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:end_rod ~0.10 ~1.70 ~-0.39 0.259 0.000 -0.966 0.5 0 force
particle minecraft:end_rod ~0.20 ~1.70 ~-0.35 0.500 0.000 -0.866 0.5 0 force
particle minecraft:end_rod ~0.28 ~1.70 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:end_rod ~0.35 ~1.70 ~-0.20 0.866 0.000 -0.500 0.5 0 force
particle minecraft:end_rod ~0.39 ~1.70 ~-0.10 0.966 0.000 -0.259 0.5 0 force
particle minecraft:firework ~0.40 ~1.70 ~0.00 1.000 0.300 0.000 0.3 0 force
particle minecraft:firework ~0.35 ~1.70 ~0.20 0.866 0.300 0.500 0.3 0 force
particle minecraft:firework ~0.20 ~1.70 ~0.35 0.500 0.300 0.866 0.3 0 force
particle minecraft:firework ~0.00 ~1.70 ~0.40 0.000 0.300 1.000 0.3 0 force
particle minecraft:firework ~-0.20 ~1.70 ~0.35 -0.500 0.300 0.866 0.3 0 force
particle minecraft:firework ~-0.35 ~1.70 ~0.20 -0.866 0.300 0.500 0.3 0 force
particle minecraft:firework ~-0.40 ~1.70 ~0.00 -1.000 0.300 0.000 0.3 0 force
particle minecraft:firework ~-0.35 ~1.70 ~-0.20 -0.866 0.300 -0.500 0.3 0 force
particle minecraft:firework ~-0.20 ~1.70 ~-0.35 -0.500 0.300 -0.866 0.3 0 force
particle minecraft:firework ~-0.00 ~1.70 ~-0.40 -0.000 0.300 -1.000 0.3 0 force
particle minecraft:firework ~0.20 ~1.70 ~-0.35 0.500 0.300 -0.866 0.3 0 force
particle minecraft:firework ~0.35 ~1.70 ~-0.20 0.866 0.300 -0.500 0.3 0 force
playsound minecraft:block.stone.break hostile @a[distance=..40] ~ ~ ~ 1.4 0.6
playsound minecraft:item.shield.break hostile @a[distance=..40] ~ ~ ~ 1.2 0.7
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……石子？","color":"#9C9A94","bold":false,"italic":false}]
# 石子只有一颗：打断这一次之后，大卫的幽灵就消散了（之后的大招不再被打断）
execute as @e[type=minecraft:vindicator,tag=rpg.jqd] at @s run function rpg:jacques_boss/david/fade
