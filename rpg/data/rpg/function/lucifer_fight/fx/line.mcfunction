scoreboard players set #d rpg_l2_v 0
function rpg:lucifer_fight/fx/line_step
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.aim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/lure"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:0,interpolation_duration:3,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.16f,0.16f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 11
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 20
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
execute as @e[tag=rpg.lu2f.aim,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rpg.lu2f.aim,limit=1] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d rpg_l2_v
execute as @e[tag=rpg.lu2f.aim,limit=1] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d rpg_l2_v
tag @e[tag=rpg.lu2f.aim] remove rpg.lu2f.aim
