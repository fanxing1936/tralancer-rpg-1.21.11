# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_usm_anim 2
scoreboard players set @s rpg_usm_t 0
return run function rpg:usurper/anim/attack/tick
