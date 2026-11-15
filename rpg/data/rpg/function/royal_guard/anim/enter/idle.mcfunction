# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_rg_anim 0
scoreboard players set @s rpg_rg_t 0
return run function rpg:royal_guard/anim/idle/tick
