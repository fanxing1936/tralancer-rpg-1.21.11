# 印记炸开（as/at 被诅咒的人）：3 格内所有人 12
function rpg:jacques_boss/curse/clear
tag @e[tag=rpg.unit.f,distance=..3] add rpg.jqb.chit
execute as @e[tag=rpg.unit,tag=rpg.jqb.chit] run damage @s 12 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.jqb.chit
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A14"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4.25f,4.25f,4.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[9112084]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.12 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[9112084]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 12
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 18
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.40 ~0.40 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.39 ~0.40 ~0.10 0.966 0.000 0.259 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.35 ~0.40 ~0.20 0.866 0.000 0.500 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.28 ~0.40 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.20 ~0.40 ~0.35 0.500 0.000 0.866 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.10 ~0.40 ~0.39 0.259 0.000 0.966 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.00 ~0.40 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.10 ~0.40 ~0.39 -0.259 0.000 0.966 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.20 ~0.40 ~0.35 -0.500 0.000 0.866 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.28 ~0.40 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.35 ~0.40 ~0.20 -0.866 0.000 0.500 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.39 ~0.40 ~0.10 -0.966 0.000 0.259 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.40 ~0.40 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.39 ~0.40 ~-0.10 -0.966 0.000 -0.259 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.35 ~0.40 ~-0.20 -0.866 0.000 -0.500 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.28 ~0.40 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.20 ~0.40 ~-0.35 -0.500 0.000 -0.866 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.10 ~0.40 ~-0.39 -0.259 0.000 -0.966 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.00 ~0.40 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.10 ~0.40 ~-0.39 0.259 0.000 -0.966 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.20 ~0.40 ~-0.35 0.500 0.000 -0.866 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.28 ~0.40 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.35 ~0.40 ~-0.20 0.866 0.000 -0.500 0.5 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.39 ~0.40 ~-0.10 0.966 0.000 -0.259 0.5 0 force
particle minecraft:flame ~0.40 ~0.80 ~0.00 1.000 0.000 0.000 0.35 0 force
particle minecraft:flame ~0.37 ~0.80 ~0.15 0.924 0.000 0.383 0.35 0 force
particle minecraft:flame ~0.28 ~0.80 ~0.28 0.707 0.000 0.707 0.35 0 force
particle minecraft:flame ~0.15 ~0.80 ~0.37 0.383 0.000 0.924 0.35 0 force
particle minecraft:flame ~0.00 ~0.80 ~0.40 0.000 0.000 1.000 0.35 0 force
particle minecraft:flame ~-0.15 ~0.80 ~0.37 -0.383 0.000 0.924 0.35 0 force
particle minecraft:flame ~-0.28 ~0.80 ~0.28 -0.707 0.000 0.707 0.35 0 force
particle minecraft:flame ~-0.37 ~0.80 ~0.15 -0.924 0.000 0.383 0.35 0 force
particle minecraft:flame ~-0.40 ~0.80 ~0.00 -1.000 0.000 0.000 0.35 0 force
particle minecraft:flame ~-0.37 ~0.80 ~-0.15 -0.924 0.000 -0.383 0.35 0 force
particle minecraft:flame ~-0.28 ~0.80 ~-0.28 -0.707 0.000 -0.707 0.35 0 force
particle minecraft:flame ~-0.15 ~0.80 ~-0.37 -0.383 0.000 -0.924 0.35 0 force
particle minecraft:flame ~-0.00 ~0.80 ~-0.40 -0.000 0.000 -1.000 0.35 0 force
particle minecraft:flame ~0.15 ~0.80 ~-0.37 0.383 0.000 -0.924 0.35 0 force
particle minecraft:flame ~0.28 ~0.80 ~-0.28 0.707 0.000 -0.707 0.35 0 force
particle minecraft:flame ~0.37 ~0.80 ~-0.15 0.924 0.000 -0.383 0.35 0 force
particle minecraft:dust{color:[0.55,0.04,0.08],scale:2} ~ ~1 ~ 1.4 0.6 1.4 0 40
particle minecraft:flash{color:9112084} ~ ~1.2 ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~1 ~ 0.6 0.6 0.6 0.05 16
playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 1.2
