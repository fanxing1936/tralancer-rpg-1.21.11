# 切到 shield_break 并立即播放第一帧。
scoreboard players set @s rpg_tg_anim 6
scoreboard players set @s rpg_tg_t 0
return run function rpg:tower_guard/anim/shield_break/tick
