execute if score @s rpg_pf_l matches 29 run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[5f,1f,5f]}}
execute if score @s rpg_pf_l matches 16 positioned ~ ~18 ~ run function rpg:pope_fight/fx/shell_down
execute if score @s rpg_pf_l matches 1 run function rpg:pope_fight/fx/mark_boom
