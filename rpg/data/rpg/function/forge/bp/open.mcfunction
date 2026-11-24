function rpg:forge/bp/find
execute if score @s rpg_fg_arg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　副手拿着图纸，主手拿器胚，再对准魂火右键","color":"#C04A3C","bold":false,"italic":false}]
execute if score @s rpg_fg_arg matches 1 run function rpg:forge/bp/check_starry
execute if score @s rpg_fg_arg matches 1 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_starry
execute if score @s rpg_fg_arg matches 2 run function rpg:forge/bp/check_leviathan_song
execute if score @s rpg_fg_arg matches 2 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_leviathan_song
execute if score @s rpg_fg_arg matches 3 run function rpg:forge/bp/check_flame_pride
execute if score @s rpg_fg_arg matches 3 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_flame_pride
execute if score @s rpg_fg_arg matches 4 run function rpg:forge/bp/check_wind_echo
execute if score @s rpg_fg_arg matches 4 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_wind_echo
execute if score @s rpg_fg_arg matches 5 run function rpg:forge/bp/check_mountain_roar
execute if score @s rpg_fg_arg matches 5 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_mountain_roar
execute if score @s rpg_fg_arg matches 6 run function rpg:forge/bp/check_grave_bane
execute if score @s rpg_fg_arg matches 6 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_grave_bane
execute if score @s rpg_fg_arg matches 7 run function rpg:forge/bp/check_harp_crossbow
execute if score @s rpg_fg_arg matches 7 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_harp_crossbow
execute if score @s rpg_fg_arg matches 8 run function rpg:forge/bp/check_azure_seeker
execute if score @s rpg_fg_arg matches 8 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_azure_seeker
execute if score @s rpg_fg_arg matches 9 run function rpg:forge/bp/check_gale_bow
execute if score @s rpg_fg_arg matches 9 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_gale_bow
execute if score @s rpg_fg_arg matches 10 run function rpg:forge/bp/check_jachin
execute if score @s rpg_fg_arg matches 10 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_jachin
execute if score @s rpg_fg_arg matches 11 run function rpg:forge/bp/check_boaz
execute if score @s rpg_fg_arg matches 11 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_boaz
execute if score @s rpg_fg_arg matches 12 run function rpg:forge/bp/check_molten_hammer
execute if score @s rpg_fg_arg matches 12 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_molten_hammer
execute if score @s rpg_fg_arg matches 13 run function rpg:forge/bp/check_dark_sun
execute if score @s rpg_fg_arg matches 13 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_dark_sun
execute if score @s rpg_fg_arg matches 14 run function rpg:forge/bp/check_chainsaw
execute if score @s rpg_fg_arg matches 14 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_chainsaw
execute if score @s rpg_fg_arg matches 15 run function rpg:forge/bp/check_earth_spine
execute if score @s rpg_fg_arg matches 15 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_earth_spine
execute if score @s rpg_fg_arg matches 16 run function rpg:forge/bp/check_venom_fang
execute if score @s rpg_fg_arg matches 16 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_venom_fang
execute if score @s rpg_fg_arg matches 17 run function rpg:forge/bp/check_wind_bone
execute if score @s rpg_fg_arg matches 17 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_wind_bone
execute if score @s rpg_fg_arg matches 18 run function rpg:forge/bp/check_mischief_bow
execute if score @s rpg_fg_arg matches 18 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_mischief_bow
execute if score @s rpg_fg_arg matches 19 run function rpg:forge/bp/check_vine_whip
execute if score @s rpg_fg_arg matches 19 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_vine_whip
execute if score @s rpg_fg_arg matches 20 run function rpg:forge/bp/check_truth_blade
execute if score @s rpg_fg_arg matches 20 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_truth_blade
execute if score @s rpg_fg_arg matches 21 run function rpg:forge/bp/check_crystal_roar
execute if score @s rpg_fg_arg matches 21 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_crystal_roar
