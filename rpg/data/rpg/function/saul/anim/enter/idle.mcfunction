# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_slm_anim 0
scoreboard players set @s rpg_slm_t 0
return run function rpg:saul/anim/idle/tick
