execute unless score @s rpg_tw_m8_anim matches 0..1 run function rpg:town_models/town_folk_b/anim/init
execute if score @s rpg_tw_m8_anim matches 0 run return run function rpg:town_models/town_folk_b/anim/idle/tick
execute if score @s rpg_tw_m8_anim matches 1 run return run function rpg:town_models/town_folk_b/anim/look/tick
