# 一枚圣光弹（at 枪口，rotated 为飞行方向）。
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.blast"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.8333f,1.8333f,1f]}}
tp @e[tag=rpg.pf.new,distance=..1,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 36
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
