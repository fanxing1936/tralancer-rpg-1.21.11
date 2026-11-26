summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 34
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:squid_ink ~ ~1.1 ~ 0.3 0.4 0.3 0.05 20
playsound rpg:daath.execute hostile @a[distance=..48] ~ ~ ~ 1.2 1.1
