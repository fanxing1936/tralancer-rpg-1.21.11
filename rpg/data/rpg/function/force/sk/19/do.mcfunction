damage @s 6 rpg:force
execute if score #lv rpg_fo matches 1 run execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 40
execute if score #lv rpg_fo matches 2 run execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 50
execute if score #lv rpg_fo matches 3 run execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 60
execute if score #lv rpg_fo matches 1 run execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 40
execute if score #lv rpg_fo matches 2 run execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 50
execute if score #lv rpg_fo matches 3 run execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 60
playsound minecraft:entity.player.hurt_sweet_berry_bush player @s ~ ~ ~ 1 0.6
playsound minecraft:block.respawn_anchor.charge player @a[distance=..16] ~ ~ ~ 0.6 0.6
particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.5} ~ ~1 ~ 0.3 0.6 0.3 0 50
particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.04 15
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[9112094]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.2f,1f,3.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 30
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:text_display ^ ^1 ^1.4 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A1E"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
