# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_slm_anim 1
scoreboard players set @s rpg_slm_t 0
return run function rpg:saul/anim/walk/tick
