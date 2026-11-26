# 眩晕（#s 刻）：夺走的东西立刻掉还
scoreboard players operation @s rpg_dt_i = #s rpg_dt
scoreboard players set @s rpg_dt_sk 20
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/stun
execute if score @s rpg_dt_sw matches 1.. run function rpg:daath_fight/steal/lose_w
execute if score @s rpg_dt_sa matches 1.. run function rpg:daath_fight/steal/lose_a
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
playsound minecraft:entity.zombie.attack_iron_door hostile @a[distance=..48] ~ ~ ~ 0.6 0.6
summon minecraft:text_display ~ ~1.20 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 31
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.60 ~1.20 ~0.00 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.42 ~1.45 ~0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.00 ~1.70 ~0.60 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.42 ~1.20 ~0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.60 ~1.45 ~0.00 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.42 ~1.70 ~-0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.00 ~1.20 ~-0.60 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.42 ~1.45 ~-0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
