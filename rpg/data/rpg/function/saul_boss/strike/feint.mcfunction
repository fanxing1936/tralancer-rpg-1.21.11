# 刺空（as/at 他）：一刺扎进空处，踉跄
execute positioned ^ ^1.35 ^0.9 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,1.8f],left_rotation:[0f,0f,0f,1f],scale:[0.12f,0.12f,3.6f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^1.35 ^0.9 run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 20
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ^ ^1.35 ^4.2 0.15 0.15 0.15 0.3 4
particle minecraft:crit ^ ^1.2 ^2.6 0.3 0.3 0.3 0.2 6
playsound minecraft:entity.player.attack.nodamage hostile @a[distance=..24] ~ ~ ~ 1 0.7
