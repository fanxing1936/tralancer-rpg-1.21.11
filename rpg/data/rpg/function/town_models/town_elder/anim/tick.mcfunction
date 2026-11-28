execute unless score @s rpg_tw_m1_anim matches 0..1 run function rpg:town_models/town_elder/anim/init
execute if score @s rpg_tw_m1_anim matches 0 run return run function rpg:town_models/town_elder/anim/idle/tick
execute if score @s rpg_tw_m1_anim matches 1 run return run function rpg:town_models/town_elder/anim/look/tick
