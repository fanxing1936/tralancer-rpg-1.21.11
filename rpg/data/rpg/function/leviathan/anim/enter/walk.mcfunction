# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_lv_anim 1
scoreboard players set @s rpg_lv_t 0
return run function rpg:leviathan/anim/walk/tick
