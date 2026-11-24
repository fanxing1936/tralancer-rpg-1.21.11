# 每个载体独立记下片段和刻数。
execute unless score @s rpg_mtr_anim matches 0..3 run function rpg:merchant_travel/anim/init
execute if score @s rpg_mtr_anim matches 0 run return run function rpg:merchant_travel/anim/idle/tick
execute if score @s rpg_mtr_anim matches 1 run return run function rpg:merchant_travel/anim/look/tick
execute if score @s rpg_mtr_anim matches 2 run return run function rpg:merchant_travel/anim/bow/tick
execute if score @s rpg_mtr_anim matches 3 run return run function rpg:merchant_travel/anim/examine/tick
