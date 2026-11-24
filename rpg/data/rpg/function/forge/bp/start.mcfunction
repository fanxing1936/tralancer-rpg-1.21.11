# 开炉：靠近灵魂火、再核对一遍
function rpg:forge/bp/find
scoreboard players operation #me rpg_fg = @s rpg_fg_id
scoreboard players set #fire rpg_fg 0
execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1
execute if score #fire rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　离灵魂火太远了，靠近些再开炉","color":"#C04A3C","bold":false,"italic":false}]
execute if score @s rpg_fg_arg matches 1 run function rpg:forge/bp/check_starry
execute if score @s rpg_fg_arg matches 1 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_starry
execute if score @s rpg_fg_arg matches 2 run function rpg:forge/bp/check_leviathan_song
execute if score @s rpg_fg_arg matches 2 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_leviathan_song
execute if score @s rpg_fg_arg matches 3 run function rpg:forge/bp/check_flame_pride
execute if score @s rpg_fg_arg matches 3 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_flame_pride
execute if score @s rpg_fg_arg matches 4 run function rpg:forge/bp/check_wind_echo
execute if score @s rpg_fg_arg matches 4 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_wind_echo
execute if score @s rpg_fg_arg matches 5 run function rpg:forge/bp/check_mountain_roar
execute if score @s rpg_fg_arg matches 5 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_mountain_roar
execute if score @s rpg_fg_arg matches 6 run function rpg:forge/bp/check_grave_bane
execute if score @s rpg_fg_arg matches 6 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_grave_bane
execute if score @s rpg_fg_arg matches 7 run function rpg:forge/bp/check_harp_crossbow
execute if score @s rpg_fg_arg matches 7 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_harp_crossbow
execute if score @s rpg_fg_arg matches 8 run function rpg:forge/bp/check_azure_seeker
execute if score @s rpg_fg_arg matches 8 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_azure_seeker
execute if score @s rpg_fg_arg matches 9 run function rpg:forge/bp/check_gale_bow
execute if score @s rpg_fg_arg matches 9 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_gale_bow
execute if score @s rpg_fg_arg matches 10 run function rpg:forge/bp/check_jachin
execute if score @s rpg_fg_arg matches 10 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_jachin
execute if score @s rpg_fg_arg matches 11 run function rpg:forge/bp/check_boaz
execute if score @s rpg_fg_arg matches 11 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_boaz
execute if score @s rpg_fg_arg matches 12 run function rpg:forge/bp/check_molten_hammer
execute if score @s rpg_fg_arg matches 12 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_molten_hammer
execute if score @s rpg_fg_arg matches 13 run function rpg:forge/bp/check_dark_sun
execute if score @s rpg_fg_arg matches 13 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_dark_sun
execute if score @s rpg_fg_arg matches 14 run function rpg:forge/bp/check_chainsaw
execute if score @s rpg_fg_arg matches 14 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_chainsaw
execute if score @s rpg_fg_arg matches 15 run function rpg:forge/bp/check_earth_spine
execute if score @s rpg_fg_arg matches 15 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_earth_spine
execute if score @s rpg_fg_arg matches 16 run function rpg:forge/bp/check_venom_fang
execute if score @s rpg_fg_arg matches 16 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_venom_fang
execute if score @s rpg_fg_arg matches 17 run function rpg:forge/bp/check_wind_bone
execute if score @s rpg_fg_arg matches 17 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_wind_bone
execute if score @s rpg_fg_arg matches 18 run function rpg:forge/bp/check_mischief_bow
execute if score @s rpg_fg_arg matches 18 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_mischief_bow
execute if score @s rpg_fg_arg matches 19 run function rpg:forge/bp/check_vine_whip
execute if score @s rpg_fg_arg matches 19 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_vine_whip
execute if score @s rpg_fg_arg matches 20 run function rpg:forge/bp/check_truth_blade
execute if score @s rpg_fg_arg matches 20 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_truth_blade
execute if score @s rpg_fg_arg matches 21 run function rpg:forge/bp/check_crystal_roar
execute if score @s rpg_fg_arg matches 21 if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_crystal_roar
