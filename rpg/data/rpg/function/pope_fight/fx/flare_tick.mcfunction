execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_flare
execute if score @s rpg_pf_l matches 40 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[4.375f,4.375f,1f]}}
execute if score @s rpg_pf_l matches 4 run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0f,0f,1f]}}
