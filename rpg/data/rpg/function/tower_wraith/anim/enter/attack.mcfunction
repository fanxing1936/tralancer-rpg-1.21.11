# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_tw_anim 2
scoreboard players set @s rpg_tw_t 0
return run function rpg:tower_wraith/anim/attack/tick
