# 一张蛛网（at 落点）：贴地的原版蛛网，不改方块
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.web"]}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 160
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:cobweb",count:1},brightness:{sky:15,block:12},view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[2.8f,2.8f,2.8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 160
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~ ~0.3 ~ 0.8 0.1 0.8 0 16
particle minecraft:item{item:"minecraft:cobweb"} ~ ~0.4 ~ 0.5 0.2 0.5 0.05 8
