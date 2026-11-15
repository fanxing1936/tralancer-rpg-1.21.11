# 放出一枚圣光弹（at 手前），朝最近的人的眼睛直飞
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.ei.bolt","rpg.ei.bnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2A8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,view_range:2f,transformation:{translation:[0f,-0.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:text_display,tag=rpg.ei.bnew] at @s run tp @s ~ ~ ~ facing entity @e[tag=rpg.unit.f,distance=..24,sort=nearest,limit=1] eyes
scoreboard players set @e[type=minecraft:text_display,tag=rpg.ei.bnew] rpg_ei_life 40
tag @e[type=minecraft:text_display,tag=rpg.ei.bnew] remove rpg.ei.bnew
playsound rpg:end_illager.cast hostile @a[distance=..24] ~ ~ ~ 1 1.2
particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.05 10 normal
