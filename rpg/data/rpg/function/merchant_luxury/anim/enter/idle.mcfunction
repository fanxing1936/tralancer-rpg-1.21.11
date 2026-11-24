# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_mlx_anim 0
scoreboard players set @s rpg_mlx_t 0
return run function rpg:merchant_luxury/anim/idle/tick
