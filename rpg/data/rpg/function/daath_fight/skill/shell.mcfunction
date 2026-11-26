scoreboard players set @s rpg_dt_sk 13
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/kneel
scoreboard players operation @s rpg_dt_shell = @s rpg_dt_mx
scoreboard players set #k rpg_dt 80
scoreboard players operation @s rpg_dt_shell *= #k rpg_dt
scoreboard players operation @s rpg_dt_shell /= #100 rpg_dt
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1 0.7
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagon","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 60
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 15
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
