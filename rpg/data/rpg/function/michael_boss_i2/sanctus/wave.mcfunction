# 一道焰墙（as/at 他）：一个圆心标记，带波号；地上一圈往外长的火环
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.wave","rpg.mkb.wavenew"]}
scoreboard players set @e[tag=rpg.mkb.wavenew,distance=0..] rpg_mk_life 61
scoreboard players set @e[tag=rpg.mkb.wavenew,distance=0..] rpg_mk_kd 0
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_t","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 19
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/glow_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 17
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 4
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute rotated 0 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 12 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 24 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 36 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 48 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 60 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 72 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 84 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 96 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 108 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 120 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 132 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 144 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 156 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 168 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 180 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 192 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 204 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 216 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 228 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 240 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 252 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 264 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 276 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 288 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 300 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 312 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 324 0 run function rpg:michael_boss_i2/sanctus/flame
execute rotated 336 0 run function rpg:michael_boss_i2/sanctus/spoke
execute rotated 348 0 run function rpg:michael_boss_i2/sanctus/spoke
