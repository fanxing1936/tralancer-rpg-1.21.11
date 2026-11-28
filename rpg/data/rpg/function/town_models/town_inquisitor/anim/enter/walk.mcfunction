# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_tw_m6_anim 1
scoreboard players set @s rpg_tw_m6_t 0
return run function rpg:town_models/town_inquisitor/anim/walk/tick
