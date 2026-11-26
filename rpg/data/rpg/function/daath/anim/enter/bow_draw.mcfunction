# 切到 bow_draw 并立即播放第一帧。
scoreboard players set @s rpg_dtm_anim 3
scoreboard players set @s rpg_dtm_t 0
return run function rpg:daath/anim/bow_draw/tick
