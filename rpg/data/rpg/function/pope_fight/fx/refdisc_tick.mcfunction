tp @s ~ ~ ~ ~4 0
execute if score @s rpg_pf_l matches 109 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[7f,1f,7f]}}
