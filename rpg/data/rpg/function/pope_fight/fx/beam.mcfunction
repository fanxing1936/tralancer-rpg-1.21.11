execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_beam
execute if score @s rpg_pf_l matches 40 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[15f,6f,1f]}}
execute if score @s rpg_pf_l matches 3 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[15f,0f,1f]}}
execute if score @s rpg_pf_l matches 41.. run return 0
execute if score #dir rpg_pf matches 0 run tp @s ~ ~ ~ ~1.5 0
execute if score #dir rpg_pf matches 1 run tp @s ~ ~ ~ ~-1.5 0
execute if score @s rpg_pf_l matches 3.. if entity @s[tag=rpg.pf.beamhit] run function rpg:pope_fight/fx/beam_sweep
