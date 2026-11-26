function rpg:daath/anim/enter/bow
execute positioned ^ ^1.35 ^0.8 facing entity @a[tag=rpg.dt.me,limit=1] eyes run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.shot","rpg.dt.snew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,0.1f,1.4f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] at @s facing entity @a[tag=rpg.dt.me,limit=1] eyes run rotate @s ~ ~
scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] rpg_dt_life 34
scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] rpg_dt_pc 14
scoreboard players operation @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] rpg_dt = @s rpg_dt
tag @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] remove rpg.dt.snew
playsound rpg:daath.shot hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
