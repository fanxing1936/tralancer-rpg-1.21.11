execute if entity @s[tag=rpg.pf.cw] run tp @s ~ ~ ~ ~1.5 0
execute if entity @s[tag=rpg.pf.ccw] run tp @s ~ ~ ~ ~-2 0
execute if score @s rpg_pf_l matches 121 run data merge entity @s {start_interpolation:0,interpolation_duration:24,transformation:{scale:[60f,1f,60f]}}
execute if score @s rpg_pf_l matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{scale:[0f,1f,0f]}}
