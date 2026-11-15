# slash2：22 刻，播完回到 idle。由 add_jacques_model.py 生成。
execute if score @s rpg_jqm_t matches 23.. run return run function rpg:jacques/anim/enter/idle
scoreboard players add @s rpg_jqm_t 1
function rpg:jacques/anim/slash2/at
