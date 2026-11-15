tag @s add rpg.jqb.cursed
scoreboard players set @s rpg_jq_cu 160
playsound minecraft:entity.wither.ambient hostile @a[distance=..24] ~ ~ ~ 0.8 1.4
tellraw @s ["",{"text":"〖莫莱的诅咒〗","color":"#C04A3C","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"8 秒后在你身上炸开——离开队友。","color":"#C04A3C","bold":false,"italic":false}]
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A14"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[9112084]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 20
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~2.4 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A14"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 20
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.40 ~0.30 ~0.00 1.000 0.000 0.000 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.37 ~0.30 ~0.15 0.924 0.000 0.383 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.28 ~0.30 ~0.28 0.707 0.000 0.707 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.15 ~0.30 ~0.37 0.383 0.000 0.924 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.00 ~0.30 ~0.40 0.000 0.000 1.000 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.15 ~0.30 ~0.37 -0.383 0.000 0.924 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.28 ~0.30 ~0.28 -0.707 0.000 0.707 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.37 ~0.30 ~0.15 -0.924 0.000 0.383 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.40 ~0.30 ~0.00 -1.000 0.000 0.000 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.37 ~0.30 ~-0.15 -0.924 0.000 -0.383 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.28 ~0.30 ~-0.28 -0.707 0.000 -0.707 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.15 ~0.30 ~-0.37 -0.383 0.000 -0.924 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.00 ~0.30 ~-0.40 -0.000 0.000 -1.000 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.15 ~0.30 ~-0.37 0.383 0.000 -0.924 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.28 ~0.30 ~-0.28 0.707 0.000 -0.707 0.25 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.37 ~0.30 ~-0.15 0.924 0.000 -0.383 0.25 0 force
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.6 0.3 0.02 10
