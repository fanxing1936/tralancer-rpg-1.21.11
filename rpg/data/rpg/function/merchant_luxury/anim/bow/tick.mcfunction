# bow：33 刻，播完回到 idle。由 add_merchant_models.py 生成。
execute if score @s rpg_mlx_t matches 34.. run return run function rpg:merchant_luxury/anim/enter/idle
scoreboard players add @s rpg_mlx_t 1
function rpg:merchant_luxury/anim/bow/at
