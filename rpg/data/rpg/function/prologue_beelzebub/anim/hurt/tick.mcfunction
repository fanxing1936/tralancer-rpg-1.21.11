# hurt：38 刻，播完回到 idle。由 add_prologue_models.py 生成。
execute if score @s rpg_prbz_t matches 39.. run return run function rpg:prologue_beelzebub/anim/enter/idle
scoreboard players add @s rpg_prbz_t 1
function rpg:prologue_beelzebub/anim/hurt/at
