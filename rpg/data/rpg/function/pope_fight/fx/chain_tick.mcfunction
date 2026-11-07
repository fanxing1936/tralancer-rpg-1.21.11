execute if entity @s[tag=rpg.pf.lo] at @a[distance=..8,sort=nearest,limit=1] run tp @s ~ ~0.6 ~ ~9 0
execute if entity @s[tag=rpg.pf.hi] at @a[distance=..8,sort=nearest,limit=1] run tp @s ~ ~1.3 ~ ~-9 0
execute if score @s rpg_pf_l matches 39 run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[1.3f,1.3f,1.3f]}}
execute if score @s rpg_pf_l matches 8 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[0f,0f,0f]}}
