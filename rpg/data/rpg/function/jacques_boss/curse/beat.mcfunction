summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A14"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.35 ~0.20 ~0.20 0.866 0.000 0.500 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.20 ~0.20 ~0.35 0.500 0.000 0.866 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.20 ~0.20 ~0.35 -0.500 0.000 0.866 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.35 ~0.20 ~0.20 -0.866 0.000 0.500 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.35 ~0.20 ~-0.20 -0.866 0.000 -0.500 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.20 ~0.20 ~-0.35 -0.500 0.000 -0.866 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.20 ~0.20 ~-0.35 0.500 0.000 -0.866 0.18 0 force
particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.35 ~0.20 ~-0.20 0.866 0.000 -0.500 0.18 0 force
playsound minecraft:block.note_block.basedrum hostile @a[distance=..16] ~ ~ ~ 1 0.6
