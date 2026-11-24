scoreboard players operation @s rpg_fo_buf = #now rpg_fo
execute if score #lv rpg_fo matches 1 run scoreboard players add @s rpg_fo_buf 100
execute if score #lv rpg_fo matches 2 run scoreboard players add @s rpg_fo_buf 120
execute if score #lv rpg_fo matches 3 run scoreboard players add @s rpg_fo_buf 140
scoreboard players set @s rpg_fo_bk 14
scoreboard players operation @s rpg_fo_blv = #lv rpg_fo
scoreboard players set @s rpg_fo_dd 0
playsound minecraft:entity.wither.ambient player @a[distance=..16] ~ ~ ~ 0.5 1.6
particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.2} ~ ~1 ~ 0.3 0.6 0.3 0 40
summon minecraft:text_display ^ ^1.2 ^1.2 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A1E"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 8
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 13
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
