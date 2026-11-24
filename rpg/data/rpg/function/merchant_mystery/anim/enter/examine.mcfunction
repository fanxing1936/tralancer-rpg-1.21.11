# 切到 examine 并立即播放第一帧。
scoreboard players set @s rpg_mmy_anim 3
scoreboard players set @s rpg_mmy_t 0
return run function rpg:merchant_mystery/anim/examine/tick
