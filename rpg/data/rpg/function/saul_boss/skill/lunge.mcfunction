scoreboard players set @s rpg_sl_sk 6
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 34
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.lungewarn"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[9213602]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,5f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.02f,10f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.05 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 18
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.4 ^0.8 0.1 0.1 0.1 0 6
playsound minecraft:item.trident.riptide_1 hostile @a[distance=..24] ~ ~ ~ 0.8 1.4
