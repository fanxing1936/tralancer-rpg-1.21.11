execute if score @s rpg_pf_l matches 9 if entity @s[tag=rpg.pf.lit] run data merge entity @s {start_interpolation:0,interpolation_duration:7,transformation:{scale:[3.125f,3.125f,1f]}}
execute if score @s rpg_pf_l matches 9 if entity @s[tag=rpg.pf.wide] run data merge entity @s {start_interpolation:0,interpolation_duration:7,transformation:{scale:[10f,1f,10f]}}
execute if score @s rpg_pf_l matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[0f,0f,0f]}}
