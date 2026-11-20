# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_slgm_anim 0
scoreboard players set @s rpg_slgm_t 0
return run function rpg:saul_ghost/anim/idle/tick
