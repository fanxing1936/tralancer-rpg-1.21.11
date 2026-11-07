execute if entity @s[tag=rpg.pf.cw] run tp @s ~ ~ ~ ~3 0
execute if entity @s[tag=rpg.pf.ccw] run tp @s ~ ~ ~ ~-4 0
execute if score @s rpg_pf_l matches 39 if entity @s[tag=rpg.pf.big] run data merge entity @s {start_interpolation:0,interpolation_duration:14,transformation:{scale:[6f,1f,6f]}}
execute if score @s rpg_pf_l matches 39 if entity @s[tag=rpg.pf.small] run data merge entity @s {start_interpolation:0,interpolation_duration:14,transformation:{scale:[3f,1f,3f]}}
execute if score @s rpg_pf_l matches 39 if entity @s[tag=rpg.pf.mid] run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[5f,1f,5f]}}
execute if score @s rpg_pf_l matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{scale:[0f,1f,0f]}}
