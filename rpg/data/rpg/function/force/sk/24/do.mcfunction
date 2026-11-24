playsound minecraft:block.end_portal_frame.fill player @a[distance=..16] ~ ~ ~ 1 0.6
particle minecraft:sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.05 30
tag @s add rpg.pact.cast
execute if score @s rpg_pact matches 1 run function rpg:pact/p1
execute if score @s rpg_pact matches 2 run function rpg:pact/p2
execute if score @s rpg_pact matches 3 run function rpg:pact/p3
execute if score @s rpg_pact matches 4 run function rpg:pact/p4
execute if score @s rpg_pact matches 5 run function rpg:pact/p5
execute if score @s rpg_pact matches 6 run function rpg:pact/p6
execute if score @s rpg_pact matches 7 run function rpg:pact/p7
tag @s remove rpg.pact.cast
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[10647230]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 30
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:text_display ^ ^1.2 ^1.6 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#A276BE"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
