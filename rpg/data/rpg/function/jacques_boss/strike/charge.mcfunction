execute positioned ^ ^ ^1.8 run tag @e[tag=rpg.unit.f,distance=..2.5] add rpg.jqb.hit
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 10 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
summon minecraft:text_display ^ ^1.2 ^1.6 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 13
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ^ ^1.3 ^1.7 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4.75f,4.75f,4.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 13
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:crit ^ ^1 ^1.8 0.8 0.4 0.8 0.3 16
execute positioned ^ ^ ^1.8 run function rpg:jacques_boss/vfx/impact
