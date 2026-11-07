execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_beam
execute if score @s rpg_pf_l matches 36 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[15f,5f,1f]}}
execute if score @s rpg_pf_l matches 4 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[15f,0f,1f]}}
