# 切到 talk 并立即播放第一帧。
scoreboard players set @s rpg_tw_m0_anim 1
scoreboard players set @s rpg_tw_m0_t 0
return run function rpg:town_models/town_priest/anim/talk/tick
