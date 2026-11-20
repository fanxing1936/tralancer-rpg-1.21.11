# 切到 heavy 并立即播放第一帧。
scoreboard players set @s rpg_mkwm_anim 3
scoreboard players set @s rpg_mkwm_t 0
return run function rpg:watchling/anim/heavy/tick
