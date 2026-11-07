summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.shard"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/shard_c"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.3f,1.3f,1.3f]}}
tp @e[tag=rpg.pf.new,distance=..1,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 30
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
