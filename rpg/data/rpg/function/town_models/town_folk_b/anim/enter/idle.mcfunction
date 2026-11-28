# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_tw_m8_anim 0
scoreboard players set @s rpg_tw_m8_t 0
return run function rpg:town_models/town_folk_b/anim/idle/tick
