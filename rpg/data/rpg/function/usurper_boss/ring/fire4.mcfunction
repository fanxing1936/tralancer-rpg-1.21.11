# 第 5 段射出：一道原作光束从圈上射向圈心，这一扇区里的人受伤
execute positioned ~ ~1.4 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16735314]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,5.0f],left_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,10f],right_rotation:[0f,0f,0f,1f]},Rotation:[141.42857142857142f,0f]}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 11
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
execute rotated 141.4 0 positioned ^ ^ ^5.5 run function rpg:usurper_boss/ring/blast4
execute rotated 141.4 0 positioned ^ ^ ^2.5 run tag @e[tag=rpg.unit.f,distance=..2.0] add rpg.usb.hit
execute rotated 141.4 0 positioned ^ ^ ^5.5 run tag @e[tag=rpg.unit.f,distance=..2.8] add rpg.usb.hit
execute rotated 141.4 0 positioned ^ ^ ^8.5 run tag @e[tag=rpg.unit.f,distance=..3.6] add rpg.usb.hit
execute rotated 141.4 0 positioned ^ ^ ^12 run tag @e[tag=rpg.unit.f,distance=..4.6] add rpg.usb.hit
execute rotated 141.4 0 positioned ^ ^ ^17 run tag @e[tag=rpg.unit.f,distance=..6.2] add rpg.usb.hit
execute rotated 141.4 0 positioned ^ ^ ^23 run tag @e[tag=rpg.unit.f,distance=..8.2] add rpg.usb.hit
execute as @e[tag=rpg.unit,tag=rpg.usb.hit,distance=..40] run damage @s 12 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.usb,limit=1]
tag @e[tag=rpg.unit,tag=rpg.usb.hit] remove rpg.usb.hit
kill @e[tag=rpg.usb.rs4]
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 1.12
