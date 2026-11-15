# 切到 throw 并立即播放第一帧。
scoreboard players set @s rpg_jqdm_anim 2
scoreboard players set @s rpg_jqdm_t 0
return run function rpg:david/anim/throw/tick
