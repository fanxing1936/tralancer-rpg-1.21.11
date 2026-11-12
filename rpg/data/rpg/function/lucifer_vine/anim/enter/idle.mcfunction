# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_luv_anim 0
scoreboard players set @s rpg_luv_t 0
return run function rpg:lucifer_vine/anim/idle/tick
