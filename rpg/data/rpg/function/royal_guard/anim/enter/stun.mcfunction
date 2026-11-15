# 切到 stun 并立即播放第一帧。
scoreboard players set @s rpg_rg_anim 3
scoreboard players set @s rpg_rg_t 0
return run function rpg:royal_guard/anim/stun/tick
