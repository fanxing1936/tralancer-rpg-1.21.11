execute if score #lv rpg_fo matches 1 run effect give @s minecraft:absorption 20 1 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:absorption 20 2 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:absorption 20 3 true
playsound minecraft:entity.slime.squish_small player @a[distance=..16] ~ ~ ~ 1 0.5
playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.6
particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.3} ~ ~1 ~ 0.4 0.7 0.4 0 40
summon minecraft:text_display ^ ^1 ^1.4 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A1E"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagon","minecraft:custom_model_data":{colors:[9112094]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,1f,2.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 30
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
