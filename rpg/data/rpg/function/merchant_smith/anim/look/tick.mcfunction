# look：46 刻，播完回到 idle。由 add_merchant_models.py 生成。
execute if score @s rpg_msm_t matches 47.. run return run function rpg:merchant_smith/anim/enter/idle
scoreboard players add @s rpg_msm_t 1
function rpg:merchant_smith/anim/look/at
