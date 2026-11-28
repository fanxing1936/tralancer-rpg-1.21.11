execute unless score @s rpg_tw_m5_anim matches 0..0 run function rpg:town_models/town_edgewalker/anim/init
execute if score @s rpg_tw_m5_anim matches 0 run return run function rpg:town_models/town_edgewalker/anim/idle/tick
