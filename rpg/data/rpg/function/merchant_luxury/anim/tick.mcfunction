# 每个载体独立记下片段和刻数。
execute unless score @s rpg_mlx_anim matches 0..3 run function rpg:merchant_luxury/anim/init
execute if score @s rpg_mlx_anim matches 0 run return run function rpg:merchant_luxury/anim/idle/tick
execute if score @s rpg_mlx_anim matches 1 run return run function rpg:merchant_luxury/anim/look/tick
execute if score @s rpg_mlx_anim matches 2 run return run function rpg:merchant_luxury/anim/bow/tick
execute if score @s rpg_mlx_anim matches 3 run return run function rpg:merchant_luxury/anim/examine/tick
