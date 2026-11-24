# idle：100 刻循环。由 add_merchant_models.py 生成。
execute if score @s rpg_mlx_t matches 100.. run scoreboard players set @s rpg_mlx_t 0
scoreboard players add @s rpg_mlx_t 1
function rpg:merchant_luxury/anim/idle/at
