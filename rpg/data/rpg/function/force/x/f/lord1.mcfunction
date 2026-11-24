playsound minecraft:entity.phantom.flap player @a[distance=..24] ~ ~ ~ 1 1.2
playsound minecraft:item.trident.thunder player @a[distance=..32] ~ ~ ~ 0.7 1.8
function rpg:force/ray/lord1/go
summon minecraft:text_display ^ ^1.6 ^-1.8 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"#5FD68C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 19
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:text_display ^ ^1.6 ^4.5 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"#5FD68C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
