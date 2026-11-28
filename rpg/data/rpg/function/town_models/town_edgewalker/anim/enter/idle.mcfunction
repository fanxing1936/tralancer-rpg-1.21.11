# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_tw_m5_anim 0
scoreboard players set @s rpg_tw_m5_t 0
return run function rpg:town_models/town_edgewalker/anim/idle/tick
