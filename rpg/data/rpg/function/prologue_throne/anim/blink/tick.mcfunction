# blink：24 刻，播完回到 idle。由 add_prologue_models.py 生成。
execute if score @s rpg_prth_t matches 25.. run return run function rpg:prologue_throne/anim/enter/idle
scoreboard players add @s rpg_prth_t 1
function rpg:prologue_throne/anim/blink/at
