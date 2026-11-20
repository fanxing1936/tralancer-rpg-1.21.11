# 甲碎（as/at 他）：火花、碎屑、白光
summon minecraft:text_display ~ ~1.55 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#D8DEE6"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 4
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:text_display ~ ~1.7 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 10
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 3
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ~0.40 ~1.80 ~0.00 1.000 0.000 0.000 0.6 0 force
particle minecraft:crit ~0.39 ~1.80 ~0.10 0.966 0.000 0.259 0.6 0 force
particle minecraft:crit ~0.35 ~1.80 ~0.20 0.866 0.000 0.500 0.6 0 force
particle minecraft:crit ~0.28 ~1.80 ~0.28 0.707 0.000 0.707 0.6 0 force
particle minecraft:crit ~0.20 ~1.80 ~0.35 0.500 0.000 0.866 0.6 0 force
particle minecraft:crit ~0.10 ~1.80 ~0.39 0.259 0.000 0.966 0.6 0 force
particle minecraft:crit ~0.00 ~1.80 ~0.40 0.000 0.000 1.000 0.6 0 force
particle minecraft:crit ~-0.10 ~1.80 ~0.39 -0.259 0.000 0.966 0.6 0 force
particle minecraft:crit ~-0.20 ~1.80 ~0.35 -0.500 0.000 0.866 0.6 0 force
particle minecraft:crit ~-0.28 ~1.80 ~0.28 -0.707 0.000 0.707 0.6 0 force
particle minecraft:crit ~-0.35 ~1.80 ~0.20 -0.866 0.000 0.500 0.6 0 force
particle minecraft:crit ~-0.39 ~1.80 ~0.10 -0.966 0.000 0.259 0.6 0 force
particle minecraft:crit ~-0.40 ~1.80 ~0.00 -1.000 0.000 0.000 0.6 0 force
particle minecraft:crit ~-0.39 ~1.80 ~-0.10 -0.966 0.000 -0.259 0.6 0 force
particle minecraft:crit ~-0.35 ~1.80 ~-0.20 -0.866 0.000 -0.500 0.6 0 force
particle minecraft:crit ~-0.28 ~1.80 ~-0.28 -0.707 0.000 -0.707 0.6 0 force
particle minecraft:crit ~-0.20 ~1.80 ~-0.35 -0.500 0.000 -0.866 0.6 0 force
particle minecraft:crit ~-0.10 ~1.80 ~-0.39 -0.259 0.000 -0.966 0.6 0 force
particle minecraft:crit ~-0.00 ~1.80 ~-0.40 -0.000 0.000 -1.000 0.6 0 force
particle minecraft:crit ~0.10 ~1.80 ~-0.39 0.259 0.000 -0.966 0.6 0 force
particle minecraft:crit ~0.20 ~1.80 ~-0.35 0.500 0.000 -0.866 0.6 0 force
particle minecraft:crit ~0.28 ~1.80 ~-0.28 0.707 0.000 -0.707 0.6 0 force
particle minecraft:crit ~0.35 ~1.80 ~-0.20 0.866 0.000 -0.500 0.6 0 force
particle minecraft:crit ~0.39 ~1.80 ~-0.10 0.966 0.000 -0.259 0.6 0 force
particle minecraft:flash{color:14212838} ~ ~2 ~ 0 0 0 0 1 force
particle minecraft:block{block_state:"minecraft:iron_block"} ~ ~2 ~ 0.5 0.5 0.5 0 30
playsound minecraft:item.shield.break hostile @a[distance=..40] ~ ~ ~ 1.4 0.7
playsound minecraft:entity.iron_golem.damage hostile @a[distance=..40] ~ ~ ~ 1.2 0.6
