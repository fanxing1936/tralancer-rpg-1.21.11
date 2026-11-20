# 切到 hero 并立即播放第一帧。
scoreboard players set @s rpg_slm_anim 16
scoreboard players set @s rpg_slm_t 0
return run function rpg:saul/anim/hero/tick
