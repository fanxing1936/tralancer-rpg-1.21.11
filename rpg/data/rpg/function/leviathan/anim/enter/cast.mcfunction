# 切到 cast 并立即播放第一帧。
scoreboard players set @s rpg_lv_anim 2
scoreboard players set @s rpg_lv_t 0
return run function rpg:leviathan/anim/cast/tick
