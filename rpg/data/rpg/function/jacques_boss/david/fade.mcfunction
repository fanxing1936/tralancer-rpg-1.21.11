# 大卫的幽灵消散（as/at 它）：一道天光，光点升起，然后移除
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[14216447]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#D8ECFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~0.40 ~1.00 ~0.00 1.000 0.000 0.000 0.25 0 force
particle minecraft:end_rod ~0.38 ~1.00 ~0.14 0.940 0.000 0.342 0.25 0 force
particle minecraft:end_rod ~0.31 ~1.00 ~0.26 0.766 0.000 0.643 0.25 0 force
particle minecraft:end_rod ~0.20 ~1.00 ~0.35 0.500 0.000 0.866 0.25 0 force
particle minecraft:end_rod ~0.07 ~1.00 ~0.39 0.174 0.000 0.985 0.25 0 force
particle minecraft:end_rod ~-0.07 ~1.00 ~0.39 -0.174 0.000 0.985 0.25 0 force
particle minecraft:end_rod ~-0.20 ~1.00 ~0.35 -0.500 0.000 0.866 0.25 0 force
particle minecraft:end_rod ~-0.31 ~1.00 ~0.26 -0.766 0.000 0.643 0.25 0 force
particle minecraft:end_rod ~-0.38 ~1.00 ~0.14 -0.940 0.000 0.342 0.25 0 force
particle minecraft:end_rod ~-0.40 ~1.00 ~0.00 -1.000 0.000 0.000 0.25 0 force
particle minecraft:end_rod ~-0.38 ~1.00 ~-0.14 -0.940 0.000 -0.342 0.25 0 force
particle minecraft:end_rod ~-0.31 ~1.00 ~-0.26 -0.766 0.000 -0.643 0.25 0 force
particle minecraft:end_rod ~-0.20 ~1.00 ~-0.35 -0.500 0.000 -0.866 0.25 0 force
particle minecraft:end_rod ~-0.07 ~1.00 ~-0.39 -0.174 0.000 -0.985 0.25 0 force
particle minecraft:end_rod ~0.07 ~1.00 ~-0.39 0.174 0.000 -0.985 0.25 0 force
particle minecraft:end_rod ~0.20 ~1.00 ~-0.35 0.500 0.000 -0.866 0.25 0 force
particle minecraft:end_rod ~0.31 ~1.00 ~-0.26 0.766 0.000 -0.643 0.25 0 force
particle minecraft:end_rod ~0.38 ~1.00 ~-0.14 0.940 0.000 -0.342 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.500 0.720 0.000 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 1.000 0.480 0.000 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.462 0.720 0.191 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.924 0.480 0.383 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.354 0.720 0.354 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.707 0.480 0.707 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.191 0.720 0.462 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.383 0.480 0.924 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.000 0.720 0.500 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.000 0.480 1.000 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.191 0.720 0.462 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.383 0.480 0.924 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.354 0.720 0.354 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.707 0.480 0.707 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.462 0.720 0.191 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.924 0.480 0.383 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.500 0.720 0.000 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -1.000 0.480 0.000 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.462 0.720 -0.191 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.924 0.480 -0.383 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.354 0.720 -0.354 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.707 0.480 -0.707 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.191 0.720 -0.462 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.383 0.480 -0.924 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.000 0.720 -0.500 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ -0.000 0.480 -1.000 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.191 0.720 -0.462 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.383 0.480 -0.924 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.354 0.720 -0.354 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.707 0.480 -0.707 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.462 0.720 -0.191 0.25 0 force
particle minecraft:end_rod ~ ~1.20 ~ 0.924 0.480 -0.383 0.25 0 force
particle minecraft:dust{color:[0.85,0.93,1.0],scale:1.4} ~ ~1 ~ 0.4 0.8 0.4 0 30
particle minecraft:flash{color:14216447} ~ ~1.2 ~ 0 0 0 0 1 force
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..40] ~ ~ ~ 1.2 1.4
playsound minecraft:block.beacon.deactivate hostile @a[distance=..40] ~ ~ ~ 1 1.2
tellraw @a[distance=..48] ["",{"text":"〖大卫〗","color":"#D8ECFF","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"剩下的，交给你了。","color":"#E6DFCF","bold":false,"italic":false}]
function rpg:jacques_boss/clear_unit
