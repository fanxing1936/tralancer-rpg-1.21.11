# 切到 look 并立即播放第一帧。
scoreboard players set @s rpg_tw_m1_anim 1
scoreboard players set @s rpg_tw_m1_t 0
return run function rpg:town_models/town_elder/anim/look/tick
