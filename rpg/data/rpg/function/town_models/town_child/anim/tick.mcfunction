execute unless score @s rpg_tw_m10_anim matches 0..0 run function rpg:town_models/town_child/anim/init
execute if score @s rpg_tw_m10_anim matches 0 run return run function rpg:town_models/town_child/anim/idle/tick
