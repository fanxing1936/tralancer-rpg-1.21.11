execute unless score @s rpg_tw_m2_anim matches 0..0 run function rpg:town_models/town_bard/anim/init
execute if score @s rpg_tw_m2_anim matches 0 run return run function rpg:town_models/town_bard/anim/idle/tick
