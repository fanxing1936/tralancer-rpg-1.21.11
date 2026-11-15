# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_ei_anim 0
scoreboard players set @s rpg_ei_t 0
return run function rpg:end_illager/anim/idle/tick
