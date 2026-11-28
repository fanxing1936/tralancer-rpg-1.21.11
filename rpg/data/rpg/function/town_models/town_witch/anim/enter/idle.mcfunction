# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_tw_m4_anim 0
scoreboard players set @s rpg_tw_m4_t 0
return run function rpg:town_models/town_witch/anim/idle/tick
