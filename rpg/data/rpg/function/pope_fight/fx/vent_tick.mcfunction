execute if score @s rpg_pf_l matches 15 run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[4f,1f,4f]}}
execute if score @s rpg_pf_l matches 1 run function rpg:pope_fight/fx/vent_boom
