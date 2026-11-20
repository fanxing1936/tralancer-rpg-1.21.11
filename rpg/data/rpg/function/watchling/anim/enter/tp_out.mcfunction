# 切到 tp_out 并立即播放第一帧。
scoreboard players set @s rpg_mkwm_anim 4
scoreboard players set @s rpg_mkwm_t 0
return run function rpg:watchling/anim/tp_out/tick
