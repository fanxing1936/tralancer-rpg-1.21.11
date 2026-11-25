tag @a remove rpg.vt.op
execute as @a if score @s rpg_vt_id = #c rpg_vt run tag @s add rpg.vt.op
data modify storage rpg:vault n set value {text:"",extra:[]}
data modify storage rpg:vault n.extra append from storage rpg:vault i.components."minecraft:custom_name"
execute store result storage rpg:vault c.n int 1 run data get storage rpg:vault i.count
execute unless data storage rpg:vault i{count:1} run function rpg:vault/count with storage rpg:vault c
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.vt.t","rpg.vt.tn"],billboard:"center",background:0,see_through:0b,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],scale:[0.95f,0.95f,0.95f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
data modify entity @e[type=minecraft:text_display,tag=rpg.vt.tn,distance=..3,limit=1] text set from storage rpg:vault n
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.vt.tn,distance=..3] rpg_vt_id = #c rpg_vt
tag @e[type=minecraft:text_display,tag=rpg.vt.tn,distance=..3] remove rpg.vt.tn
execute if score #q rpg_vt matches 1 run function rpg:vault/fx_1
execute if score #q rpg_vt matches 2 run function rpg:vault/fx_2
execute if score #q rpg_vt matches 3 run function rpg:vault/fx_3
execute if score #q rpg_vt matches 4 run function rpg:vault/fx_4
