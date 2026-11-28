# 一片燃烧的羽毛（at 起点，朝飞行方向）
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.feather"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/feather"}},item_display:"none",brightness:{sky:15,block:15},teleport_duration:1,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[1.2f,1.2f,1.2f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.mkb.fxnew,limit=1,predicate=!rpg:in_prologue] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
