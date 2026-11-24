# 每个载体独立记下片段和刻数。
execute unless score @s rpg_msm_anim matches 0..3 run function rpg:merchant_smith/anim/init
execute if score @s rpg_msm_anim matches 0 run return run function rpg:merchant_smith/anim/idle/tick
execute if score @s rpg_msm_anim matches 1 run return run function rpg:merchant_smith/anim/look/tick
execute if score @s rpg_msm_anim matches 2 run return run function rpg:merchant_smith/anim/bow/tick
execute if score @s rpg_msm_anim matches 3 run return run function rpg:merchant_smith/anim/examine/tick
