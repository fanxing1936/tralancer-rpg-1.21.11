# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_lv_anim 0
scoreboard players set @s rpg_lv_t 0
return run function rpg:leviathan/anim/idle/tick
