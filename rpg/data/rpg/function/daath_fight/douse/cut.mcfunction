function rpg:daath/anim/enter/ax3
summon minecraft:text_display ^ ^1.2 ^0.9 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.51f,3.51f,3.51f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 27
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
execute as @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..3] at @s run function rpg:daath_fight/douse/out
playsound minecraft:block.candle.extinguish hostile @a[distance=..48] ~ ~ ~ 1.2 0.5
function rpg:daath_fight/sk/end
scoreboard players set @s rpg_dt_gap 14
