execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_vortex_void
execute if score @s rpg_pf_l matches 107 run data merge entity @s {start_interpolation:0,interpolation_duration:30,transformation:{scale:[10f,6.6667f,1f]}}
execute if score @s rpg_pf_l matches 8 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[0f,6.6667f,1f]}}
