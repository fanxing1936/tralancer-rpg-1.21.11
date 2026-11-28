# 收场时守望者散去（as 它）
execute at @s run particle minecraft:ash ~ ~1.5 ~ 0.4 1 0.4 0 40
execute at @s run summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 36
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute at @s run particle minecraft:flame ~ ~2.4 ~ 0.3 0.3 0.3 0.02 8
function rpg:michael_boss_i3/clear_unit
