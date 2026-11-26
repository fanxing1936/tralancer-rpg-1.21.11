# 一条 8 格的影子手；灯下夺不到
execute positioned ~ ~0.06 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[1711396]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,4.0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,0.05f,8.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.06 ~ run tp @e[tag=rpg.dt.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 8
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 20
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
execute positioned ^ ^ ^1.0 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^2.2 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^3.4 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^4.6 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^5.8 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^7.0 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^8.2 run tag @a[distance=..1.3,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute as @a[tag=rpg.dt.hit] at @s if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6] run tag @s remove rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/steal/caught
tag @a remove rpg.dt.hit
playsound minecraft:item.trident.throw hostile @a[distance=..48] ~ ~ ~ 1 0.5
