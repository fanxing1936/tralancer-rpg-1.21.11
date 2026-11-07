execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_beam_gold
execute if score @s rpg_pf_l matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[25f,5.5f,1f]}}
execute if score @s rpg_pf_l matches 3 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[25f,0f,1f]}}
execute if score @s rpg_pf_l matches 12 if entity @s[tag=rpg.pf.lancehit] run function rpg:pope_fight/fx/lance_fire
execute if score @s rpg_pf_l matches 10 if entity @s[tag=rpg.pf.lancehit] run function rpg:pope_fight/fx/lance_ray
execute if score @s rpg_pf_l matches 4 if entity @s[tag=rpg.pf.lancehit] run function rpg:pope_fight/fx/lance_ray
