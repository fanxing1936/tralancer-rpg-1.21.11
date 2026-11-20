# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_slgm_anim 1
scoreboard players set @s rpg_slgm_t 0
return run function rpg:saul_ghost/anim/walk/tick
