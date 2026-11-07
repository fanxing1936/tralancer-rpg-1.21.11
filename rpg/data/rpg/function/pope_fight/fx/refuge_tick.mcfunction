execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_column
execute if score @s rpg_pf_l matches 109 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[2f,11.25f,1f]}}
execute if score #h rpg_pf matches 0 run particle end_rod ~ ~1 ~ 1.5 1 1.5 0.02 6 normal
