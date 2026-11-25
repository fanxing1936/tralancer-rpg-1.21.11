# 停在开箱人面前的那件亮出来
execute as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=1..}] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0.000f,0.000f,1.250f],scale:[0.000f,0.000f,0.000f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=0}] run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{translation:[0.000f,0.450f,0.000f],scale:[1.000f,1.000f,1.000f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation #q rpg_vt = @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=0},limit=1] rpg_vt_q
data modify storage rpg:vault i set from entity @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=0},limit=1] item
function rpg:vault/show
