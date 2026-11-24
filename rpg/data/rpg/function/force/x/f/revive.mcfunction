tag @s add rpg.fo.self
execute as @e[type=minecraft:player,tag=rpg.fo.down,tag=!rpg.fo.self,limit=1,sort=nearest] run function rpg:force/x/f/revive_one
tag @s remove rpg.fo.self
playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1 1.6
summon minecraft:text_display ^ ^1.6 ^1.6 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 21
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
