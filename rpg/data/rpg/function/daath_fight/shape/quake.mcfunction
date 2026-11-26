summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath_fx/crack_mirror","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.5f,1f,5.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 50
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath_fx/smash_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 36
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:cloud ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.28 0 force
particle minecraft:cloud ~0.38 ~0.20 ~0.14 0.940 0.000 0.342 0.28 0 force
particle minecraft:cloud ~0.31 ~0.20 ~0.26 0.766 0.000 0.643 0.28 0 force
particle minecraft:cloud ~0.20 ~0.20 ~0.35 0.500 0.000 0.866 0.28 0 force
particle minecraft:cloud ~0.07 ~0.20 ~0.39 0.174 0.000 0.985 0.28 0 force
particle minecraft:cloud ~-0.07 ~0.20 ~0.39 -0.174 0.000 0.985 0.28 0 force
particle minecraft:cloud ~-0.20 ~0.20 ~0.35 -0.500 0.000 0.866 0.28 0 force
particle minecraft:cloud ~-0.31 ~0.20 ~0.26 -0.766 0.000 0.643 0.28 0 force
particle minecraft:cloud ~-0.38 ~0.20 ~0.14 -0.940 0.000 0.342 0.28 0 force
particle minecraft:cloud ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.28 0 force
particle minecraft:cloud ~-0.38 ~0.20 ~-0.14 -0.940 0.000 -0.342 0.28 0 force
particle minecraft:cloud ~-0.31 ~0.20 ~-0.26 -0.766 0.000 -0.643 0.28 0 force
particle minecraft:cloud ~-0.20 ~0.20 ~-0.35 -0.500 0.000 -0.866 0.28 0 force
particle minecraft:cloud ~-0.07 ~0.20 ~-0.39 -0.174 0.000 -0.985 0.28 0 force
particle minecraft:cloud ~0.07 ~0.20 ~-0.39 0.174 0.000 -0.985 0.28 0 force
particle minecraft:cloud ~0.20 ~0.20 ~-0.35 0.500 0.000 -0.866 0.28 0 force
particle minecraft:cloud ~0.31 ~0.20 ~-0.26 0.766 0.000 -0.643 0.28 0 force
particle minecraft:cloud ~0.38 ~0.20 ~-0.14 0.940 0.000 -0.342 0.28 0 force
particle minecraft:block{block_state:"minecraft:black_stained_glass"} ~ ~0.2 ~ 1 0.1 1 0.1 24
playsound minecraft:entity.player.attack.strong hostile @a[distance=..32] ~ ~ ~ 1.2 0.6
playsound minecraft:block.glass.break hostile @a[distance=..32] ~ ~ ~ 0.8 0.6
