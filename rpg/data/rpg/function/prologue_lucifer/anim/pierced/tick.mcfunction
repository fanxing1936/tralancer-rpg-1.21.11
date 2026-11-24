# pierced：40 刻，播完回到 idle。由 add_prologue_models.py 生成。
execute if score @s rpg_prlu_t matches 41.. run return run function rpg:prologue_lucifer/anim/enter/idle
scoreboard players add @s rpg_prlu_t 1
function rpg:prologue_lucifer/anim/pierced/at
