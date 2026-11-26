tag @s add rpg.dt.lit
function rpg:daath/look/lit
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.875f,2.875f,2.875f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..48] ~ ~ ~ 1.2 1.4
playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..48] ~ ~ ~ 0.4 1.8
particle minecraft:flash{color:16774826} ~ ~1.2 ~ 0 0 0 0 1
