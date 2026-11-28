# 六翼全展（as/at 他）
particle minecraft:end_rod ~0.40 ~1.80 ~0.00 1.000 0.000 0.000 0.25 0 force
particle minecraft:end_rod ~0.37 ~1.80 ~0.15 0.924 0.000 0.383 0.25 0 force
particle minecraft:end_rod ~0.28 ~1.80 ~0.28 0.707 0.000 0.707 0.25 0 force
particle minecraft:end_rod ~0.15 ~1.80 ~0.37 0.383 0.000 0.924 0.25 0 force
particle minecraft:end_rod ~0.00 ~1.80 ~0.40 0.000 0.000 1.000 0.25 0 force
particle minecraft:end_rod ~-0.15 ~1.80 ~0.37 -0.383 0.000 0.924 0.25 0 force
particle minecraft:end_rod ~-0.28 ~1.80 ~0.28 -0.707 0.000 0.707 0.25 0 force
particle minecraft:end_rod ~-0.37 ~1.80 ~0.15 -0.924 0.000 0.383 0.25 0 force
particle minecraft:end_rod ~-0.40 ~1.80 ~0.00 -1.000 0.000 0.000 0.25 0 force
particle minecraft:end_rod ~-0.37 ~1.80 ~-0.15 -0.924 0.000 -0.383 0.25 0 force
particle minecraft:end_rod ~-0.28 ~1.80 ~-0.28 -0.707 0.000 -0.707 0.25 0 force
particle minecraft:end_rod ~-0.15 ~1.80 ~-0.37 -0.383 0.000 -0.924 0.25 0 force
particle minecraft:end_rod ~-0.00 ~1.80 ~-0.40 -0.000 0.000 -1.000 0.25 0 force
particle minecraft:end_rod ~0.15 ~1.80 ~-0.37 0.383 0.000 -0.924 0.25 0 force
particle minecraft:end_rod ~0.28 ~1.80 ~-0.28 0.707 0.000 -0.707 0.25 0 force
particle minecraft:end_rod ~0.37 ~1.80 ~-0.15 0.924 0.000 -0.383 0.25 0 force
summon minecraft:text_display ~ ~1.8 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,10f,10f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 33
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ^ ^1.8 ^-0.6 1.6 0.8 0.3 0 20
playsound minecraft:entity.phantom.flap hostile @a[distance=..40] ~ ~ ~ 1.6 0.7
