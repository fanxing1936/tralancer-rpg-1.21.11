# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 0
scoreboard players set @s rpg_pp_t 0
return run function rpg:pope/anim/idle/tick
