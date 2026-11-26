# 站在亮着的灯下就没事
execute as @a[tag=rpg.dt.me,limit=1] at @s unless entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6] run tag @s add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 16
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
particle minecraft:flash{color:11187395} ~ ~2 ~ 0 0 0 0 1 force
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 1 0.8
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 34
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 18
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
