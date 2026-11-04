# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_tw_anim 1
scoreboard players set @s rpg_tw_t 0
return run function rpg:tower_wraith/anim/walk/tick
