execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_orb
execute if score @s rpg_pf_l matches 17 run data merge entity @s {start_interpolation:0,interpolation_duration:15,transformation:{scale:[4f,4f,1f]}}
