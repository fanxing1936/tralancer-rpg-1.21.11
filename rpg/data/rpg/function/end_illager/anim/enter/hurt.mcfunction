# 切到 hurt 并立即播放第一帧。
scoreboard players set @s rpg_ei_anim 6
scoreboard players set @s rpg_ei_t 0
return run function rpg:end_illager/anim/hurt/tick
