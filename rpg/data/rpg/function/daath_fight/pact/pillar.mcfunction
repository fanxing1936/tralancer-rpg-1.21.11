execute if entity @a[distance=..2.5,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] run tag @a[distance=..2.5,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 12
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 1 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 2 run particle dust_color_transition{from_color:[0.31,0.62,0.94],to_color:[0.11,0.31,0.45],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 3 run particle dust_color_transition{from_color:[0.65,0.69,0.79],to_color:[0.42,0.42,0.44],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 4 run particle dust_color_transition{from_color:[0.71,0.85,0.34],to_color:[0.35,0.42,0.12],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 5 run particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 6 run particle dust_color_transition{from_color:[0.85,0.48,0.85],to_color:[0.36,0.17,0.44],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute if score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 7 run particle dust_color_transition{from_color:[0.9,0.64,0.24],to_color:[0.72,0.58,0.04],scale:2} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
execute unless score @a[tag=rpg.dt.me,limit=1] rpg_pact matches 1..7 run particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~2 ~ 0.6 1.6 0.6 0 40 force
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 24
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 19
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:end_rod ~ ~5 ~ 0.15 5 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[8160659]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 16
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 5
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..48] ~ ~ ~ 0.6 0.8
