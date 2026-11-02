# rise：48 刻，播完回到 idle。由 add_beelzebub.py 生成。
execute if score @s rpg_bz_t matches 49.. run return run function rpg:beelzebub/anim/enter/idle
scoreboard players add @s rpg_bz_t 1
function rpg:beelzebub/anim/rise/at
