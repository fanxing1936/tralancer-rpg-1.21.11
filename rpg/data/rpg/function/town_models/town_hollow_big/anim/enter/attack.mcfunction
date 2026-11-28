# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_tw_m11_anim 2
scoreboard players set @s rpg_tw_m11_t 0
return run function rpg:town_models/town_hollow_big/anim/attack/tick
