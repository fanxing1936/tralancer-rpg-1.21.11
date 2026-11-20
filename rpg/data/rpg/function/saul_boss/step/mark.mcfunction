# 落点（at 你身后 2.4 格）：一个暗红的印
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.stepto"]}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 14
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.4f,1f,2.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 15
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~ ~1 ~ 0.3 0.6 0.3 0 10
playsound minecraft:block.note_block.basedrum hostile @a[distance=..24] ~ ~ ~ 1 0.6
