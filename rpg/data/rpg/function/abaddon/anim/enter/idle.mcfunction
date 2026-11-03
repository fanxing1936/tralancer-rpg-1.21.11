# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_ab_anim 0
scoreboard players set @s rpg_ab_t 0
return run function rpg:abaddon/anim/idle/tick
