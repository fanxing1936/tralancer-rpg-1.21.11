# 弩口（as/at 他）：闪光与火花
summon minecraft:text_display ^ ^1.45 ^1.1 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 10
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
execute if score @s rpg_jq matches 1 run particle minecraft:electric_spark ^ ^1.45 ^1.2 0.15 0.15 0.15 0.4 10
execute if score @s rpg_jq matches 1 run particle minecraft:firework ^ ^1.45 ^1.2 0.05 0.05 0.05 0.1 6
execute if score @s rpg_jq matches 2 run particle minecraft:flame ^ ^1.45 ^1.2 0.1 0.1 0.1 0.15 14
execute if score @s rpg_jq matches 2 run particle minecraft:lava ^ ^1.45 ^1.2 0 0 0 0 2
