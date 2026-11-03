# 切到 cast 并立即播放第一帧。
scoreboard players set @s rpg_tw_anim 3
scoreboard players set @s rpg_tw_t 0
return run function rpg:tower_wraith/anim/cast/tick
