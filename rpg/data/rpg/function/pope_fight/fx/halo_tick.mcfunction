execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_halo
execute if score @s rpg_pf_l matches 59 run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[3.4375f,3.4375f,1f]}}
execute if score @s rpg_pf_l matches 149 run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[3.4375f,3.4375f,1f]}}
execute if score @s rpg_pf_l matches 10 run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[0f,0f,1f]}}
