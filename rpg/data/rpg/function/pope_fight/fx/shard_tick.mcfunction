tp @s ^ ^ ^0.35
execute if score @s rpg_pf_l matches 29 if entity @s[type=minecraft:item_display] run data merge entity @s {start_interpolation:0,interpolation_duration:17,transformation:{left_rotation:[0.7071f,0f,0.7071f,0f]}}
execute if score @s rpg_pf_l matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{scale:[0f,0f,0f]}}
