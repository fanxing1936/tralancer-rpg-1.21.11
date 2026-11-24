# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_mmy_anim 0
scoreboard players set @s rpg_mmy_t 0
return run function rpg:merchant_mystery/anim/idle/tick
