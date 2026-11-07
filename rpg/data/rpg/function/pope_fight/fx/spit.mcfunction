# 虚空碎块（at 嘴部，rotated 为飞行方向）。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.bolt"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:heart_of_ender/shell_head"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.7f,0.7f,0.7f]}}
tp @e[tag=rpg.pf.new,distance=..1,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 30
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
particle dust{color:[0.835f,0.588f,0.949f],scale:1.0} ~ ~ ~ 0.2 0.2 0.2 0.05 8 normal
