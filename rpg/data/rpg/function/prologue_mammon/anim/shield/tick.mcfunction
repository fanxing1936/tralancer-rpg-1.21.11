# shield：12 刻，播完回到 idle。由 add_prologue_models.py 生成。
execute if score @s rpg_prmm_t matches 13.. run return 0
scoreboard players add @s rpg_prmm_t 1
function rpg:prologue_mammon/anim/shield/at
