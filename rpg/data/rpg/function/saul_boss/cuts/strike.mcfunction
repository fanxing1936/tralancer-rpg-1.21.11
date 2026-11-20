# 斩下（as/at 斩痕）：痕上三点各 1.3 格
execute positioned ^ ^ ^-1.5 run tag @e[tag=rpg.unit.f,distance=..1.3] add rpg.slb.hit
tag @e[tag=rpg.unit.f,distance=..1.3] add rpg.slb.hit
execute positioned ^ ^ ^1.5 run tag @e[tag=rpg.unit.f,distance=..1.3] add rpg.slb.hit
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute positioned ~ ~0.08 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.4f,0.04f,4.4f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.08 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 10
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 22
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C9505A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 13
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:sweep_attack ~ ~0.6 ~ 0.6 0.1 0.6 0 2
particle minecraft:crit ~ ~0.5 ~ 0.8 0.2 0.8 0.3 8
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 0.8 1.7
