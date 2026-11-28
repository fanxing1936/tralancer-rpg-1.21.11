# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_tw_m12_anim 2
scoreboard players set @s rpg_tw_m12_t 0
return run function rpg:town_models/town_hollow/anim/attack/tick
