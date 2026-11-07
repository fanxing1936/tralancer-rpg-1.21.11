# 三片平面，第一片负责判定；先是一条细线。
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.lance","rpg.pf.lancehit"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0.707107f,0f,0.707107f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,20f],scale:[25f,0.45f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.lance"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,-0.707107f,0f,0.707107f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,20f],scale:[25f,0.45f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.lance"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[-0.5f,0.5f,0.5f,0.5f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,20f],scale:[25f,0.45f,1f]}}
tp @e[tag=rpg.pf.new,distance=..1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 34
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
