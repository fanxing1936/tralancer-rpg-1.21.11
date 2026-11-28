# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_tw_m6_anim 2
scoreboard players set @s rpg_tw_m6_t 0
return run function rpg:town_models/town_inquisitor/anim/attack/tick
