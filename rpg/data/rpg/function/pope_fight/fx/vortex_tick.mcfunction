execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_vortex
execute if score @s rpg_pf_l matches 149 run data merge entity @s {start_interpolation:0,interpolation_duration:30,transformation:{scale:[5.8333f,5f,1f]}}
