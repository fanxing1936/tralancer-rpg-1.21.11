# 横扫（as/at 他）：5 格内，背后那一块除外
tag @e[tag=rpg.unit.f,distance=..5] add rpg.mkb.hit
execute positioned ^ ^ ^-2.8 run tag @e[tag=rpg.unit,distance=..2.3,tag=rpg.mkb.hit] remove rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,predicate=!rpg:in_prologue] run damage @s 10 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,predicate=!rpg:in_prologue]
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.hit
summon minecraft:text_display ~ ~0.9 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"fixed",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0.70711f,0.70711f,0f],scale:[13.75f,13.75f,13.75f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.mkb.fxnew,limit=1,predicate=!rpg:in_prologue] ~ ~0.9 ~ ~ 0
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 31
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 17
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
particle minecraft:sweep_attack ~ ~1.1 ~ 2.2 0.3 2.2 0 8
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~ ~1 ~ 2.5 0.4 2.5 0 20
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 1.2 0.7
