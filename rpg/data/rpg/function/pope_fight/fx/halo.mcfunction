# 光环（at 头顶）。
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.halo"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.0625f,0.0625f,1f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 60
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
