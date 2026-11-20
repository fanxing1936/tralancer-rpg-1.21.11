# 坚毅铠甲：甲片弹开了这一下（as/at 他；下一刻退回伤害）
scoreboard players set @e[tag=rpg.unit,tag=rpg.slb.att] rpg_sl_v 1
summon minecraft:text_display ^ ^1.4 ^0.6 {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#D8DEE6"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 10
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ^ ^1.3 ^0.7 0.3 0.4 0.3 0.4 12
particle minecraft:electric_spark ^ ^1.3 ^0.7 0.2 0.3 0.2 0.3 6
playsound minecraft:item.shield.block hostile @a[distance=..24] ~ ~ ~ 1 1.3
playsound minecraft:block.anvil.land hostile @a[distance=..24] ~ ~ ~ 0.3 1.8
