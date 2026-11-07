execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_halo
execute if score @s rpg_pf_l matches 39 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[2.25f,2.25f,1f]}}
execute if score @s rpg_pf_l matches 6 run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{scale:[0f,0f,1f]}}
