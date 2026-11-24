scoreboard players operation @s rpg_fo_wr = #now rpg_fo
scoreboard players add @s rpg_fo_wr 200
scoreboard players set @s rpg_fo_dt 0
playsound minecraft:entity.ender_dragon.growl player @a[distance=..24] ~ ~ ~ 0.6 1.4
particle minecraft:flame ~ ~1 ~ 0.6 1 0.6 0.05 60
summon minecraft:text_display ^ ^1.2 ^3 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"#FF5C52"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
