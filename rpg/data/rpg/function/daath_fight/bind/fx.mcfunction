summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 40
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 37
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.5 ~1.4 ~0.3 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 40
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 37
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:squid_ink ~ ~1 ~ 0.4 0.8 0.4 0.02 16
playsound minecraft:block.chain.break hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
