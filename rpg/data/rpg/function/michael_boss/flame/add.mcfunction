# 叠一层圣焰（as 玩家）
tag @s add rpg.mkb.flamed
scoreboard players add @s rpg_mk_fl 1
scoreboard players set @s rpg_mk_ft 100
execute at @s run summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 8
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 38
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
execute if score @s rpg_mk_fl matches 3.. unless score @s rpg_mk_fu matches 1.. run function rpg:michael_boss/flame/kindle
execute if score @s rpg_mk_fl matches 1 run title @s actionbar [{"text":"圣焰 ","color":"#FF805F"},{"text":"● ○ ○","color":"#FF3300"}]
execute if score @s rpg_mk_fl matches 2 run title @s actionbar [{"text":"圣焰 ","color":"#FF805F"},{"text":"● ● ○","color":"#FF3300"}]
