scoreboard players set @s rpg_dt_shell 0
scoreboard players set #s rpg_dt 40
function rpg:daath_fight/stun
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4.3125f,4.3125f,4.3125f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
