scoreboard players operation @s rpg_fo_buf = #now rpg_fo
scoreboard players add @s rpg_fo_buf 200
scoreboard players set @s rpg_fo_bk 4
scoreboard players operation @s rpg_fo_blv = #lv rpg_fo
scoreboard players set @s rpg_fo_dd 0
playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 1.3
particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.05 40
summon minecraft:text_display ^-0.4 ^1.2 ^0.5 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 21
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
