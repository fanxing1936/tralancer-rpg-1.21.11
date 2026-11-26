kill @e[type=minecraft:text_display,tag=rpg.dt.eye,distance=..6]
summon minecraft:text_display ~ ~2.75 ~ {Tags:["rpg.dt.fx","rpg.dt.eye","rpg.dt.eyenew"],text:["",{"text":"","font":"rpg:daath_marks","color":"#FFFFFF"}],background:0,billboard:"center",see_through:0b,brightness:{sky:15,block:15},teleport_duration:2,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,2.6f,2.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[type=minecraft:text_display,tag=rpg.dt.eyenew] rpg_dt_life 60
scoreboard players set @e[type=minecraft:text_display,tag=rpg.dt.eyenew] rpg_dt_kd 0
tag @e[type=minecraft:text_display,tag=rpg.dt.eyenew] remove rpg.dt.eyenew
playsound minecraft:block.sculk_sensor.clicking hostile @a[distance=..24] ~ ~ ~ 0.8 0.8
summon minecraft:text_display ~ ~2.75 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.375f,2.375f,2.375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 24
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 35
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
execute unless entity @s[tag=rpg.dt.told] run function rpg:daath_fight/eye/told
