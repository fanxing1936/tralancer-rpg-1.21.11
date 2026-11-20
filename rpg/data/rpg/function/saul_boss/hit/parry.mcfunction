# 招架中被正面打到：格开，立刻反击（as/at 他；下一刻退回伤害）
scoreboard players set @e[tag=rpg.unit,tag=rpg.slb.att] rpg_sl_v 2
tag @s remove rpg.slb.guard
summon minecraft:text_display ^ ^1.4 ^0.8 {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 4
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:flash{color:15660282} ^ ^1.4 ^0.8 0 0 0 0 1 force
particle minecraft:crit ^ ^1.3 ^0.8 0.3 0.4 0.3 0.6 20
playsound minecraft:item.shield.block hostile @a[distance=..24] ~ ~ ~ 1.2 1.6
playsound minecraft:block.chain.break hostile @a[distance=..24] ~ ~ ~ 1 1.4
function rpg:saul_boss/skill/counter
