# 切到 normal_stop 并立即播放第一帧。
scoreboard players set @s rpg_tg_anim 4
scoreboard players set @s rpg_tg_t 0
return run function rpg:tower_guard/anim/normal_stop/tick
