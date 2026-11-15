# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_mml_anim 0
scoreboard players set @s rpg_mml_t 0
return run function rpg:mammon_lord/anim/idle/tick
