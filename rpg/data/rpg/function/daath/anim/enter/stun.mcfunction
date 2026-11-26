# 切到 stun 并立即播放第一帧。
scoreboard players set @s rpg_dtm_anim 23
scoreboard players set @s rpg_dtm_t 0
return run function rpg:daath/anim/stun/tick
