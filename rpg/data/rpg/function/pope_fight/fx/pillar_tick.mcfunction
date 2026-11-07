execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_column
execute if score @s rpg_pf_l matches 29 run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{scale:[3.25f,11.25f,1f]}}
execute if score @s rpg_pf_l matches 8 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[0f,11.25f,1f]}}
