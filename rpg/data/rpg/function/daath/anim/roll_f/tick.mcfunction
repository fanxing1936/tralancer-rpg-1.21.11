# roll_f：12 刻，播完回到 idle。由 add_daath_model.py 生成。
execute if score @s rpg_dtm_t matches 13.. run return run function rpg:daath/anim/enter/idle
scoreboard players add @s rpg_dtm_t 1
function rpg:daath/anim/roll_f/at
