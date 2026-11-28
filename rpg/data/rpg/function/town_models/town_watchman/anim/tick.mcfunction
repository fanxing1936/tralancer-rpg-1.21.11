execute unless score @s rpg_tw_m3_anim matches 0..0 run function rpg:town_models/town_watchman/anim/init
execute if score @s rpg_tw_m3_anim matches 0 run return run function rpg:town_models/town_watchman/anim/idle/tick
