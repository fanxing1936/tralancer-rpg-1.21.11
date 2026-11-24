# roll_l：14 刻，播完回到 idle。由 add_prologue_models.py 生成。
execute if score @s rpg_prmi_t matches 15.. run return run function rpg:prologue_michael/anim/enter/idle
scoreboard players add @s rpg_prmi_t 1
function rpg:prologue_michael/anim/roll_l/at
