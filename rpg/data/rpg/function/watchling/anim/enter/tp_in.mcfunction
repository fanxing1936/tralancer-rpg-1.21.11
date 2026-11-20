# 切到 tp_in 并立即播放第一帧。
scoreboard players set @s rpg_mkwm_anim 5
scoreboard players set @s rpg_mkwm_t 0
return run function rpg:watchling/anim/tp_in/tick
