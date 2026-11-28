# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_tw_m6_anim 0
scoreboard players set @s rpg_tw_m6_t 0
return run function rpg:town_models/town_inquisitor/anim/idle/tick
