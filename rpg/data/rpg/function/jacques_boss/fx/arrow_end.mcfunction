summon minecraft:text_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 10
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 3
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 10
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.4 8
execute if entity @s[tag=rpg.jqb.af] run particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.12 10
execute if entity @s[tag=rpg.jqb.af] run particle minecraft:lava ~ ~ ~ 0 0 0 0 2
playsound rpg:jacques.arrow hostile @a[distance=..16] ~ ~ ~ 0.6 1.2
scoreboard players set #d rpg_jq 8
execute if entity @s[tag=rpg.jqb.af] run function rpg:jacques_boss/fire/drop
kill @s
