playsound minecraft:block.bubble_column.upwards_inside player @a[distance=..16] ~ ~ ~ 1 1.2
playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 1.4
particle minecraft:end_rod ~ ~1 ~ 3 0.6 3 0.01 60
execute as @a[distance=..6,gamemode=!spectator] at @s run function rpg:force/sk/7/one
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 26
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:text_display ^ ^1.6 ^1.6 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 24
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
