# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 1
scoreboard players set @s rpg_pp_t 0
return run function rpg:pope/anim/walk/tick
